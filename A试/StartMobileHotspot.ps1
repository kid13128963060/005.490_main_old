# StartMobileHotspot.ps1 完整版（Windows PowerShell5.1专用）
# 预加载全部WinRT类型，解决找不到类型报错
[Windows.System.UserProfile.LockScreen, Windows.System.UserProfile, ContentType = WindowsRuntime] | Out-Null
[Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult, Windows.Networking.NetworkOperators, ContentType = WindowsRuntime] | Out-Null
[Windows.Networking.Connectivity.NetworkInformation, Windows.Networking.Connectivity, ContentType = WindowsRuntime] | Out-Null
[Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager, Windows.Networking.NetworkOperators, ContentType = WindowsRuntime] | Out-Null

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 }).MakeGenericMethod([Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult])

$connectionProfile = [Windows.Networking.Connectivity.NetworkInformation]::GetInternetConnectionProfile()
if (-not $connectionProfile) {
    Write-Output "未找到可用的互联网连接"
    exit
}
$tetheringManager = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager]::CreateFromConnectionProfile($connectionProfile)
$op = $tetheringManager.StartTetheringAsync()
$res = $asTask.Invoke($null, @($op)).Result
if ($res.Status -eq 'Success') {
    Write-Output "移动热点已成功开启"
}
else {
    Write-Output "开启失败：$($res.Status)"
}
