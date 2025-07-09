$url = "http://localhost:5000/expand"
$headers = @{ "Content-Type" = "application/json" }
$body = '{"url": "http://bit.ly/4lepK9e"}'

$response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body
$response | ConvertTo-Json -Depth 5