#include <Excel.au3>
#include <Array.au3>

; ==============================================
; ========= 顶部配置区（全部在这里修改）=========
Global $iLoopIntervalMs  = 3000      ;循环间隔 3秒
Global $iMaxWaitMs       = 30 * 1000 ;最大等待时限 30秒
Global $sTargetKeyword   = "知道了"   ;要识别的目标文字
Global $sTesseract       = "tesseract.exe"
Global $sLang            = "chi_sim+eng"
; ==============================================

Local $sDevice = "emulator-5554"
Local $sRemoteImg = "/sdcard/test.png"
Local $sLocalImg = @TempDir & "\pop-up.png"
Local $sOutTxt   = @TempDir & "\ocr_result"

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

Local $sB2 = _Excel_RangeRead($oBook, Default, "B2")

_Excel_BookClose($oBook)
_Excel_Close($oExcel)

Local $sAdbPath
$sDeviceName = $sB2
If $sDeviceName = "工脑模拟器" Then
    $sAdbPath = "c:\leidian\LDPlayer9\adb.exe"
ElseIf $sDeviceName = "家脑模拟器" Then
    $sAdbPath = "E:\Program Files\leidian\LDPlayer9\adb.exe"
Else
    MsgBox(16, "错误", "未识别的设备名：" & $sDeviceName)
    Exit
EndIf


;====================循环OCR等待目标文字====================
Local $hTimer = TimerInit() ;启动计时
Local $bFound = False

While True
    ;判断是否超时
    If TimerDiff($hTimer) >= $iMaxWaitMs Then
        ConsoleWrite("⚠️ 已达到最大等待时限" & $iMaxWaitMs/1000 & "秒，未检测到关键词【" & $sTargetKeyword & "】" & @CRLF)
        BreakLoop
    EndIf

    ;1.ADB截图
    Local $sCmd1 = '"' & $sAdbPath & '" -s ' & $sDevice & ' shell screencap ' & $sRemoteImg
    Local $iRet1 = RunWait($sCmd1, "", @SW_HIDE)
    If $iRet1 <> 0 Then
        ConsoleWrite("❌截图命令失败！返回码：" & $iRet1 & @CRLF)
        Sleep($iLoopIntervalMs)
        ContinueLoop
    EndIf
    Sleep(800)

    ;2.pull拉取图片到临时目录
    Local $sCmd2 = '"' & $sAdbPath & '" -s ' & $sDevice & ' pull ' & $sRemoteImg & ' "' & $sLocalImg & '"'
    Local $iRet2 = RunWait($sCmd2, "", @SW_HIDE)
    If $iRet2 <> 0 Then
        ConsoleWrite("❌pull拉取图片失败！返回码：" & $iRet2 & @CRLF)
        Sleep($iLoopIntervalMs)
        ContinueLoop
    EndIf

    ;3.Tesseract OCR识别
    Local $sCmdOcr = $sTesseract & " """ & $sLocalImg & """ """ & $sOutTxt & """ -l " & $sLang
    RunWait($sCmdOcr, @TempDir, @SW_HIDE)

    Local $sResult = ""
    If FileExists($sOutTxt & ".txt") Then
        $sResult = FileRead($sOutTxt & ".txt")
    EndIf
    ConsoleWrite("====识别结果====" & @CRLF & $sResult & @CRLF)

    ;4.判断是否包含目标关键词
    If StringInStr($sResult,$sTargetKeyword) Then
        ConsoleWrite("🎉成功检测到关键词【" & $sTargetKeyword & "】" & @CRLF)
        $bFound = True
        BreakLoop
    EndIf

    ;清理临时文件
    FileDelete($sOutTxt & ".txt")
    FileDelete($sLocalImg)

    ;循环间隔等待
    Sleep($iLoopIntervalMs)
WEnd

;最后清理残留
FileDelete($sOutTxt & ".txt")
FileDelete($sLocalImg)

If $bFound Then
    MsgBox(0,"结果","检测到目标文字：" & $sTargetKeyword)
Else
    MsgBox(48,"结果","超时，未检测到目标文字")
EndIf
