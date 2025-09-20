Write-Host "# === Sub Criterion: nw-srv.paris.local ===`r`n" -ForeGroundColor Green
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

Write-Host "# Aspect - DNS: Secondary DNS Zone transfer from Primary DNS" -ForeGroundColor Green
echo "`"dc1`",`"nw-srv`" | foreach { Get-DnsServerResourceRecord -ComputerName `"`$_.paris.local`" -ZoneName `"paris.local`" -Name `"@`" -RRType SOA -ErrorAction Stop | Select-Object -ExpandProperty RecordData | Select-Object -Property SerialNumber}"
"dc1","nw-srv" | foreach { Get-DnsServerResourceRecord -ComputerName "$_.paris.local" -ZoneName "paris.local" -Name "@" -RRType SOA -ErrorAction Stop | Select-Object -ExpandProperty RecordData | Select-Object -Property SerialNumber} | oh
pause

Write-Host "# Aspect - DHCP: Lease Range, DNS Servers, Router, Scope Name,  Lease Duration" -ForeGroundColor Green
echo "Get-DhcpServerv4Scope -ComputerName `"nw-srv.paris.local`" -ErrorAction Stop"
Get-DhcpServerv4Scope -ComputerName "nw-srv.paris.local" -ErrorAction Stop | oh
echo "Get the ScopeID. If ScopeID is 10.30.0.0, then use following commands. Change ScopeID accordingly to what was configured for the 10.30.0.0 network:"
echo "Get-DhcpServerv4OptionValue -ComputerName `"nw-srv.paris.local`" -ScopeId `"10.30.0.0`" | Select OptionId,Name,Type,Value"
pause

Write-Host "# Aspect - DHCP: Exclusion" -ForeGroundColor Green
echo "Get-DhcpServerv4ExclusionRange -ComputerName `"nw-srv.paris.local`" -ScopeId `"10.30.0.0`""
Get-DhcpServerv4ExclusionRange -ComputerName "nw-srv.paris.local" -ScopeId "10.30.0.0" | oh
pause