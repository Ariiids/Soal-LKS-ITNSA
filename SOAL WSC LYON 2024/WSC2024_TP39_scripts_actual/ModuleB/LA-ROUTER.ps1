Write-Host "# === Sub Criterion: LA-Router ===`r`n" -ForeGroundColor Green
echo "Begin" | oh
pause

Write-Host "# Aspect - Basic: Hostname & IP Address" -ForeGroundColor Green
echo "hostname"
hostname | oh
echo "Get-NetIPAddress | select ipaddress"
Get-NetIPAddress | select ipaddress | oh
pause

Write-Host "# Aspect - DNS: paris.com zone" -ForeGroundColor Green
echo "'external.paris.com' | foreach { Resolve-DnsName -Type A `$_ | select Name,IPAddress }"
'external.paris.com' | foreach { Resolve-DnsName -Type A $_ | select Name,IPAddress } | oh
pause

Write-Host "# Aspect - RRAS: Routing is installed and configured" -ForeGroundColor Green
echo "On LA-Router using the Administrator account,  Server Manager > Tools > Routing and Remote Access > LA-ROUTER > IPv4 > General" | oh
pause