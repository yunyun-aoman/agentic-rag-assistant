$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $ProjectRoot

python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements-core.txt

Write-Host ""
Write-Host "Core environment installed."
Write-Host "Activate with:"
Write-Host "  .\.venv\Scripts\activate"
Write-Host ""
Write-Host "Optional RAG extras:"
Write-Host "  .\.venv\Scripts\python.exe -m pip install -r requirements-rag-extra.txt"
