Write-Host "# === Sub Criterion: web-srv.paris.local ===`r`n" -ForeGroundColor Green
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

Write-Host "# Aspect - CA: Root CA for paris.local" -ForeGroundColor Green
echo "On web-srv powershell: Get-Service -Name certsvc" | oh
Get-Service -Name certsvc | oh 
pause

Write-Host "# Aspect - CA: Certificate Enrollment" -ForeGroundColor Green
echo "[Manual] Check enroll certificates for www.paris.local and help.paris.local and distribute them domain wide.

Server Manager > Tools > Certification Authority > Issued Certificates.

Check certificates with Certificate Template of `"Web Server`", or check each issued certificated by double-clicking and assert it certificates are issued to www.paris.local and help.paris.local websites. This can also be checked via Subject Alternative Name as well." | oh
pause

Write-Host "# Aspect - CA: Subject Alternative Name" -ForeGroundColor Green
echo "Subject Alternative Name should be present on web-srv for www.paris.local, help.paris.local, external.paris.local websites. This condition is only valid for these websites in paris.local, and not any other websites.

[MANUAL] From DC1, access microsoft edge. Navigate to https://external.paris.local and click on the `"lock`" icon next to the `"https`" scheme. If done correctly, `"Connection is Secure`" should appear with `"Certificate (Valid)`". Click on Certificate, under Details tab, scroll to `"Subject Alternative Name`". The following records should exists:

DNS Name=help.paris.local
DNS Name=www.paris.local
DNS Name=external.paris.local" | oh
pause

Write-Host "# Aspect - IIS: Iinstalled on WEB-SRV" -ForeGroundColor Green
echo "Run the following on Web-SRV: Get-WindowsFeature -ComputerName `"web-srv.paris.local`" | Where-Object { `$_.Name -eq `"Web-Server`" -and `$_.Installed }" | oh
Get-WindowsFeature -ComputerName "web-srv.paris.local" | Where-Object { $_.Name -eq "Web-Server" -and $_.Installed } | oh
pause

Write-Host "# Aspect - IIS: Virtual Hosts" -ForeGroundColor Green
echo "On WIN-CLIENT1, using tech13 user, use microsot edge to:

Access https://www.paris.local, and it should show `"This is internal WSC2024`". 

Access https://help.paris.local, it should should `"This is Internal WSC2024 Help`". " | oh
pause

Write-Host "# Aspect - IIS: No certificate error when accessed using HTTPS" -ForeGroundColor Green
echo "On WIN-CLIENT1 using tech13 user, when accessing https://www.paris.local, no certificate error was shown." | oh
pause