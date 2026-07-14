$root = 'C:\Users\MONSTER\Desktop\portfolio-hosted'
$port = 8010

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()
Write-Host "Portfolio server running at http://localhost:$port" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $req = $context.Request
        $res = $context.Response

        $localPath = $req.Url.LocalPath
        if ($localPath -eq '/') { $localPath = '/index.html' }

        $filePath = Join-Path $root ($localPath.TrimStart('/').Replace('/', '\'))

        if (Test-Path $filePath -PathType Leaf) {
            $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
            $mime = 'application/octet-stream'
            if ($ext -eq '.html')  { $mime = 'text/html; charset=utf-8' }
            elseif ($ext -eq '.css')   { $mime = 'text/css' }
            elseif ($ext -eq '.js')    { $mime = 'application/javascript' }
            elseif ($ext -eq '.jpg')   { $mime = 'image/jpeg' }
            elseif ($ext -eq '.jpeg')  { $mime = 'image/jpeg' }
            elseif ($ext -eq '.png')   { $mime = 'image/png' }
            elseif ($ext -eq '.svg')   { $mime = 'image/svg+xml' }
            elseif ($ext -eq '.pdf')   { $mime = 'application/pdf' }
            elseif ($ext -eq '.md')    { $mime = 'text/plain; charset=utf-8' }

            $bytes = [System.IO.File]::ReadAllBytes($filePath)
            $res.ContentType = $mime
            $res.ContentLength64 = $bytes.Length
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
            Write-Host "200  $localPath"
        }
        else {
            $res.StatusCode = 404
            $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $localPath")
            $res.ContentLength64 = $msg.Length
            $res.OutputStream.Write($msg, 0, $msg.Length)
            Write-Host "404  $localPath" -ForegroundColor Red
        }
        $res.Close()
    }
    catch {
        # connection reset etc, keep going
    }
}
