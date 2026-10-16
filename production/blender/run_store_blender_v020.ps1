param([switch]$SkipPreviews)

$ErrorActionPreference = 'Stop'

$package = Get-AppxPackage -Name 'BlenderFoundation.Blender' | Select-Object -First 1
if (-not $package) {
  throw 'Blender Store package is not installed. Install Blender 5.2 LTS or run the build script with a regular Blender executable.'
}

$source = Join-Path $package.InstallLocation 'Blender'
$runtime = Join-Path $env:TEMP 'motionboard-blender-runtime'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $source 'blender.exe') -Destination $runtime -Force
foreach ($directory in @('blender.crt', 'blender.shared', '5.2')) {
  Copy-Item -LiteralPath (Join-Path $source $directory) -Destination $runtime -Recurse -Force
}
Get-ChildItem -LiteralPath $source -File -Filter '*.dll' | Copy-Item -Destination $runtime -Force

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$buildScript = Join-Path $PSScriptRoot 'build_schoolboy_v020.py'
$blender = Join-Path $runtime 'blender.exe'
$log = Join-Path $env:TEMP 'motionboard-schoolboy-v020-build.log'
$buildArguments = @('--background', '--python', $buildScript, '--', '--output-root', $repositoryRoot)
if ($SkipPreviews) { $buildArguments += '--skip-previews' }
& $blender @buildArguments *> $log
if ($LASTEXITCODE -ne 0) {
  Get-Content -LiteralPath $log -Tail 100
  throw "Blender v0.2 build failed with exit code $LASTEXITCODE. Full log: $log"
}
Get-Content -LiteralPath $log -Tail 30
