#RequireAdmin
#NoTrayIcon
AutoItSetOption("WinTitleMatchMode", 2)

; 等待【卸载】问卷窗口出现，标题包含“卸载”，文本包含“您遇到的问题是?”，超时8秒
WinWait("卸载", "您遇到的问题是?", 8)
If WinExists("卸载") Then
    WinActivate("卸载")
    Sleep(300)
    ControlClick("卸载", "", "[TEXT:我要卸载]")
    Sleep(600)
EndIf

Exit 0
