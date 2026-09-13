<#
.SYNOPSIS
单人仓库Git回滚脚本，恢复到【回退至 指定历史分支】
⚠️警告：清空本地未提交改动 + 强制覆盖远程main分支，仅单人仓库使用
#>

# 定义提交哈希常量
$TARGET_COMMIT_HASH = "661a70c4b1da7b45eac7cdda7120f516630bff0a"

git fetch origin
git reset --hard $TARGET_COMMIT_HASH
git push origin main --force

Write-Host "✅ 已回退至 指定历史分支，并强制推送远程main"