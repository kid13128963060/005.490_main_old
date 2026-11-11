;V1.2 整合 dnconsole 启动模拟器
#include <Excel.au3>
#include <Array.au3>

;配置区
Local $sAdb = "C:\leidian\LDPlayer9\adb.exe"
Local $sWorkDir = "C:\leidian\LDPlayer9"
Local $sDnConsole = "C:\leidian\LDPlayer9\dnplayer.exe"
Local $sExcelFile = "F:\自动同步_只增加\设备识别\设备识别.xls"

;设备识别
Local $oExcel = _Excel_Open(False)
If @error Then
    MsgBox(0,"错误","Excel COM启动失败")
    Exit
EndIf

Local $oBook = _Excel_BookOpen($oExcel, $sExcelFile, True, False)
If @error Then
    MsgBox(0,"错误","打开文件失败")
    _Excel_Close($oExcel)
    Exit
EndIf

; 读取B2 + 去除首尾空格，避免匹配失败
Local $sB2 = _Excel_RangeRead($oBook, Default, "B2")
$sB2 = StringStripWS($sB2, 3)

; 释放COM
_Excel_BookClose($oBook)
_Excel_Close($oExcel)

;数据区
; 声明定义点击数组：3个点，每个点x,y
Local $sDeviceName = $sB2
Local $tap_points[3][2]

If $sDeviceName = "工脑模拟器" Then
    $tap_points[0][0] = 169
    $tap_points[0][1] = 632   ; 第一步：打开自动按键点击
    $tap_points[1][0] = 945
    $tap_points[1][1] = 1815  ; 第二步：点击我的
    $tap_points[2][0] = 200
    $tap_points[2][1] = 255   ; 第三步：点击春眠
ElseIf $sDeviceName = "家脑模拟器" Then
    $tap_points[0][0] = 0
    $tap_points[0][1] = 0   ; 第一步：打开自动按键点击
    $tap_points[1][0] = 0
    $tap_points[1][1] = 0  ; 第二步：点击我的
    $tap_points[2][0] = 0
    $tap_points[2][1] = 0   ; 第三步：点击春眠
Else
    MsgBox(0,"提示","未知设备：" & $sDeviceName)
    Exit
EndIf

;_ArrayDisplay($tap_points, "tap_points 坐标数组")

; 滑动一维数组 [x1,y1,x2,y2,时长]
Local $swipe_param[5]
$swipe_param[0] = 500
$swipe_param[1] = 1400
$swipe_param[2] = 500
$swipe_param[3] = 600
$swipe_param[4] = 300

; ========== 使用dnconsole启动0号模拟器 ==========
Run($sDnConsole & " launch --index 0", $sWorkDir, @SW_HIDE)

; 等待雷电模拟器窗口出现
If WinWait("雷电模拟器", "", 5) = 0 Then
    MsgBox(0,"错误","雷电模拟器启动超时")
    Exit
EndIf
WinActivate("雷电模拟器")
Sleep(3000) ; 等待桌面加载完成

