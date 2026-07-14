@echo off
echo Starting local server for portfolio-hosted...
echo.
echo Files will be served at: http://localhost:8010
echo.
echo Press Ctrl+C to stop.
echo.

REM Try Antigravity IDE bundled node first
set "AG_NODE=%LOCALAPPDATA%\Programs\Antigravity IDE\resources\app\node_modules\.bin"
if exist "%AG_NODE%\serve.cmd" (
    echo Using Antigravity IDE serve...
    "%AG_NODE%\serve.cmd" "C:\Users\MONSTER\Desktop\portfolio-hosted" -l 8010
    goto :done
)

REM Try Windows Store python
python -m http.server 8010 --directory "C:\Users\MONSTER\Desktop\portfolio-hosted" 2>nul
if %ERRORLEVEL% EQU 0 goto :done

python3 -m http.server 8010 --directory "C:\Users\MONSTER\Desktop\portfolio-hosted" 2>nul
if %ERRORLEVEL% EQU 0 goto :done

REM Try PowerShell fallback
echo Trying PowerShell HTTP listener...
powershell -NoProfile -Command "& {
  $listener = New-Object System.Net.HttpListener
  $listener.Prefixes.Add('http://localhost:8010/')
  $listener.Start()
  Write-Host 'Server running at http://localhost:8010'
  Write-Host 'Press Ctrl+C to stop.'
  while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    $localPath = $request.Url.LocalPath
    if ($localPath -eq '/') { $localPath = '/index.html' }
    $filePath = 'C:\Users\MONSTER\Desktop\portfolio-hosted' + $localPath.Replace('/', '\')
    if (Test-Path $filePath) {
      $ext = [System.IO.Path]::GetExtension($filePath)
      $mime = switch ($ext) {
        '.html' { 'text/html; charset=utf-8' }
        '.css'  { 'text/css' }
        '.js'   { 'application/javascript' }
        '.jpg'  { 'image/jpeg' }
        '.jpeg' { 'image/jpeg' }
        '.png'  { 'image/png' }
        '.svg'  { 'image/svg+xml' }
        '.pdf'  { 'application/pdf' }
        default { 'application/octet-stream' }
      }
      $bytes = [System.IO.File]::ReadAllBytes($filePath)
      $response.ContentType = $mime
      $response.ContentLength64 = $bytes.Length
      $response.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $response.StatusCode = 404
    }
    $response.Close()
  }
}"

:done
echo Server stopped.
pause
