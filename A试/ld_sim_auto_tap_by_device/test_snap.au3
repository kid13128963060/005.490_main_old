#include <Excel.au3>
#include <Array.au3>; ==============================================
; ADB 雷电模拟器截图 + pull拉取图片
; 设备：emulator-5554
; ==============================================
Local $sAdbPath = "c:\leidian\LDPlayer9\adb.exe"
Local $sDevice = "emulator-5554"
Local $sRemoteImg = "/sdcard/test.png"
Local $sLocalImg = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\ld_sim_auto_tap_by_device\test.png"
;设备识别
Local $sExcelFile = "F:\自动同步_只增加\设备识别\设备识别.xls"
Local $oExcel = _Excel_Open(False)
If @error Then
    MsgBox(0,"错误","Excel COM启动失败")
    Exit
EndIf

; 读取B2
Local $sB2 = _Excel_RangeRead($oBook, Default, "B2")
; MsgBox(0,"提示", "读到的设备名：" & $sB2)

; 释放COM
_Excel_BookClose($oBook)
_Excel_Close($oExcel)

$sDeviceName = $sB2
If $sDeviceName = "工脑模拟器" Then
    ; 第一条：adb shell screencap 截图
    Local $sCmd1 = '"' & $sAdbPath & '" -s ' & $sDevice & ' shell screencap ' & $sRemoteImg
    ConsoleWrite("执行截图命令：" & $sCmd1 & @CRLF)
    Local $iRet1 = RunWait($sCmd1, "", @SW_HIDE)
    If $iRet1 <> 0 Then
        MsgBox(16, "错误", "截图命令失败！返回码：" & $iRet1)
        Exit
    EndIf

    ; 加短暂延时，等模拟器文件写入完成（很关键，防止pull拿到空/损坏图片）
    Sleep(800)

    ; 第二条：adb pull 拉取到本地
    Local $sCmd2 = '"' & $sAdbPath & '" -s ' & $sDevice & ' pull ' & $sRemoteImg & ' "' & $sLocalImg & '"'
    ConsoleWrite("执行pull命令：" & $sCmd2 & @CRLF)
    Local $iRet2 = RunWait($sCmd2, "", @SW_HIDE)
    If $iRet2 <> 0 Then
        MsgBox(16, "错误", "pull拉取图片失败！返回码：" & $iRet2)
        Exit
    EndIf
ElseIf $sDeviceName = "家脑模拟器" Then
        ; 第一条：adb shell screencap 截图
    Local $sCmd1 = '"' & $sAdbPath & '" -s ' & $sDevice & ' shell screencap ' & $sRemoteImg
    ConsoleWrite("执行截图命令：" & $sCmd1 & @CRLF)
    Local $iRet1 = RunWait($sCmd1, "", @SW_HIDE)
    If $iRet1 <> 0 Then
        MsgBox(16, "错误", "截图命令失败！返回码：" & $iRet1)
        Exit
    EndIf

    ; 加短暂延时，等模拟器文件写入完成（很关键，防止pull拿到空/损坏图片）
    Sleep(800)

MsgBox(0, "完成", "截图+拉取成功！" & @CRLF & $sLocalImg)
