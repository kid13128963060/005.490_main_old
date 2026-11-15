; 雷电ADB路径、设备标识
Global $adbPath = "E:\Program Files\leidian\LDPlayer9\adb.exe"
Global $devId = "emulator-5554"
Global $snapPath = "E:\下载\test.png"
Global $btnX = 540
Global $btnY = 720

ConsoleWrite("=== 下线弹窗自动监控启动 ===" & @CRLF)

While 1
    ; ADB管道截图输出到文件
    RunWait('"' & $adbPath & '" -s ' & $devId & ' exec-out screencap -p > "' & $snapPath & '"', "", @SW_HIDE)
    
    ; 找图：你把这张test.png保存为模板图，命名 template.png，放在同目录
    Local $hWnd = 0
    Local $pos = ImageSearch($snapPath, 0, 0, 1080, 1920, "template.png", 0.8)
    If @error = 0 Then
        ConsoleWrite("【检测到下线弹窗】执行点击知道了" & @CRLF)
        Run('"' & $adbPath & '" -s ' & $devId & ' shell input tap ' & $btnX & " " & $btnY, "", @SW_HIDE)
        Sleep(2000)
    Else
        ConsoleWrite("无弹窗，继续监控" & @CRLF)
    EndIf
    Sleep(1500)
WEnd

Func ImageSearch($imgPath, $x1, $y1, $x2, $y2, $template, $tolerance)
    ; 依赖AutoIt ImageSearch UDF，如果你没有，我给你替换方案
    Return 0
EndFunc
