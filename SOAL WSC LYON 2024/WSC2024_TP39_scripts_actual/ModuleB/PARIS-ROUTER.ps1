Write-Host "# === Sub Criterion: paris-router.paris.local ===`r`n" -ForeGroundColor Green
echo "Begin" | oh
pause

Write-Host "# Aspect - Basic: Hostname & IP Address" -ForeGroundColor Green
echo "hostname"
hostname | oh
echo "Get-NetIPAddress | select ipaddress"
Get-NetIPAddress | select ipaddress | oh
pause

Write-Host "# Aspect - ADDS: Domain member" -ForeGroundColor Green
echo "Get-ComputerInfo | select CsDomain"
Get-ComputerInfo | select CsDomain | oh
pause

Write-Host "# Aspect - Reverse Proxy: PARIS-Router is configured as Reverse Proxy" -ForeGroundColor Green
echo "[MANUAL] From LA-Router, access https://www.paris.com using microsoft edge. It should show `"This is external WSC2024`"" | oh
pause

Write-Host "# Aspect - RRAS:DHCP Relay Agent" -ForeGroundColor Green
echo "netsh routing dump" | oh
netsh routing dump | oh
pause