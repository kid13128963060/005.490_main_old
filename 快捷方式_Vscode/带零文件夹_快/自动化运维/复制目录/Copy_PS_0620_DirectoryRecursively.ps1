# 设置源文件夹和目标文件夹路径
$source = "E:\备份盘\8000-大文件夹\009-备份文件夹-自\005-209-Listary!2-设置\自定义设置"
$destination = "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\"

# 检查源文件夹是否存在
if (-not (Test-Path -Path $source -PathType Container)) {
    Write-Error "源文件夹不存在: $source"
    exit 1
}

# 检查目标文件夹是否存在，如果不存在则创建
if (-not (Test-Path -Path $destination -PathType Container)) {
    New-Item -ItemType Directory -Path $destination | Out-Null
    Write-Host "已创建目标文件夹: $destination"
}

try {
    # 递归复制目录及文件，保留文件结构
    Copy-Item -Path "$source\*" -Destination $destination -Recurse -Force -ErrorAction Stop
    Write-Host "复制完成！源目录: $source 到 目标目录: $destination"
}
catch {
    Write-Error "复制过程中发生错误: $_"
    exit 2
}