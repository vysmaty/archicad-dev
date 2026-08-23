[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("27", "28", "29")]
    [string]$Version,

    [ValidateSet("Debug", "Release")]
    [string]$Configuration = "Debug"
)

$ErrorActionPreference = "Stop"
$preset = "ac$Version-$($Configuration.ToLowerInvariant())"
$env:AC_API_DEVKIT_DIR = (uv run tools/devkit.py path $Version).Trim()

if (-not $env:AC_API_DEVKIT_DIR.EndsWith("Support")) {
    throw "The Archicad DevKit path must point to its Support folder."
}

cmake --preset $preset
if ($LASTEXITCODE -ne 0) {
    throw "CMake configuration failed for $preset."
}

cmake --build --preset $preset
if ($LASTEXITCODE -ne 0) {
    throw "CMake build failed for $preset."
}
