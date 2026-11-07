; 等待【卸载】问卷窗口出现
WinWait("卸载", "您遇到的问题是?", 8)
If WinExists("卸载") Then
    WinActivate("卸载")
    ControlClick("卸载", "", "[TEXT:我要卸载]")
    Sleep(600)
    ; 如果后面还有确认弹窗，继续追加点击代码
EndIf
