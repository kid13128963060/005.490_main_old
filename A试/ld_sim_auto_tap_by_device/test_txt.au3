; Tesseract OCR AutoIt 测试
; 注意：已经把 Tesseract 加入系统PATH，否则要写完整路径：C:\Program Files\Tesseract-OCR\tesseract.exe

Local $sTesseract = "tesseract.exe"
Local $sImgPath = @ScriptDir & "\test.png"   ; 把要识别的图片放到脚本同目录，命名 test.png
Local $sOutTxt = @ScriptDir & "\ocr_result"  ; 输出文件，tesseract会自动加 .txt
Local $sLang = "chi_sim+eng"                 ; 同时识别中文+英文

; 命令格式：tesseract 图片 输出文件名 -l 语言
Local $sCmd = $sTesseract & " """ & $sImgPath & """ """ & $sOutTxt & """ -l " & $sLang

ConsoleWrite("执行命令：" & $sCmd & @CRLF)
RunWait($sCmd, @ScriptDir, @SW_HIDE)

; 读取识别结果
Local $sResult = FileRead($sOutTxt & ".txt")
ConsoleWrite("====识别结果====" & @CRLF & $sResult & @CRLF)
MsgBox(0, "OCR识别结果", $sResult)

; 可选：删除临时txt文件
; FileDelete($sOutTxt & ".txt")
