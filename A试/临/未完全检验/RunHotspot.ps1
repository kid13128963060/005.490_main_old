# RunHotspot.ps1 完整新版代码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 获取当前RunHotspot.ps1所在文件夹
$scriptDir = $PSScriptRoot
# 拼接同目录下的热点脚本
$scriptPath = Join-Path -Path $scriptDir -ChildPath "StartMobileHotspot.ps1"

Write-Output "目标脚本路径：$scriptPath"

# 校验文件
if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
    Write-Error "【错误】找不到文件：$scriptPath"
    Read-Host "按 Enter 继续..."
    exit 1
}

# 执行热点脚本
& $scriptPath
