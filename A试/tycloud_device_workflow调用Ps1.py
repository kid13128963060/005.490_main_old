# -*- coding: utf-8 -*-
# version: V1.1
# 更新记录
# V1.0 当前脚本仅负责执行内嵌的云端覆盖本地配置PowerShell脚本
# V1.1 修改PS脚本逻辑：移除while循环实时监控，改为采集两份哈希表，
# 云盘启动前生成哈希表1，启动云盘等待同步后生成哈希表2，对比两个哈希表；
# 检测到文件变化就执行配置覆盖操作2，完成后脚本退出。

import subprocess


def main():
    print("\n---------- 开始执行内嵌PowerShell：云端覆盖本地配置 ----------")
    ps_script_text = r'''
<#
版本：V1.2
功能：云端覆盖本地配置脚本
说明：
1.云盘启动前采集目录文件大小存入哈希表1
2.启动天翼云盘程序，等待同步时间
3.采集云盘启动后目录文件大小存入哈希表2
4.对比哈希表2与哈希表1，检测到文件变更则执行配置覆盖操作，执行一次后退出脚本。
#>

# PowerShell 脚本：云端覆盖本地配置
# 配置：云盘本地同步目录
$SyncFolder = "E:\备份盘"

# =========哈希表1：启动天翼云盘【之前】递归获取所有文件，存储初始文件大小=========
$InitialFileSizes = @{}
Get-ChildItem -Path $SyncFolder -Recurse -File | ForEach-Object {
    $InitialFileSizes[$_.FullName] = $_.Length  # 文件大小（字节）
}
Write-Host "哈希表1采集完成（云盘启动前）" -ForegroundColor Green

# =========启动天翼云盘程序=========
Start-Process -FilePath "C:\Program Files\ecloud\eCloud.exe"
Write-Host "已启动eCloud云盘程序，等待云盘同步……" -ForegroundColor Green

# 等待云盘同步完成时间，可按需调整
Start-Sleep -Seconds 40

# =========哈希表2：启动天翼云盘【之后】递归获取所有文件大小=========
$AfterCloudStartSizes = @{}
Get-ChildItem -Path $SyncFolder -Recurse -File | ForEach-Object {
    $AfterCloudStartSizes[$_.FullName] = $_.Length
}
Write-Host "哈希表2采集完成（云盘启动后），准备对比哈希表2与哈希表1" -ForegroundColor Green

# =========操作3：哈希表2与哈希表1进行对比=========
$hasChange = $false
#遍历哈希表1全部文件
foreach ($filePath in $InitialFileSizes.Keys) {
    $size1 = $InitialFileSizes[$filePath]
    # 如果文件在哈希表2存在，取出大小对比
    if ($AfterCloudStartSizes.ContainsKey($filePath)) {
        $size2 = $AfterCloudStartSizes[$filePath]
        if ($size1 -ne $size2) {
            Write-Host "检测到文件发生变化：$filePath" -ForegroundColor Yellow
            Write-Host "  大小变化：$size1 → $size2 字节" -ForegroundColor Yellow
            $hasChange = $true
            break
        }
    }
}

# 操作3如果检测到变化就执行操作2
if ($hasChange) {
    Write-Host "哈希对比发现文件变更，触发复制命令..." -ForegroundColor Cyan

    # =========操作2：若检测到变化，触发批处理操作=========
    # 关闭多个应用程序
    Stop-Process -Name "Listary", "i_view64", "Ditto" -Force
    Start-Sleep -Seconds 10

    #云端配置恢复到本地
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\PathHistory.json" -Destination "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\Preferences.json" -Destination "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\SearchHistory.json" -Destination "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_238_irfanview!2_设置备份\i_view64.ini" -Destination "C:\Users\Administrator\AppData\Roaming\IrfanView\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_211_Ditto_备份\005_211_Ditto_数据备份.db" -Destination "C:\Users\Administrator\AppData\Roaming\Ditto\" -Recurse -Force

    #启动关闭的应用
    Start-Process -FilePath "C:\Program Files\Listary\Listary.exe"
    Start-Process -FilePath "C:\Program Files\Ditto\Ditto.exe"
    New-Item -Path "E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\同步成功提示文件.txt" -Force

}
else {
    Write-Host "哈希对比完成：未检测到任何文件变化，不执行配置覆盖操作" -ForegroundColor Gray
}

Write-Host "执行云端覆盖本地配置操作ok"
'''

    # 方式2 powershell -Command 执行脚本字符串，绕过执行策略
    ps_result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script_text],
        capture_output=True,
        text=True,
        errors="replace"
    )
    print("=====PowerShell脚本标准输出=====")
    print(ps_result.stdout)
    print("=====PowerShell脚本错误输出=====")
    print(ps_result.stderr)
    print(f"PowerShell脚本返回码：{ps_result.returncode}")
    print("----------内嵌PowerShell脚本执行完毕----------")


if __name__ == "__main__":
    main()
