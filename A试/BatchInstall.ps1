<#
批量静默安装本地软件
特点：顺序执行、等待安装结束、打印简单提示
#>
Write-Host "===== 开始批量安装程序 =====" -ForegroundColor Cyan

# ========== 1. MSI 安装包示例 ==========
Write-Host "正在安装 Python MSI..." -ForegroundColor Yellow
#Start-Process msiexec -ArgumentList "/i F:\带零文件夹\005_210_电脑软件\必装软件\python-3.12.4-amd64.msi /quiet /norestart" -Wait -NoNewWindow

# ========== 2. EXE 安装包示例 ==========
Write-Host "正在安装 7-Zip..." -ForegroundColor Yellow
Start-Process -FilePath "F:\带零文件夹\005_210_电脑软件\必装软件\7z2408-x64.exe" -ArgumentList "/S" -Wait -NoNewWindow

Write-Host "正在安装 有道词典..." -ForegroundColor Yellow
Start-Process -FilePath "F:\带零文件夹\005_210_电脑软件\必装软件\YoudaoDict.exe" -ArgumentList "/S" -Wait -NoNewWindow -PassThru

Write-Host "正在安装 极速PDF..." -ForegroundColor Yellow
Start-Process -FilePath "F:\带零文件夹\005_210_电脑软件\必装软件\极速PDF.exe" -ArgumentList "/S" -Wait -NoNewWindow -PassThru

Write-Host "正在安装 搜狗五笔输入法..." -ForegroundColor Yellow
Start-Process -FilePath "F:\带零文件夹\005_210_电脑软件\必装软件\搜狗五笔输入法.exe" -ArgumentList "/S" -Wait -NoNewWindow -PassThru

Write-Host "正在安装 irFanview..." -ForegroundColor Yellow
Start-Process -FilePath "F:\带零文件夹\005_210_电脑软件\必装软件\irFanview.exe" -ArgumentList "/silent /desktop=1 /thumbs=1 /group=1 /allusers=0" -Wait -NoNewWindow -PassThru

<#
Write-Host "正在安装 微信..." -ForegroundColor Yellow
Start-Process -FilePath "F:\带零文件夹\005_210_电脑软件\必装软件\WeChatSetup.exe" -ArgumentList "/S" -Wait -NoNewWindow

Write-Host "===== 全部安装任务执行完毕 =====" -ForegroundColor Green
Write-Host "建议重启电脑以完成配置" -ForegroundColor DarkYellow
#>