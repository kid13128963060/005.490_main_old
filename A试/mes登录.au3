; 启动MES客户端
Run('F:\信息MES\Mes_Client.exe')

; 等待登录窗口
If WinWait("系统登录", "", 10) = 0 Then
    MsgBox(0, "错误", "未检测到【系统登录】窗口，退出脚本")
    Exit
EndIf
WinActivate("系统登录")
Sleep(400)

; ========= 第一步：密码框输入密码 =========
ControlFocus("系统登录", "", "TcxCustomInnerTextEdit1")
Sleep(200)
ControlSend("系统登录", "", "TcxCustomInnerTextEdit1", "0911047")
Sleep(300)

; ========= 第二步：Tab跳到【登录系统】下拉框，选择深圳信恳生产机 =========
Send("{TAB}")
Sleep(200)
Send("{DOWN}")
Sleep(150)
Send("{DOWN}")
Sleep(150)
Send("{DOWN}")
Sleep(150)


