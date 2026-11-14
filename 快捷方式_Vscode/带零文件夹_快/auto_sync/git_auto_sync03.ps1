
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

<#
Git一键同步脚本
使用前：VSCode务必 Ctrl+S 将文件保存到磁盘！脚本读取磁盘文件，不能直接保存编辑器缓存
#>
# 常量定义：修改提交备注前缀只改这里即可
#$CommitPrefix = "家脑_测试自动同步090906"
$CommitPrefix = "工脑_恢复前09092302"

Write-Host "==== Git一键同步开始 ====" -ForegroundColor Cyan
Write-Host "确认 VSCode 已保存全部修改到磁盘" -ForegroundColor Yellow


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
