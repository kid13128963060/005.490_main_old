#RequireAdmin
Opt("WinTitleMatchMode", 2)

; ========== 函数区域，全部放这里 ==========
; 函数：在TF_Main主窗口内，按客户区相对坐标双击
Func ClickTreeItemByClientPos($iClientX, $iClientY, $iDelay = 400)
    Local $hWin = 0
    Local $nStart = TimerInit()
    Local $nTimeout = 10000
    While $hWin = 0 And TimerDiff($nStart) < $nTimeout
        $hWin = WinGetHandle("[CLASS:TF_Main]")
        Sleep(200)
    WEnd
    If $hWin = 0 Then
        MsgBox(0, "错误", "超时，没有找到TF_Main窗口！")
        Exit
    EndIf

    WinActivate($hWin)
    WinWaitActive($hWin, "", 5)
    Sleep($iDelay)

    Local $aWinPos = WinGetPos($hWin)
    If @error Then
        MsgBox(0, "错误", "读取窗口位置失败")
        Exit
    EndIf

    Local $iScreenX = $aWinPos[0] + $iClientX
    Local $iScreenY = $aWinPos[1] + $iClientY

    ConsoleWrite("主窗口起点：" & $aWinPos[0] & "," & $aWinPos[1] & @CRLF)
    ConsoleWrite("点击屏幕坐标：" & $iScreenX & "," & $iScreenY & @CRLF)

    MouseMove($iScreenX, $iScreenY, 0)
    Sleep($iDelay)
    MouseClick("left", $iScreenX, $iScreenY, 2, 0)
EndFunc

; 启动MES客户端
Run('F:\信恳MES\Mes_Client.exe')

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

; ========= 第三步：直接点击确认按钮（TBitBtn2，Au3Info读取到的控件） =========
ControlClick("系统登录", "", "TBitBtn2")
; ========= 第三步：登录后等待【选择线体】窗口 =========
If WinWait("选择线体", "", 10) = 0 Then
    MsgBox(0, "错误", "未检测到【选择线体】窗口，退出脚本")
    Exit
EndIf

WinActivate("选择线体")
Sleep(300)

; ========= 第四步：点击【确认】按钮 =========
ControlClick("选择线体", "", "TBitBtn1")

; ========= 第四步：线体窗口确认 =========
ControlClick("选择线体", "", "TBitBtn1")

; ========= 第五步：取消升级提示 =========
If WinWait("升级", "", 10) = 0 Then
    MsgBox(0, "错误", "未检测到【升级】窗口，退出脚本")
    Exit
EndIf

WinActivate("升级")
Sleep(300)

ControlClick("升级", "", "Button2")

Local $hWin = 0
Local $nStart = TimerInit()
Local $nTimeout = 10000 ; 最大等待时长 10秒，可自行修改

While $hWin = 0 And TimerDiff($nStart) < $nTimeout
    $hWin = WinGetHandle("[CLASS:TF_Main]")
    Sleep(200) ; 每200ms查找一次
WEnd

If $hWin = 0 Then
    MsgBox(0, "错误", "超时，没有找到这个窗口！")
    Exit
EndIf



WinActivate($hWin)
WinWaitActive($hWin, "", 5)
Sleep(800)

Local $aWinPos = WinGetPos($hWin)
If @error Then
    MsgBox(0, "错误", "读取窗口位置失败")
    Exit
EndIf

Local $winScreenX = $aWinPos[0]
Local $winScreenY = $aWinPos[1]

; 在线维修坐标
ClickTreeItemByClientPos(70, 140, 500)

ClickTreeItemByClientPos(70, 158, 500)


