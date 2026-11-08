#RequireAdmin V1.0 ok 
#NoTrayIcon
AutoItSetOption("WinTitleMatchMode", 2)

ConsoleWrite("等待【是否保留用户数据】弹窗" & @CRLF)
Local $hWin = WinWait("极速PDF阅读器 3.0 卸载", "是否保留用户数据", 20)
If $hWin Then
    ConsoleWrite("✅ 捕获弹窗" & @CRLF)
    WinActivate($hWin)
    Sleep(300)
    ; 点击【取消】= 不保留用户数据
    ControlClick($hWin, "", "[CLASS:Button; TEXT:取消]")
    ConsoleWrite("✅ 点击【取消】，不保留用户数据" & @CRLF)
EndIf
