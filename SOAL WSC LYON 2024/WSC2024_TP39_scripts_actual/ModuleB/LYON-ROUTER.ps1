Write-Host "# === Sub Criterion: lyon-router.lyon.paris.local ===`r`n" -ForeGroundColor Green
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

Write-Host "# Aspect - Site-to-Site VPN: Connection between Paris & Lyon" -ForeGroundColor Green
echo "Get-VpnS2SInterface | select Destination,ConnectionState,Protocol,AuthenticationMethod" | oh
Get-VpnS2SInterface | select Destination,ConnectionState,Protocol,AuthenticationMethod | oh 
pause

Write-Host "# Aspect - DHCP: Lease Range, DNS Servers, Router, Scope Name,  Lease Duration" -ForeGroundColor Green
echo "Get-DhcpServerv4Scope -ComputerName `"lyon-router.lyon.paris.local`" -ErrorAction Stop" | oh

Get-DhcpServerv4Scope -ComputerName "lyon-router.lyon.paris.local" -ErrorAction Stop | oh 

echo "Get the ScopeID. If ScopeID is 10.40.0.0, then use following commands. Change ScopeID accordingly to what was configured for the 10.40.0.0 network:

Get-DhcpServerv4OptionValue -ComputerName `"lyon-router.lyon.paris.local`" -ScopeId `"10.40.0.0`" | Select OptionId,Name,Type,Value" | oh
pause

Write-Host "# Aspect - DHCP: Exclusion" -ForeGroundColor Green
echo "Get-DhcpServerv4ExclusionRange -ComputerName `"lyon-router.lyon.paris.local`" -ScopeId `"10.40.0.0`"" | oh

Get-DhcpServerv4ExclusionRange -ComputerName "lyon-router.lyon.paris.local" -ScopeId "10.40.0.0" | oh 
pause
