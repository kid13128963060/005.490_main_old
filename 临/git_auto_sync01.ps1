
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

<#
Git一键同步脚本
使用前：VSCode务必 Ctrl+S 将文件保存到磁盘！脚本读取磁盘文件，不能直接保存编辑器缓存
#>
# 常量定义：修改提交备注前缀只改这里即可
#$CommitPrefix = "家脑_测试自动同步090906"

Write-Host "==== Git一键同步开始 ====" -ForegroundColor Cyan
Write-Host "确认 VSCode 已保存全部修改到磁盘" -ForegroundColor Yellow


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
