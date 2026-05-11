param(
    [string]$InstallDir = (Join-Path $HOME "ResearchFlowOS"),
    [string]$RepoUrl = "https://github.com/Yuhang-Xiao/workflow1.git",
    [string]$Branch = "researchflow",
    [switch]$Force,
    [switch]$NoPath
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Resolve-Python {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return $python.Source
    }
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        return $py.Source
    }
    throw "Python 3.11+ was not found on PATH. Install Python first, then rerun this script."
}

function Ensure-Git {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        throw "Git was not found on PATH. Install Git for Windows first, then rerun this script."
    }
}

function Add-UserPath {
    param([string]$Directory)
    $current = [Environment]::GetEnvironmentVariable("Path", "User")
    $parts = @()
    if ($current) {
        $parts = $current -split ";" | Where-Object { $_ }
    }
    if ($parts -notcontains $Directory) {
        $newPath = if ($current) { "$current;$Directory" } else { $Directory }
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    }
    if (($env:Path -split ";") -notcontains $Directory) {
        $env:Path = "$env:Path;$Directory"
    }
}

$InstallDir = [System.IO.Path]::GetFullPath($InstallDir)
$VenvDir = Join-Path $InstallDir ".venv"
$BinDir = Join-Path $InstallDir "bin"

Write-Step "Installing ResearchFlow OS into $InstallDir"
Ensure-Git
$Python = Resolve-Python

if (Test-Path -LiteralPath $InstallDir) {
    $hasGit = Test-Path -LiteralPath (Join-Path $InstallDir ".git")
    $hasFiles = (Get-ChildItem -LiteralPath $InstallDir -Force | Select-Object -First 1) -ne $null
    if ($hasGit) {
        Write-Step "Updating existing checkout"
        git -C $InstallDir fetch origin $Branch
        git -C $InstallDir checkout $Branch
        git -C $InstallDir pull --ff-only origin $Branch
    } elseif ($Force) {
        Write-Step "Removing existing non-git install directory because -Force was supplied"
        Remove-Item -LiteralPath $InstallDir -Recurse -Force
        git clone --branch $Branch --single-branch $RepoUrl $InstallDir
    } elseif ($hasFiles) {
        throw "InstallDir exists and is not a ResearchFlow OS git checkout: $InstallDir. Use -Force or choose another -InstallDir."
    } else {
        git clone --branch $Branch --single-branch $RepoUrl $InstallDir
    }
} else {
    $parent = Split-Path -Parent $InstallDir
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
    git clone --branch $Branch --single-branch $RepoUrl $InstallDir
}

Write-Step "Creating virtual environment"
& $Python -m venv $VenvDir
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path -LiteralPath $VenvPython)) {
    throw "Virtual environment Python was not created: $VenvPython"
}

Write-Step "Installing package in editable mode"
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -e $InstallDir

Write-Step "Creating command wrappers"
New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
$WorkflowExe = Join-Path $VenvDir "Scripts\workflow1.exe"
$ResearchflowExe = Join-Path $VenvDir "Scripts\researchflow.exe"

$workflowCmd = @"
@echo off
set "WORKFLOW1_HOME=$InstallDir"
pushd "$InstallDir"
"$WorkflowExe" %*
set EXITCODE=%ERRORLEVEL%
popd
exit /b %EXITCODE%
"@
$researchflowCmd = @"
@echo off
set "WORKFLOW1_HOME=$InstallDir"
pushd "$InstallDir"
"$ResearchflowExe" %*
set EXITCODE=%ERRORLEVEL%
popd
exit /b %EXITCODE%
"@

Set-Content -LiteralPath (Join-Path $BinDir "workflow1.cmd") -Value $workflowCmd -Encoding ASCII
Set-Content -LiteralPath (Join-Path $BinDir "researchflow.cmd") -Value $researchflowCmd -Encoding ASCII

if (-not $NoPath) {
    Write-Step "Adding wrapper directory to user PATH"
    Add-UserPath -Directory $BinDir
}

Write-Step "Verifying installation"
& $VenvPython -m workflow1 --stage launch | Out-Host

Write-Host ""
Write-Host "ResearchFlow OS is installed." -ForegroundColor Green
Write-Host "Try one of these commands:"
Write-Host "  researchflow --stage launch"
Write-Host "  workflow1 --stage intake --raw-dir examples"
Write-Host ""
Write-Host "If this is a new terminal session, reopen PowerShell if PATH changes are not visible yet."
