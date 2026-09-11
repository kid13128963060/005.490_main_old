#功能说明远程覆盖本地
Set-Location $PSScriptRoot
Write-Host "===== 开始拉取远程并覆盖本地main =====" -ForegroundColor Cyan

git fetch origin
if ($LASTEXITCODE -ne 0) {
    Write-Error "git fetch 失败，请检查网络/仓库权限"
    exit 1
}


git reset --hard origin/main
if ($LASTEXITCODE -ne 0) {
    Write-Error "强制重置覆盖失败"
    exit 1
}

git clean -fd  # 不需要清空未跟踪文件就注释掉这一行

Write-Host "✅ 本地已被远程 origin/main 覆盖完成" -ForegroundColor Green
