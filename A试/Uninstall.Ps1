Write-Host "正在卸载 有道词典..." -ForegroundColor Yellow
$regItem = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall" -ErrorAction SilentlyContinue |
Where-Object { $_.GetValue("DisplayName") -eq "网易有道翻译" } |
Select-Object -First 1
if ($regItem) {
    $uninstPath = $regItem.GetValue("UninstallString") -replace '^"(.+?)".*', '$1'
    Write-Host "卸载程序路径：$uninstPath"
    Start-Process -FilePath $uninstPath -ArgumentList "/S" -Wait -NoNewWindow
}
else {
    Write-Host "未找到网易有道翻译注册表项" -ForegroundColor Red
}
