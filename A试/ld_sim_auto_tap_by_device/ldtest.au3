;V1.7 ok 
#include <Excel.au3>
#include <Array.au3>
;====================模式配置：1=测试模式  2=正常运行模式【默认2】====================
Local $iRunMode = 2
;时间选择
;===================================================================================

;配置区

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
        $nWaitMs = 75000
    ElseIf $nWaitLoad = 2 Then
        $nWaitMs = 65000
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
    $tap_normal[0][0] = 169
    $tap_normal[0][1] = 632   ; 第一步：打开自动按键点击
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
    $tap_normal[6][0] = 540
    $tap_normal[6][1] = 1425    
ElseIf $sDeviceName = "家脑模拟器" Then
    ;MsgBox(0,"提示", "读到的设备名：" & $sB2)
    $sAdb = "E:\Program Files\leidian\LDPlayer9\adb.exe"
    $sWorkDir = "E:\Program Files\leidian\LDPlayer9"
    $sDnConsole = '"E:\Program Files\leidian\LDPlayer9\dnconsole.exe"'
    Local $nWaitLoad = 2
    If $nWaitLoad = 1 Then
       $nWaitMs = 13700
    ElseIf $nWaitLoad = 2 Then
        $nWaitMs = 15000
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
    $tap_test[6][0] = 534
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
    $tap_normal[6][0] = 0
    $tap_normal[6][1] = 0    ; 第七步：再点击登录

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

; ========== 使用dnconsole启动0号模拟器 ==========
Local $launchCmd = $sDnConsole & " launch --index 0"
; MsgBox(0,"调试：启动命令", $launchCmd)

Run($sDnConsole & " launch --index 0", $sWorkDir, @SW_HIDE)
;Exit         ; 退出，返回码0
Sleep($nWaitMs)

; 等待雷电模拟器启动
If WinWait("雷电模拟器", "", 80) = 0 Then
    MsgBox(0,"错误","雷电模拟器启动超时")
    Exit
EndIf
WinActivate("雷电模拟器")
Sleep(3000) ; 等待桌面加载完成

; 循环点击，增加坐标0跳过逻辑
For $i = 0 To UBound($tap_points) - 1
    Local $x = $tap_points[$i][0]
    Local $y = $tap_points[$i][1]
    If $x = 0 And $y = 0 Then
        ConsoleWrite("第" & $i & "组坐标全0，跳过点击" & @CRLF)
        ContinueLoop
    EndIf
    RunWait($sAdb & " shell input tap " & $x & " " & $y, $sWorkDir, @SW_HIDE)
    Sleep(2600)
Next


; MsgBox(0,"完成","脚本全部动作执行完毕")
