local $AutoItExe,$sSubFile
$AutoItExe="C:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe"

Local $sSubFile = @ScriptDir & "\ldtest.au3"
;~ Local $sSubFile = @ScriptDir & "\emulator_ocr_popup_click.au3"
ConsoleWrite("子脚本完整路径：" & $sSubFile & @CRLF)
RunWait('"' & @AutoItExe & '" /AutoIt3ExecuteScript "' & $sSubFile & '"', "", @SW_HIDE)
