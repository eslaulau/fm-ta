@echo off
chcp 65001 >nul
setlocal
set "ROOT=%~dp0"
if "%~1"=="" (
  set "RECIPE=%ROOT%FM27_A9.0.2_GEN1.txt"
) else (
  set "RECIPE=%~1"
)
for %%F in ("%RECIPE%") do set "OUT=%%~dpnF_Offline.fmf"
py -3.12 -m pip show cryptography >nul 2>nul
if errorlevel 1 (
  echo 缺少 Python 依赖，请先运行“安装依赖.bat”。
  pause
  exit /b 2
)
py -3.12 "%ROOT%FM27GEN1_Offline_FMF_Generator.py" "%RECIPE%" --catalog "%ROOT%catalog.json" --output "%OUT%"
echo.
if errorlevel 1 (
  echo 生成失败，请将上方错误内容发回。
) else (
  echo 生成完成。请在 FM27 内手动导入生成的 FMF 验证。
)
pause
