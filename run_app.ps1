$ErrorActionPreference = "Stop"

$bundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (Test-Path -LiteralPath $bundledPython) {
    & $bundledPython (Join-Path $PSScriptRoot "main.py")
} elseif (Test-Path -LiteralPath $venvPython) {
    & $venvPython (Join-Path $PSScriptRoot "main.py")
} else {
    python (Join-Path $PSScriptRoot "main.py")
}
