[CmdletBinding()]
param(
    [switch]$SetupToken,
    [string]$RecipeJson,
    [string]$OutputDirectory = (Join-Path $env:USERPROFILE 'Desktop\FM27_Builds'),
    [ValidateRange(1, 60)][int]$TimeoutMinutes = 15,
    [switch]$KeepCloudArtifact
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repository = 'eslaulau/fm-ta'
$WorkflowFile = 'fm27-tactic-build.yml'
$ApiRoot = "https://api.github.com/repos/$Repository"
$TokenPath = Join-Path $env:APPDATA 'FM27TacticBuilder\github-token.dpapi'
$ApiVersion = '2026-03-10'

function Get-Fm27GitHubToken {
    if (-not (Test-Path -LiteralPath $TokenPath -PathType Leaf)) {
        throw "GitHub token is not configured. Run this script once with -SetupToken."
    }
    $encrypted = Get-Content -LiteralPath $TokenPath -Raw
    $secure = ConvertTo-SecureString -String $encrypted
    $credential = New-Object System.Net.NetworkCredential('', $secure)
    return $credential.Password
}

function Invoke-Fm27GitHubApi {
    param(
        [Parameter(Mandatory)][ValidateSet('GET', 'POST', 'DELETE')][string]$Method,
        [Parameter(Mandatory)][string]$Path,
        [hashtable]$Body
    )
    $parameters = @{
        Method = $Method
        Uri = "$ApiRoot/$Path"
        Headers = $script:GitHubHeaders
        ErrorAction = 'Stop'
    }
    if ($null -ne $Body) {
        $parameters.Body = $Body | ConvertTo-Json -Depth 80 -Compress
        $parameters.ContentType = 'application/json; charset=utf-8'
    }
    return Invoke-RestMethod @parameters
}

function Get-Fm27SafeStem {
    param([string]$Value)
    $stem = [regex]::Replace([string]$Value, '[^\p{L}\p{N}_\.-]+', '_').Trim([char[]]@('.', '_', '-'))
    if ([string]::IsNullOrWhiteSpace($stem)) { return 'FM27_Tactic' }
    return $stem
}

if ($SetupToken) {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
        throw 'DPAPI token storage in this script is supported on Windows only.'
    }
    $secureToken = Read-Host 'Paste a fine-grained GitHub token with Actions: write for eslaulau/fm-ta' -AsSecureString
    if ($secureToken.Length -lt 20) { throw 'The token looks too short; nothing was saved.' }
    $tokenDirectory = Split-Path -Parent $TokenPath
    New-Item -ItemType Directory -Path $tokenDirectory -Force | Out-Null
    $encryptedToken = ConvertFrom-SecureString -SecureString $secureToken
    Set-Content -LiteralPath $TokenPath -Value $encryptedToken -Encoding ASCII -NoNewline
    Write-Host 'Token saved with Windows DPAPI for the current Windows user.' -ForegroundColor Green
    Write-Host 'The token is not written to this repository or to the tactic recipe.'
    return
}

if ([string]::IsNullOrWhiteSpace($RecipeJson)) {
    try { $RecipeJson = [string](Get-Clipboard -Raw) }
    catch { throw 'Could not read the clipboard. Copy the complete tactic JSON first, or pass -RecipeJson.' }
}
if ([string]::IsNullOrWhiteSpace($RecipeJson)) { throw 'Clipboard is empty. Copy the complete tactic JSON object first.' }
if ($RecipeJson.Length -gt 60000) { throw 'Recipe JSON exceeds the 60,000-character safety limit for this workflow input.' }

try {
    $recipeObject = ConvertFrom-Json -InputObject $RecipeJson -ErrorAction Stop
} catch {
    throw "Clipboard content is not valid JSON: $($_.Exception.Message)"
}
if ($null -eq $recipeObject -or $recipeObject -is [string] -or $recipeObject -is [array]) {
    throw 'Recipe JSON root must be an object, not an array or scalar.'
}

$token = Get-Fm27GitHubToken
$script:GitHubHeaders = @{
    Authorization = "Bearer $token"
    Accept = 'application/vnd.github+json'
    'X-GitHub-Api-Version' = $ApiVersion
    'User-Agent' = 'FM27-Tactic-Builder'
}

$tacticName = [string]$recipeObject.name
if ([string]::IsNullOrWhiteSpace($tacticName)) { $tacticName = 'FM27_Tactic' }
$safeStem = Get-Fm27SafeStem -Value $tacticName
$dispatchBody = @{
    ref = 'main'
    inputs = @{ recipe_json = $RecipeJson }
}

Write-Host "Submitting in-memory tactic object to $Repository ..."
$dispatch = Invoke-Fm27GitHubApi -Method POST -Path "actions/workflows/$WorkflowFile/dispatches" -Body $dispatchBody
$runId = [long]$dispatch.workflow_run_id
if ($runId -le 0) {
    throw 'GitHub did not return workflow_run_id. Confirm the token has Actions: write and the workflow is enabled.'
}
$run = $null
$deadline = (Get-Date).AddMinutes($TimeoutMinutes)
do {
    Start-Sleep -Seconds 4
    $run = Invoke-Fm27GitHubApi -Method GET -Path "actions/runs/$runId"
    if ($run.status -eq 'completed') { break }
} while ((Get-Date) -lt $deadline)

if ($null -eq $run -or $run.status -ne 'completed') {
    Write-Host "Build is still running: https://github.com/$Repository/actions/runs/$runId" -ForegroundColor Yellow
    throw "Timed out after $TimeoutMinutes minutes. The run continues on GitHub; use the run URL above to inspect it."
}
if ($run.conclusion -ne 'success') {
    try {
        $jobs = Invoke-Fm27GitHubApi -Method GET -Path "actions/runs/$runId/jobs?per_page=100"
        foreach ($job in $jobs.jobs) {
            foreach ($step in $job.steps) {
                if ($step.conclusion -eq 'failure') { Write-Host "Failed step: $($job.name) / $($step.name)" -ForegroundColor Red }
            }
        }
    } catch { }
    Write-Host "Build failed: https://github.com/$Repository/actions/runs/$runId" -ForegroundColor Red
    throw "FM27 cloud build concluded with '$($run.conclusion)'."
}

$artifactResponse = Invoke-Fm27GitHubApi -Method GET -Path "actions/runs/$runId/artifacts?per_page=100"
$expectedArtifact = "FM27_${safeStem}_run$($run.run_number)"
$artifact = @($artifactResponse.artifacts | Where-Object { $_.name -eq $expectedArtifact -and -not $_.expired } | Select-Object -First 1)
if ($artifact.Count -ne 1) {
    throw "Build succeeded but artifact '$expectedArtifact' was not found. Run: https://github.com/$Repository/actions/runs/$runId"
}

$buildDirectory = Join-Path $OutputDirectory $expectedArtifact
New-Item -ItemType Directory -Path $buildDirectory -Force | Out-Null
$zipPath = Join-Path $buildDirectory "$expectedArtifact.zip"
$downloadUri = "$ApiRoot/actions/artifacts/$($artifact[0].id)/zip"
Write-Host 'Downloading the FMF and its readback report ...'
Invoke-WebRequest -Uri $downloadUri -Headers $script:GitHubHeaders -OutFile $zipPath -ErrorAction Stop
Expand-Archive -LiteralPath $zipPath -DestinationPath $buildDirectory -Force
Remove-Item -LiteralPath $zipPath -Force

$fmfFiles = @(Get-ChildItem -LiteralPath $buildDirectory -Filter '*.fmf' -File)
$reportFiles = @(Get-ChildItem -LiteralPath $buildDirectory -Filter '*.report.json' -File)
if ($fmfFiles.Count -ne 1 -or $reportFiles.Count -ne 1) {
    throw "Artifact content is incomplete. Expected one FMF and one report in $buildDirectory"
}
$report = Get-Content -LiteralPath $reportFiles[0].FullName -Raw | ConvertFrom-Json -ErrorAction Stop
$actualHash = (Get-FileHash -LiteralPath $fmfFiles[0].FullName -Algorithm SHA256).Hash.ToLowerInvariant()
if ($report.status -ne 'offline_binary_roundtrip_verified_not_game_import_verified') { throw "Unexpected D3 report status: $($report.status)" }
if ([long]$report.bytes -ne [long](Get-Item -LiteralPath $fmfFiles[0].FullName).Length) { throw 'FMF byte count does not match the report.' }
if ([string]$report.sha256 -ne $actualHash) { throw 'FMF SHA-256 does not match the report.' }
if (@($report.player_phase_map).Count -ne 22 -or @($report.readback_player_phase_map).Count -ne 22) { throw 'The design/readback phase count is not 22/22.' }
$requiredChecks = @(
    'fmf_outer_roundtrip',
    'all_member_decrypt_and_zstd_checksums',
    'tac_full_parse',
    '11_ip_oop_pairs',
    '22_positions_roles_pi_readback_exact',
    'pi_permissions_checked_against_catalog',
    'team_instruction_vector_readback',
    'native_style_string_and_code_readback'
)
foreach ($check in $requiredChecks) {
    if ($report.checks.$check -ne $true) { throw "D3 check failed in downloaded report: $check" }
}

if (-not $KeepCloudArtifact) {
    Invoke-Fm27GitHubApi -Method DELETE -Path "actions/artifacts/$($artifact[0].id)" | Out-Null
    Write-Host 'Cloud artifact deleted after verified local download. Use -KeepCloudArtifact to retain it online.' -ForegroundColor Yellow
}

Write-Host ''
Write-Host 'FM27 native tactic build completed and verified.' -ForegroundColor Green
Write-Host "FMF:    $($fmfFiles[0].FullName)"
Write-Host "Report: $($reportFiles[0].FullName)"
Write-Host "Bytes:  $($report.bytes)"
Write-Host "SHA256: $actualHash"
Write-Host "D3:     22 designed phases / 22 read-back phases; all required checks passed"
Write-Host "D4/D5:  Not tested by this workflow" -ForegroundColor Yellow
Write-Host "Run:    https://github.com/$Repository/actions/runs/$runId"
