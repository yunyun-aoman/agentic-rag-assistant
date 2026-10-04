$ErrorActionPreference = "Continue"

Write-Host "== System =="
python --version
python -m pip --version
git --version
docker --version
docker compose version

Write-Host ""
Write-Host "== Python packages in .venv =="
$VenvPython = ".\.venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
  & $VenvPython -c "import importlib.util; mods={'langgraph':'langgraph','openai':'openai','dotenv':'python-dotenv','requests':'requests','bs4':'beautifulsoup4','fastapi':'fastapi','uvicorn':'uvicorn','qdrant_client':'qdrant-client','sentence_transformers':'sentence-transformers','rank_bm25':'rank-bm25','pypdf':'pypdf','docx':'python-docx','pytest':'pytest','ruff':'ruff'}; [print(('OK   ' if importlib.util.find_spec(m) else 'MISS ')+p) for m,p in mods.items()]"
} else {
  Write-Host "MISS .venv"
}

Write-Host ""
Write-Host "== Network =="
Test-NetConnection mirrors.aliyun.com -Port 443 | Select-Object ComputerName,RemotePort,TcpTestSucceeded
Test-NetConnection pypi.org -Port 443 | Select-Object ComputerName,RemotePort,TcpTestSucceeded

Write-Host ""
Write-Host "== Proxy env =="
cmd /c set | findstr /i proxy
