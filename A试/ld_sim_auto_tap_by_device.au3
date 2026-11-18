;V1.9 ok
#include <Excel.au3>
#include <Array.au3>
;====================模式配置：1=测试模式  2=正常运行模式【默认2】====================
Local $iRunMode = 2
;===================================================================================

;配置区
local $AutoItExe,$sSubFile
$AutoItExe="C:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe"
Local $sSubFile = @ScriptDir & "\emulator_ocr_popup_click.au3"
; ====================== 顶部配置区（可自行修改，24小时制，HH:MM） ======================
Local $sTimeStart1 = "00:01"   ; 00:01 分支1起始时间 06:01
Local $sTimeEnd1   = "00:15"   ; 00:15 分支1结束时间 07:15
Local $sTimeStart2 = "00:16"   ; 00:16 分支2起始时间
Local $sTimeEnd2   = "00:30"   ; 00:30分支2结束时间

;~ Local $sTimeStart1 = "06:01"   ; 00:01 分支1起始时间 06:01
;~ Local $sTimeEnd1   = "07:15"   ; 00:15 分支1结束时间 07:15
;~ Local $sTimeStart2 = "06:01"   ; 00:16 分支2起始时间
;~ Local $sTimeEnd2   = "07:15"   ; 00:30分支2结束时间

; 函数：判断当前时间是否在 [sStart, sEnd) 区间内，左闭右开，避免交界重复执行
Func TimeIsBetween($sStart, $sEnd)
    Local $sNow = @HOUR & ":" & @MIN
    Local $aNow  = StringSplit($sNow,  ":")
    Local $aS    = StringSplit($sStart,":")
    Local $aE    = StringSplit($sEnd,  ":")
    Local $iNow  = $aNow[1]*60 + $aNow[2]
    Local $iS    = $aS[1]*60   + $aS[2]
    Local $iE    = $aE[1]*60   + $aE[2]
    Return ($iNow >= $iS And $iNow < $iE)
EndFunc   ;==>TimeIsBetween


;设备识别
Local $sExcelFile = "F:\自动同步_只增加\设备识别\设备识别.xls"
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

; 读取B2
Local $sB2 = _Excel_RangeRead($oBook, Default, "B2")
; MsgBox(0,"提示", "读到的设备名：" & $sB2)

; 释放COM
_Excel_BookClose($oBook)
_Excel_Close($oExcel)


;数据区
; 声明定义点击数组：3个点，每个点x,y


;数据区
Local $tap_test[7][2]     ;测试模式数组
Local $tap_normal[7][2]   ;正常运行模式数组
Local $tap_points[7][2]   ;实际执行数组
Local $tap_points1[2][2]  ;备用数组保留
Local $sAdb, $sWorkDir, $sDnConsole, $nWaitMs

$sDeviceName = $sB2
If $sDeviceName = "工脑模拟器" Then
     $sAdb = "C:\leidian\LDPlayer9\adb.exe"
     $sWorkDir = "C:\leidian\LDPlayer9"
     $sDnConsole = "C:\leidian\LDPlayer9\dnconsole.exe" ;dnplayer
    Local $nWaitLoad = 2
    If $nWaitLoad = 1 Then
        $nWaitMs = 66000
    ElseIf $nWaitLoad = 2 Then
        $nWaitMs = 68000
    Else
    ;兜底默认值，防止变量为空
    $nWaitMs = 5000
    ConsoleWrite("警告：$nWaitLoad 不是1/2，使用默认等待时间" & @CRLF)
    EndIf
;----------工脑模拟器 测试模式点位----------
    $tap_test[0][0] = 169  
    $tap_test[0][1] = 632   ; 第一步：打开自动按键点击
    $tap_test[1][0] = 945
    $tap_test[1][1] = 1815  ; 第二步：点击我的
    $tap_test[2][0] = 200
    $tap_test[2][1] = 255   ; 第三步：点击春眠
    $tap_test[3][0] = 540
    $tap_test[3][1] = 1450  ;第三步：点退出登录
    $tap_test[4][0] = 540
    $tap_test[4][1] = 1899
    $tap_test[5][0] = 168
    $tap_test[5][1] = 1775
    $tap_test[6][0] = 0
    $tap_test[6][1] = 0
    ;----------工脑模拟器 正常模式点位----------
    $tap_normal[0][0] = 170   ;170
    $tap_normal[0][1] = 630   ;630 第一步：打开自动按键点击
    $tap_normal[1][0] = 945
    $tap_normal[1][1] = 1815  ; 第二步：点击我的
    $tap_normal[2][0] = 200
    $tap_normal[2][1] = 255   ; 第三步：点击春眠
    $tap_normal[3][0] = 540
    $tap_normal[3][1] = 1450  ;第三步：点退出登录
    $tap_normal[4][0] = 540
    $tap_normal[4][1] = 1899
    $tap_normal[5][0] = 168
    $tap_normal[5][1] = 1775
    $tap_normal[6][0] = 540  ;540
    $tap_normal[6][1] = 1400 ;1400 第七步：再点击登录
ElseIf $sDeviceName = "家脑模拟器" Then
    ;MsgBox(0,"提示", "读到的设备名：" & $sB2)
    $sAdb = "E:\Program Files\leidian\LDPlayer9\adb.exe"
    $sWorkDir = "E:\Program Files\leidian\LDPlayer9"
    $sDnConsole = '"E:\Program Files\leidian\LDPlayer9\dnconsole.exe"'
    Local $nWaitLoad = 2
    If $nWaitLoad = 1 Then
       $nWaitMs = 13700
    ElseIf $nWaitLoad = 2 Then
        $nWaitMs = 60000
    Else
    ;兜底默认值，防止变量为空
    $nWaitMs = 5000
    ConsoleWrite("警告：$nWaitLoad 不是1/2，使用默认等待时间" & @CRLF)
    EndIf

    ;----------家脑模拟器 测试模式点位----------
    $tap_test[0][0] = 175
    $tap_test[0][1] = 635   ; 第一步：打开自动按键点击
    $tap_test[1][0] = 943
    $tap_test[1][1] = 1815  ; 第二步：点击我的
    $tap_test[2][0] = 430
    $tap_test[2][1] = 230  ; 第三步：点击春眠
    $tap_test[3][0] = 560
    $tap_test[3][1] = 1475  ; 第四步：点击账号登录
    $tap_test[4][0] = 510
    $tap_test[4][1] = 1890    ; 第五步：点击登录
    $tap_test[5][0] = 170
    $tap_test[5][1] = 1774    ; 第六步：勾选同意
    $tap_test[6][0] = 530
    $tap_test[6][1] = 1430    ; 第七步：再点击登录

    ;----------家脑模拟器 正常模式点位----------
    $tap_normal[0][0] = 175
    $tap_normal[0][1] = 635   ; 第一步：打开自动按键点击
    $tap_normal[1][0] = 943
    $tap_normal[1][1] = 1815  ; 第二步：点击我的
    $tap_normal[2][0] = 430
    $tap_normal[2][1] = 230  ; 第三步：点击春眠
    $tap_normal[3][0] = 560
    $tap_normal[3][1] = 1475  ; 第四步：点击账号登录
    $tap_normal[4][0] = 510
    $tap_normal[4][1] = 1890    ; 第五步：点击登录
    $tap_normal[5][0] = 170
    $tap_normal[5][1] = 1774    ; 第六步：勾选同意
    $tap_normal[6][0] = 530
    $tap_normal[6][1] = 1430    ; 第七步：再点击登录

Else
    MsgBox(0,"提示","未知设备：" & $sDeviceName)
    Exit
EndIf


;_ArrayDisplay($tap_points, "tap_points 坐标数组")

;根据模式复制数据到执行数组tap_points
If $iRunMode = 1 Then
    ;MsgBox(0,"模式提示","当前【测试模式】")
    For $i = 0 To 6
        $tap_points[$i][0] = $tap_test[$i][0]
        $tap_points[$i][1] = $tap_test[$i][1]
    Next
ElseIf $iRunMode = 2 Then
    ;MsgBox(0,"模式提示","当前【正常运行模式】")
    For $i = 0 To 6
        $tap_points[$i][0] = $tap_normal[$i][0]
        $tap_points[$i][1] = $tap_normal[$i][1]
    Next
Else
    MsgBox(0,"错误","模式变量只能填写1或者2")
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

If $sDeviceName = "工脑模拟器" Then
    ; 时间分流判断
    If TimeIsBetween($sTimeStart1, $sTimeEnd1) Then
        ConsoleWrite("【工脑模拟器】当前时间命中时段1 → 工脑模拟器-0" & @CRLF)
        $sDeviceName = "工脑模拟器-0"
    ElseIf TimeIsBetween($sTimeStart2, $sTimeEnd2) Then
        ConsoleWrite("【工脑模拟器】当前时间命中时段2 → 工脑模拟器-1" & @CRLF)
        $sDeviceName = "工脑模拟器-1"
    Else
        ConsoleWrite("【工脑模拟器】当前时间不在指定时段" & @CRLF)
    EndIf

    ; 根据标记名称启动
    Switch $sDeviceName
        Case "工脑模拟器-0"
            Local $launchCmd = $sDnConsole & " launch --index 0"
            Run($sDnConsole & " launch --index 0", $sWorkDir, @SW_HIDE)
            Sleep($nWaitMs)
        Case "工脑模拟器-1"
            Local $launchCmd = $sDnConsole & " launch --index 1"
            Run($sDnConsole & " launch --index 1", $sWorkDir, @SW_HIDE)
            Sleep($nWaitMs)
        Case Else
            ConsoleWrite("【工脑模拟器】无有效标记，跳过启动" & @CRLF)
    EndSwitch

ElseIf $sDeviceName = "家脑模拟器" Then
    ConsoleWrite("【家脑模拟器】固定启动索引0" & @CRLF)
    Local $launchCmd = $sDnConsole & " launch --index 0"
    Run($sDnConsole & " launch --index 0", $sWorkDir, @SW_HIDE)
    Sleep($nWaitMs)

Else
    MsgBox(0,"提示","未知设备：" & $sDeviceName)
    Exit
EndIf



; 等待雷电模拟器启动
If WinWait("雷电模拟器", "", 80) = 0 Then
    MsgBox(0,"错误","雷电模拟器启动超时")
    Exit
EndIf
WinActivate("雷电模拟器")
Sleep(3000) ; 等待桌面加载完成

;等待知道了弹窗出现点击
;~ ConsoleWrite("子脚本完整路径：" & $sSubFile & @CRLF)
;~ RunWait('"' & @AutoItExe & '" /AutoIt3ExecuteScript "' & $sSubFile & '"', "", @SW_HIDE)
;~ MsgBox(0,"已点击自动按","不知是否成功")


; 循环点击，增加坐标0跳过逻辑
;~ For $i = 0 To UBound($tap_points) - 1
;~     Local $x = $tap_points[$i][0]
;~     Local $y = $tap_points[$i][1]
;~     If $x = 0 And $y = 0 Then
;~         ConsoleWrite("第" & $i & "组坐标全0，跳过点击" & @CRLF)
;~         ContinueLoop
;~     EndIf
;~     RunWait($sAdb & " shell input tap " & $x & " " & $y, $sWorkDir, @SW_HIDE)
;~     If $i = 0 Then
;~         Sleep(9000) ; 第一步单独等待，你可以改这个数值
;~     Else
;~         Sleep(3200) ; 其余步骤默认等待
;~     EndIf
;~ Next



; MsgBox(0,"完成","脚本全部动作执行完毕")
