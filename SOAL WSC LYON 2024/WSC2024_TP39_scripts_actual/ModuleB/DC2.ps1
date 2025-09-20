Write-Host "# === Sub Criterion: dc2.lyon.paris.local ===`r`n" -ForeGroundColor Green
echo "Begin" | oh
pause

Write-Host "# Aspect - Basic: Hostname & IP Address" -ForeGroundColor Green
echo "hostname"
hostname | oh
echo "Get-NetIPAddress | select ipaddress"
Get-NetIPAddress | select ipaddress | oh
pause

Write-Host "# Aspect - ADDS: Check DC2, if sub forest is lyon.paris.local" -ForeGroundColor Green
echo "[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().Name"
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().Name | oh
pause

Write-Host "# Aspect - ADDS: Check if remote1-20 are created" -ForeGroundColor Green
echo "`"REMOTE`" | foreach { Get-ADUser -SearchBase `"OU=`$_,DC=lyon,DC=paris,DC=local`" -Filter * -SearchScope Subtree | measure | select -ExpandProperty Count }" | oh
"REMOTE" | foreach { Get-ADUser -SearchBase "OU=$_,DC=lyon,DC=paris,DC=local" -Filter * -SearchScope Subtree | measure | select -ExpandProperty Count } | oh
pause

Write-Host "# Aspect - ADDS: Check if REMOTE security group is created" -ForeGroundColor Green
echo "`"REMOTE`" | foreach { (Get-ADGroupMember -Identity `"`$_`" -Recursive | Where-Object { `$_.objectClass -eq 'user' }).Count}" | oh
"REMOTE" | foreach { (Get-ADGroupMember -Identity "$_" -Recursive | Where-Object { $_.objectClass -eq 'user' }).Count} | oh
pause
