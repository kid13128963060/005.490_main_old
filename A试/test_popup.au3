#RequireAdmin
#NoTrayIcon
#include <GuiConstantsEx.au3>   ; 关键！引入GUI常量，包含$GUI_EVENT_CLOSE

Local $hGUI = GUICreate("卸载", 400, 220)
GUICtrlCreateLabel("您遇到的问题是?", 30, 30, 300, 30)
Local $btn = GUICtrlCreateButton("我要卸载", 120, 90, 140, 40)
GUISetState(@SW_SHOW, $hGUI)

While 1
    Local $nMsg = GUIGetMsg()
    Switch $nMsg
        Case $GUI_EVENT_CLOSE
            Exit
        Case $btn
            MsgBox(0, "提示", "✅ 按钮被点击成功！")
            ; Exit 注释掉，点按钮后窗口不关闭，方便反复测试
    EndSwitch
WEnd
