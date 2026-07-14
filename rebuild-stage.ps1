# Rebuilds Desktop\portfolio-stage (production-only subset of portfolio-hosted)
# and Desktop\netlify-linux.zip from it. Safe to run anytime — staging is derived,
# not authored. Run from anywhere: powershell -File rebuild-stage.ps1
# (portfolio-stage vanished once on 2026-07-11; this makes it reproducible.)

$hosted = 'C:\Users\MONSTER\Desktop\portfolio-hosted'
$stage  = 'C:\Users\MONSTER\Desktop\portfolio-stage'
$zipPath = 'C:\Users\MONSTER\Desktop\netlify-linux.zip'

if (Test-Path $stage) { Remove-Item $stage -Recurse -Force }
New-Item -ItemType Directory -Force $stage | Out-Null

# Core files that make up the served site (relative paths from hosted root)
$core = @('index.html','about.html','robots.txt','sitemap.xml')
Get-ChildItem "$hosted\work" -Filter *.html | ForEach-Object { $core += "work\$($_.Name)" }
Get-ChildItem "$hosted\assets\css" -Filter *.css | ForEach-Object { $core += "assets\css\$($_.Name)" }
Get-ChildItem "$hosted\assets\js" -Filter *.js | ForEach-Object { $core += "assets\js\$($_.Name)" }
$core += 'pdf\index.html'

foreach ($rel in $core) {
  $src = Join-Path $hosted $rel
  if (-not (Test-Path $src)) { Write-Host "MISSING CORE: $rel"; continue }
  $dst = Join-Path $stage $rel
  New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
  Copy-Item $src $dst -Force
}

# Collect referenced assets from all core text files (HTML + CSS)
$assetSet = [System.Collections.Generic.HashSet[string]]::new()
$rx = [regex]'(?:src|href)\s*=\s*"([^"]+)"|url\(\s*[''"]?([^''")]+)[''"]?\s*\)'
foreach ($rel in $core) {
  $src = Join-Path $hosted $rel
  if (-not (Test-Path $src)) { continue }
  $dir = Split-Path $src
  $txt = [System.IO.File]::ReadAllText($src, [System.Text.Encoding]::UTF8)
  foreach ($m in $rx.Matches($txt)) {
    $ref = if ($m.Groups[1].Success) { $m.Groups[1].Value } else { $m.Groups[2].Value }
    if ($ref -match '^(https?:|mailto:|#|data:|tel:)') { continue }
    if ($ref -notmatch '\.(jpg|jpeg|png|webp|gif|svg|ico|css|js|woff2?|ttf|otf)(\?.*)?$') { continue }
    $ref = ($ref -split '[?#]')[0]
    $abs = [System.IO.Path]::GetFullPath((Join-Path $dir ($ref -replace '/', '\')))
    if ($abs.StartsWith($hosted, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path $abs)) {
      [void]$assetSet.Add($abs)
    }
  }
}

$copied = 0
foreach ($abs in $assetSet) {
  $rel = $abs.Substring($hosted.Length + 1)
  $dst = Join-Path $stage $rel
  New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
  Copy-Item $abs $dst -Force
  $copied++
}

$stageFiles = (Get-ChildItem $stage -Recurse -File | Measure-Object).Count
$stageSize = (Get-ChildItem $stage -Recurse -File | Measure-Object Length -Sum).Sum / 1MB
"Stage rebuilt: $stageFiles files ({0:N1} MB), {1} core + {2} referenced assets" -f $stageSize, $core.Count, $copied

# Build the zip with forward-slash entries (Linux/Netlify needs this)
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$fs = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::Create)
$zip = New-Object System.IO.Compression.ZipArchive($fs, [System.IO.Compression.ZipArchiveMode]::Create)
$zc = 0
Get-ChildItem $stage -Recurse -File | ForEach-Object {
  $rel = $_.FullName.Substring($stage.Length + 1)
  $entry = $rel -replace '\\', '/'
  [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $entry) | Out-Null
  $zc++
}
$zip.Dispose(); $fs.Dispose()
"Zip built: $zc entries, {0:N1} MB" -f ((Get-Item $zipPath).Length / 1MB)
