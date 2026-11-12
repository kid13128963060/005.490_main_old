#include <File.au3>

;==================== 配置区 ====================
Local $sAdbPath = "C:\leidian\LDPlayer9\adb.exe"
Local $sAdbDevice = "-s emulator-5554"
Local $sXmlLocal = @ScriptDir & "\ui.xml"
Local $iDumpTimeout = 5000
Local $iRetryCount = 3
;===============================================

Local $sAdb = '"' & $sAdbPath & '" ' & $sAdbDevice

Func DumpUiXml()
    RunWait($sAdb & " shell uiautomator dump /sdcard/ui.xml", @ScriptDir, @SW_HIDE, $iDumpTimeout)
    If @error Then
        ConsoleWrite("【Dump失败】模拟器内生成xml超时" & @CRLF)
        Return False
    EndIf
    If FileExists($sXmlLocal) Then FileDelete($sXmlLocal)
    RunWait($sAdb & " pull /sdcard/ui.xml " & '"' & $sXmlLocal & '"', @ScriptDir, @SW_HIDE)
    If FileExists($sXmlLocal) Then
        ConsoleWrite("Dump成功" & @CRLF)
        Return True
    Else
        ConsoleWrite("【Pull失败】拉取xml失败" & @CRLF)
        Return False
    EndIf
EndFunc

Func FindByText($sXmlFile, $sSearchText)
    Local $oXml = ObjCreate("MSXML2.DOMDocument.6.0")
    If $oXml = 0 Then Return ""
    $oXml.async = False
    $oXml.validateOnParse = False
    $oXml.load($sXmlFile)
    If $oXml.parseError.errorCode <> 0 Then
        ConsoleWrite("XML解析错误：" & $oXml.parseError.reason & @CRLF)
        $oXml = 0
        Return ""
    EndIf
    Local $nodes = $oXml.selectNodes("//node[@text='" & $sSearchText & "']")
    If $nodes.length = 0 Then
        $oXml = 0
        Return ""
    EndIf
    Local $sBounds = $nodes[0].getAttribute("bounds")
    $oXml = 0
    Return BoundsToCenter($sBounds)
EndFunc

Func BoundsToCenter($sBounds)
    $sBounds = StringReplace(StringReplace($sBounds, "[", ","), "]", ",")
    Local $aSplit = StringSplit($sBounds, ",")
    If $aSplit[0] < 5 Then Return ""
    Local $x1 = $aSplit[2], $y1 = $aSplit[3], $x2 = $aSplit[4], $y2 = $aSplit[5]
    Local $cx = ($x1 + $x2) / 2
    Local $cy = ($y1 + $y2) / 2
    Return $cx & "," & $cy
EndFunc

; ========== 主逻辑：查找并点击【退出登录】 ==========
Local $sPos = ""
For $i = 1 To $iRetryCount
    ConsoleWrite(@CRLF & "====第" & $i & "次查找【退出登录】====" & @CRLF)
    If DumpUiXml() = False Then
        Sleep(1500)
        ContinueLoop
    EndIf
    $sPos = FindByText($sXmlLocal, "退出登录")
    If $sPos <> "" Then
        ConsoleWrite("✅ 找到退出登录按钮，坐标：" & $sPos & @CRLF)
        Break
    EndIf
    Sleep(2000)
Next

If $sPos = "" Then
    MsgBox(0, "失败", "多次重试，未找到【退出登录】按钮！")
    If FileExists($sXmlLocal) Then FileDelete($sXmlLocal)
    Exit
EndIf

Local $aXY = StringSplit($sPos, ",")
RunWait($sAdb & " shell input tap " & $aXY[1] & " " & $aXY[2], @ScriptDir, @SW_HIDE)
Sleep(1000)

If FileExists($sXmlLocal) Then FileDelete($sXmlLocal)
ConsoleWrite("👉 退出登录点击指令已发送" & @CRLF)
