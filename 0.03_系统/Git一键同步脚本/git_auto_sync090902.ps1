
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

<#
Git一键同步脚本
使用前：VSCode务必 Ctrl+S 将文件保存到磁盘！脚本读取磁盘文件，不能直接保存编辑器缓存
#>
$CommitPrefix = "自动同步09090203"

Write-Host "==== Git一键同步开始 ====" -ForegroundColor Cyan
Write-Host "确认 VSCode 已保存全部修改到磁盘" -ForegroundColor Yellow

# 1.拉取远程更新
Write-Host "`n[1/4] git pull 拉取远程代码"
git pull
if ($LASTEXITCODE -ne 0) {
    Write-Host "git pull failed; resolve conflicts before continuing" -ForegroundColor Red
    pause
    exit 1
}

# 2.全部加入暂存
Write-Host "`n[2/4] git add . 添加全部改动"
git add .

# 3.提交，自动使用当前时间作为提交备注
$commitMsg = "$CommitPrefix`_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "`n[3/4] git commit -m ""$commitMsg"""
git commit -m "$commitMsg"

# 判断：没有改动会commit返回1，属于正常，不报错终止
if ($LASTEXITCODE -ne 0) {
    Write-Host "No changes detected; nothing to commit or push" -ForegroundColor Gray
    Write-Host "==== Script finished ===="
    pause
    exit 0
}

#4.推送远程
Write-Host "`n[4/4] git push 推送至远程仓库"
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "git push failed" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Sync completed" -ForegroundColor Green
Write-Host "==== Git sync finished ===="
#pause
