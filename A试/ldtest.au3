Local $sAdb = "C:\leidian\LDPlayer9\adb.exe"
Local $sWorkDir = "C:\leidian\LDPlayer9"

; 等待雷电模拟器启动
If WinWait("雷电模拟器", "", 15) = 0 Then
    MsgBox(0,"错误","雷电模拟器启动超时")
    Exit
EndIf
WinActivate("雷电模拟器")
Sleep(3000) ; 等待桌面加载完成

; 滑动一维数组 [x1,y1,x2,y2,时长]
Local $swipe_param[5]
$swipe_param[0] = 500
$swipe_param[1] = 1400
$swipe_param[2] = 500
$swipe_param[3] = 600
$swipe_param[4] = 300

RunWait($sAdb & " shell input swipe " & $swipe_param[0] & " " & $swipe_param[1] & " " & $swipe_param[2] & " " & $swipe_param[3] & " " & $swipe_param[4], $sWorkDir, @SW_HIDE)


