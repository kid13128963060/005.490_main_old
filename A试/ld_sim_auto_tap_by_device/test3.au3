#include <Excel.au3>
#include <Array.au3>
Local $sAdb, $sWorkDir, $sDnConsole, $nWaitMs

; ==================== 【代码2 合并在此处】Tesseract OCR 测试 ====================
; 注意：已经把 Tesseract 加入系统PATH，否则要写完整路径如："D:\Tesseract-OCR\tesseract.exe"
Local $sTesseract = "tesseract.exe"
; 按你要求，固定原图路径
Local $sImgPath = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\ld_sim_auto_tap_by_device\pop-up.png"
Local $sOutTxt = @TempDir & "\ocr_result"  ;输出文件迁移至临时目录，规避中文路径问题
Local $sLang = "chi_sim+eng"               ;同时识别中文+英文
$sAdb = "C:\leidian\LDPlayer9\adb.exe"
$sWorkDir = "C:\leidian\LDPlayer9"

; 命令格式：tesseract 图片 输出文件名 -l 语言
Local $sCmd = $sTesseract & " """ & $sImgPath & """ """ & $sOutTxt & """ -l " & $sLang

ConsoleWrite("执行OCR命令：" & $sCmd & @CRLF)
RunWait($sCmd, @TempDir, @SW_HIDE)

; 读取识别结果
Local $sResult = FileRead($sOutTxt & ".txt")
ConsoleWrite("====识别结果====" & @CRLF & $sResult & @CRLF)
;MsgBox(0, "OCR识别结果", $sResult)

; ========== 查找目标文字【知道了】 ==========
Local $sTarget = "知道了"
If StringInStr($sResult, $sTarget) Then
    ConsoleWrite("✅ 识别到目标文字：" & $sTarget & @CRLF)
    ;MsgBox(0, "查找结果", "找到了")
    ; 这里后续填入ADB点击代码
    RunWait($sAdb & " shell input tap " & 169 & " " & 630, $sWorkDir, @SW_HIDE)
Else
    ConsoleWrite("❌ 未识别到【" & $sTarget & "】" & @CRLF)
    MsgBox(0, "查找结果", "未找到")

EndIf

; 清理OCR输出临时txt（原图pop-up.png保留，不删除）
FileDelete($sOutTxt & ".txt")
