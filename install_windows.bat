@echo off
REM Executa o instalador PowerShell com ExecutionPolicy Bypass
cd /d "%~dp0"
echo Executando install_windows.ps1 com ExecutionPolicy Bypass...
PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_windows.ps1" %*
if errorlevel 1 (
  echo Erro durante a execucao do instalador.
) else (
  echo Instalacao concluida.
)
pause