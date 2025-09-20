Write-Host "# === Sub Criterion: file-srv.paris.local ===`r`n" -ForeGroundColor Green
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

Write-Host "# Aspect - RemoteApp" -ForeGroundColor Green
echo "From the Paris network WIN-CLIENT1, access https://app.paris.local/Rdweb. [MANUAL] On WIN-CLIENT1, access https://app.paris.local/Rdweb, using PARIS/Administrator credentials to login. It should show the remote apps available (notepad.exe). HTTPS error is accepted for this domain" | oh
pause

Write-Host "# Aspect - DFS: \\paris.local\CSDrive\Common Share configured" -ForeGroundColor Green
echo "Login using mkt13 on WIN-CLIENT1. Click on `"File Explorer`" > `"This PC`". `"Common Share`" Should be mounted as Drive Z under network locations. Login using hr13 on CLIENT1. Click on `"File Explorer`". `"Common Share`" Should not be mounted." | oh
pause

Write-Host "# Aspect - DFS: \\paris.local\CSDrive\MKT Mounting Configured" -ForeGroundColor Green
echo "Login using mkt13 on WIN-CLIENT1. Click on `"File Explorer`". `"MKT`" Should be mounted as Drive X under network locations" | oh
pause

Write-Host "# Aspect - DFS: \\paris.local\CSDrive\SALES Mounting Configured" -ForeGroundColor Green
echo "Login using sales13 on WIN-CLIENT1. Click on `"File Explorer`". `"SALES`" Should be mounted as Drive X under network locations" | oh
pause

Write-Host "# Aspect - DFS: \\paris.local\CSDrive\HR Mounting Configured" -ForeGroundColor Green
echo "Login using hr13 on WIN-CLIENT1. Click on `"File Explorer`". `"HR`" Should be mounted as Drive X under network locations" | oh
pause

Write-Host "# Aspect - DFS: \\paris.local\CSDrive\TECH Mounting Configured" -ForeGroundColor Green
echo "Login using tech13 on WIN-CLIENT1. Click on `"File Explorer`". `"TECH`" Should be mounted as Drive X under network locations" | oh
pause

Write-Host "# Aspect - DFS: Personal Share (Quota)" -ForeGroundColor Green
echo "Login using tech13 on WIN-CLIENT1. Open powershell, type the following:" | oh
echo "fsutil file createnew T:\smalllfile.txt 1048575" | oh
echo "fsutil file createnew T:\largefile.txt 52428800" | oh
pause

Write-Host "# Aspect - DFS: Personal Share (Executable File Restriction)" -ForeGroundColor Green
echo "Login using tech13 on WIN-CLIENT1. Open powershell, type the following:" | oh
echo "Copy-Item `"C:\Windows\system32\ActiveHours.png`" -Destination `"T:\ `"" | oh
echo "Copy-Item `"C:\Windows\system32\calc.exe`" -Destination `"T:\ `"" | oh
echo "Get-ChildItem `"T:\`"" | oh
pause

Write-Host "# Aspect - DFS Replication" -ForeGroundColor Green
echo "`"WSC2024`" | Out-File -FilePath \\paris.local\CSDrive\CommonShare\sync.txt" | oh
"WSC2024" | Out-File -FilePath \\paris.local\CSDrive\CommonShare\sync.txt| oh
pause