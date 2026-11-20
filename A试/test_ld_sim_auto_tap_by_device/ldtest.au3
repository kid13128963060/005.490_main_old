;~ V1.0模拟器 OCR 弹窗识别点击

#include <Excel.au3>
#include <Array.au3>

; ==============================================
; 【顶部配置区】全部参数放这里
; ==============================================
Local $nLoopInterval  = 3000      ; 循环间隔3秒(毫秒)
Local $nTimeOutTotal  = 60000     ; 总时限30秒(毫秒)
Local $sTargetText    = "知道了"   ; 需要识别的目标文字
Local $nClickX,$nClickY   



Local $sDevice        = "emulator-5554"
Local $sRemoteImg     = "/sdcard/test.png"
Local $sLocalImg      = @TempDir & "\pop-up.png"
Local $sTesseract     = "tesseract.exe"
Local $sOutTxt        = @TempDir & "\ocr_result"
Local $sLang          = "chi_sim+eng"

Local $sAdb, $sWorkDir

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

; 释放COM
_Excel_BookClose($oBook)
_Excel_Close($oExcel)
;分流变量赋值
Local $sDeviceName = $sB2
If $sDeviceName = "工脑模拟器" Then
    $sAdb = "C:\leidian\LDPlayer9\adb.exe"
    $sWorkDir = "C:\leidian\LDPlayer9"
    $nClickX        = 540   ;170 540
    $nClickY        = 1360  ;630 1360
ElseIf $sDeviceName = "家脑模拟器" Then
    $sAdb = "E:\Program Files\leidian\LDPlayer9\adb.exe"
    $sWorkDir = "E:\Program Files\leidian\LDPlayer9"
    $nClickX        = 540   ; 540
    $nClickY        = 1360  ; 1360
Else
    MsgBox(16, "错误", "未识别的设备名：" & $sDeviceName)
    Exit
EndIf

; ==============================================
; 主循环：60秒超时，每3秒一轮
; ==============================================
Local $nStartTime = TimerInit()
ConsoleWrite("==== 开始循环监控，超时时间：" & $nTimeOutTotal/1000 & "秒 ====" & @CRLF)

While 1
    ; 判断是否超时
    If TimerDiff($nStartTime) >= $nTimeOutTotal Then
        ConsoleWrite("⚠️ 已到达30秒时限，脚本退出" & @CRLF)
        ExitLoop   ; 修改：Break替换为ExitLoop
    EndIf

    ; 1.adb截图模拟器
    Local $sCmd1 = '"' & $sAdb & '" -s ' & $sDevice & ' shell screencap ' & $sRemoteImg
    ConsoleWrite(@CRLF & ">> 执行截图命令" & @CRLF)
    Local $iRet1 = RunWait($sCmd1, $sWorkDir, @SW_HIDE)
    If $iRet1 <> 0 Then
        ConsoleWrite("❌ 截图命令失败！返回码：" & $iRet1 & @CRLF)
        Sleep($nLoopInterval)
        ContinueLoop
    EndIf
    Sleep(800)

    ;~ ; 2.pull拉取图片到本地临时目录
    ;~ Local $sCmd2 = '"' & $sAdb & '" -s ' & $sDevice & ' pull ' & $sRemoteImg & ' "' & $sLocalImg & '"'
    ;~ ConsoleWrite(">> 执行pull拉取图片" & @CRLF)
    ;~ Local $iRet2 = RunWait($sCmd2, $sWorkDir, @SW_HIDE)
    ;~ If $iRet2 <> 0 Then
    ;~     ConsoleWrite("❌ pull拉取图片失败！返回码：" & $iRet2 & @CRLF)
    ;~     Sleep($nLoopInterval)
    ;~     ContinueLoop
    ;~ EndIf

    ; 3.Tesseract OCR识别
    Local $sCmdOcr = '"' & $sTesseract & '" "' & $sLocalImg & '" "' & $sOutTxt & '" -l ' & $sLang
    ConsoleWrite(">> 执行OCR识别" & @CRLF)
    RunWait($sCmdOcr, @TempDir, @SW_HIDE)

    Local $sResult = ""
    If FileExists($sOutTxt & ".txt") Then
        $sResult = FileRead($sOutTxt & ".txt")
    EndIf
    ConsoleWrite("识别结果：" & $sResult & @CRLF)
    MsgBox(0, "OCR识别结果", $sResult)


    ; 4.判断目标文字
    If StringInStr($sResult, $sTargetText) Then
        ConsoleWrite("✅ 识别到目标文字：" & $sTargetText & @CRLF)
        ; 修改：adb路径增加引号，补充-s设备参数
        RunWait('"' & $sAdb & '" -s ' & $sDevice & ' shell input tap ' & $nClickX & " " & $nClickY, $sWorkDir, @SW_HIDE)
        ConsoleWrite("👉 执行点击 X:" & $nClickX & " Y:" & $nClickY & @CRLF)
        ExitLoop  ;修改：Break替换为ExitLoop ;识别成功点击后退出循环
    Else
        ConsoleWrite("❌ 未识别到【" & $sTargetText & "】" & @CRLF)
    EndIf

    ;清理本轮临时文件
    ;~ FileDelete($sOutTxt & ".txt")
    ;~ FileDelete($sLocalImg)

    Sleep($nLoopInterval)
WEnd

;最终清理
;~ FileDelete($sOutTxt & ".txt")
;~ FileDelete($sLocalImg)
ConsoleWrite("==== 脚本结束 ====" & @CRLF)
