#include <Excel.au3>
#include <Array.au3>

; ==============================================
; V1.1 ok ADB 雷电模拟器截图 + pull拉取图片
; 设备：emulator-5554
; ==============================================
Local $sDevice = "emulator-5554"
Local $sRemoteImg = "/sdcard/test.png"
Local $sLocalImg = @TempDir & "\pop-up.png"

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

$sDeviceName = $sB2
If $sDeviceName = "工脑模拟器" Then
Local     $sAdbPath = "c:\leidian\LDPlayer9\adb.exe"

ElseIf $sDeviceName = "家脑模拟器" Then
Local     $sAdbPath = "E:\Program Files\leidian\LDPlayer9\adb.exe"

Else
    MsgBox(16, "错误", "未识别的设备名：" & $sDeviceName)
    Exit
EndIf

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
;MsgBox(0, "完成", "截图+拉取成功！" & @CRLF & $sLocalImg)


; ==================== 【代码2 合并在此处】Tesseract OCR 测试 ====================
; 注意：已经把 Tesseract 加入系统PATH，否则要写完整路径如："D:\Tesseract-OCR\tesseract.exe"
Local $sTesseract = "tesseract.exe"
Local $sImgPath = @TempDir & "\pop-up.png"
Local $sOutTxt = @TempDir & "\ocr_result"  ;输出文件迁移至临时目录，规避中文路径问题
Local $sLang = "chi_sim+eng"               ;同时识别中文+英文

; 命令格式：tesseract 图片 输出文件名 -l 语言
Local $sCmd = $sTesseract & " """ & $sImgPath & """ """ & $sOutTxt & """ -l " & $sLang

ConsoleWrite("执行OCR命令：" & $sCmd & @CRLF)
    RunWait($sCmd, @TempDir, @SW_HIDE)

; 读取识别结果
    Local         $sResult = FileRead($sOutTxt & ".txt")
        ConsoleWrite("====识别结果====" & @CRLF & $sResult & @CRLF)
MsgBox(0, "OCR识别结果", $sResult)

; 清理临时文件
FileDelete($sOutTxt & ".txt")
FileDelete($sLocalImg)
