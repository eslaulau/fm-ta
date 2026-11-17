@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3.12 -m pip install -r requirements.txt
if errorlevel 1 (
  echo 依赖安装失败，请检查 Python 3.12 和 pip。
) else (
  echo 依赖已安装。之后生成 FMF 时只需提供本地模板和配方。
)
pause
