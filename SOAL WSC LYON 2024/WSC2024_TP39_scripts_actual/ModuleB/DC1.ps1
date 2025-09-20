Write-Host "# === Sub Criterion: dc1.paris.local ===`r`n" -ForeGroundColor Green
echo "Begin" | oh
pause

Write-Host "# Aspect - Basic: Hostname & IP Address" -ForeGroundColor Green
echo "hostname"
hostname | oh
echo "Get-NetIPAddress | select ipaddress"
Get-NetIPAddress | select ipaddress | oh
pause

Write-Host "# Aspect - ADDS: DC installed and configured" -ForeGroundColor Green
echo "[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().Name"
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().Name | oh
pause

Write-Host "# Aspect - ADDS: Users created with the right OU" -ForeGroundColor Green
echo '"MKT","SALES","TECH","HR" | foreach { Get-ADUser -SearchBase "OU=$_,DC=paris,DC=local" -Filter * -SearchScope Subtree | measure | select -ExpandProperty Count }'
"MKT","SALES","TECH","HR" | foreach { Get-ADUser -SearchBase "OU=$_,DC=paris,DC=local" -Filter * -SearchScope Subtree | measure | select -ExpandProperty Count } | oh
pause

Write-Host "# Aspect - ADDS: Assign Users to Groups" -ForeGroundColor Green
echo '"MKT","SALES","TECH","HR" | foreach { (Get-ADGroupMember -Identity "$_" -Recursive | Where-Object { $_.objectClass -eq 'user' }).Count}'
"MKT","SALES","TECH","HR" | foreach { (Get-ADGroupMember -Identity "$_" -Recursive | Where-Object { $_.objectClass -eq 'user' }).Count} | oh
pause

Write-Host "# Aspect - ADDS: Creation of users using automated powershell script" -ForeGroundColor Green
echo '[MANUAL] Open Powershell on DC1, Run: C:\create_user.ps1 -count 100 Observe if users are created successfully. Errors should be skipped/ignore and not break the script'
echo 'Run: "MKT","SALES","TECH","HR" | foreach { Get-ADUser -SearchBase "OU=$_,DC=paris,DC=local" -Filter * -SearchScope Subtree | measure | select -ExpandProperty Count }'
pause

Write-Host "# Aspect - ADDS: Fine-Graine Password Policy for HR" -ForeGroundColor Green
echo 'Set-ADAccountPassword 'hr1' -OldPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill39@Lyon) -NewPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill40@Skill40@)'
Set-ADAccountPassword 'hr1' -OldPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill39@Lyon) -NewPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill40@Skill40@) | oh
echo 'Set-ADAccountPassword 'hr2' -OldPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill39@Lyon) -NewPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill40)'
Set-ADAccountPassword 'hr2' -OldPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill39@Lyon) -NewPassword (ConvertTo-SecureString -AsPlainText -Force -String Skill40) | oh
pause

Write-Host "# Aspect - DNS: paris.local zone" -ForeGroundColor Green
echo "'www','external','help','app' | foreach { Resolve-DnsName -Type A $_ | select Name,IPAddress }"
'www','external','help','app' | foreach { Resolve-DnsName -Type A $_ | select Name,IPAddress } | oh
pause

Write-Host "# Aspect - DNS: paris.local reverse zone" -ForeGroundColor Green
echo "Resolve-DnsName -Name 10.20.0.11 -Type PTR"
Resolve-DnsName -Name 10.20.0.11 -Type PTR | oh
echo "Resolve-DnsName -Name 10.20.0.10 -Type PTR"
Resolve-DnsName -Name 10.20.0.10 -Type PTR | oh
pause

Write-Host "# Aspect - GPO: Message Banner" -ForeGroundColor Green
echo "On WIN-CLIENT1, login using sales13, access the login page, it should show the correct message" | oh
pause

Write-Host "# Aspect - GPO: Set envionrment variable Name=TheErasTour Value=2024" -ForeGroundColor Green
echo "Continue to use sales13 on WIN-CLIENT1. Open powershell.exe and type the following command: `$Env:TheErasTour" | oh
pause

Write-Host "# Aspect - GPO: Disable the local Administrator Account" -ForeGroundColor Green
echo "Continue to use sales13 on WIN-CLIENT1. Open powershell.exe and type the following command: Get-LocalUser -Name `"Administrator`" | Select-Object Name, Enabled" | oh
pause

Write-Host "# Aspect - GPO: Prevent LM hash from being stored locally in SAM DB and AD" -ForeGroundColor Green
echo "Continue to use sales13 on WIN-CLIENT1, open powershell.exe and type the following command: Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name 'NoLMHash' | Select NoLmHash" | oh
pause

Write-Host "# Aspect - GPO: Check for windows update every Friday at 13hrs" -ForeGroundColor Green
echo "Get-GPOReport -Name `"Updates`" -ReportType HTML -Path `"C:\UpdatesGPO.html`""
Get-GPOReport -Name "Updates" -ReportType HTML -Path "C:\UpdatesGPO.html" | oh
echo "Open C:\UpdatesGPO.html Click on `"Show all`". Under Computer Configuration > Policies > Administrative Templates > Windows Comopents/Windows Update, the following should be present."
pause

Write-Host "# Aspect - GPO: Users in SALES, MKT and HR should not have access to registry" -ForeGroundColor Green
echo "Continue to use sales13 on WIN-CLIENT1. Press `"start`" and type `"regedit`" and press enter. Regedit access should be denied" | oh
pause

Write-Host "# Aspect - GPO: Users in SALES, MKT and HR are not able to run powershell.exe, cmd.exe and access run command" -ForeGroundColor Green
echo "Functional check by logging in as salest13 on WIN-CLIENT1. Press `"start`" and type `"run`" and press enter. Repeat for `"cmd.exe`", `"powershell.exe`"" | oh
pause

Write-Host "# Aspect - GPO: Users in SALES, MKT and HR file history should be turned off" -ForeGroundColor Green
echo "Continue to use sales13 on WIN-CLIENT1. Press `"start`" and type `"File History`". Click on `"Restore your files with File History`". File History should be shown as Turned Off." | oh
pause

Write-Host "# Aspect - GPO: Tech group should have powershell.exe launched at logon" -ForeGroundColor Green
echo "Functional check by logging in as tech13 on WIN-CLIENT1. powershell.exe should be launched upon logged in." | oh
pause