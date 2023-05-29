$scriptPath = $MyInvocation.MyCommand.Path
$dirPath = Split-Path $scriptPath

$pythonPath = "C:\Users\Josh\AppData\Local\Programs\Python\Python311"
$blackPath = Join-Path $pythonPath "Scripts\black.exe"
$flake8Path = Join-Path $pythonPath "Scripts\flake8.exe"

$pyFiles = Get-ChildItem -Path $dirPath -Filter "*.py" -Recurse

foreach ($file in $pyFiles) {
    Write-Host "Running Black for formatting on $($file.FullName)..."
    & $blackPath $file.FullName

    Write-Host "Running Flake8 on $($file.FullName)..."
    & $flake8Path $file.FullName
}
