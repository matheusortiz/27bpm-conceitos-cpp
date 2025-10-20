# Instalador Windows (PowerShell)
# Uso: abra PowerShell na pasta do projeto e execute:
#       PowerShell -ExecutionPolicy Bypass -File .\install_windows.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "Instalador do projeto 27BPM (v0.2)"
Write-Host "Diretório do projeto: $scriptDir"

# verifica python
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) {
    Write-Error "Python não encontrado no PATH. Instale Python 3.8+ e reexecute."
    exit 1
}

# cria venv se não existir
$venvPath = Join-Path $scriptDir 'venv'
if (-Not (Test-Path (Join-Path $venvPath 'Scripts\python.exe'))) {
    Write-Host "Criando venv em $venvPath ..."
    & $pyCmd.Source -m venv $venvPath
} else {
    Write-Host "Venv já existe — pulando criação."
}

$pythonVenv = Join-Path $venvPath 'Scripts\python.exe'
if (-Not (Test-Path $pythonVenv)) {
    Write-Error "Python do venv não encontrado em $pythonVenv"
    exit 1
}

# atualiza pip e instala dependências
Write-Host "Atualizando pip e instalando dependências (pandas, fpdf)..."
& $pythonVenv -m pip install --upgrade pip | Out-Null
& $pythonVenv -m pip install pandas fpdf | Out-Null
Write-Host "Dependências instaladas."

# cria launcher .bat
$batPath = Join-Path $scriptDir 'run_main.bat'
$batContent = @"
@echo off
REM Lança main.py usando o Python do venv localizado na pasta do projeto
set SCRIPT_DIR=%~dp0
"%SCRIPT_DIR%venv\Scripts\python.exe" "%SCRIPT_DIR%main.py" %*
pause
"@
Set-Content -Path $batPath -Value $batContent -Encoding ASCII
Write-Host "Criado launcher: run_main.bat"

# cria launcher .ps1
$psPath = Join-Path $scriptDir 'run_main.ps1'
$psContent = @"
\$here = Split-Path -Parent \$MyInvocation.MyCommand.Definition
& "\$here\venv\Scripts\python.exe" "\$here\main.py" \$args
"@
Set-Content -Path $psPath -Value $psContent -Encoding UTF8
Write-Host "Criado launcher: run_main.ps1"

Write-Host "Instalação concluída."
Write-Host "Para executar: use run_main.bat (duplo clique) ou PowerShell: .\run_main.ps1"