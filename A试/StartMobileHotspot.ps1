<#
开启Windows移动热点（对应截图设置界面开关）
兼容PS5.1，不需要安装PowerShell7
#>

# 移动热点注册表路径
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters"
# 1=开启 0=关闭
Set-ItemProperty -Path $regPath -Name "EnableInternetConnectionSharing" -Value 1 -Force

# 重启SharedAccess服务使热点生效，管理员权限！
Restart-Service SharedAccess -Force

Write-Host "✅已执行开启移动热点，请检查系统【移动热点】设置页面"
