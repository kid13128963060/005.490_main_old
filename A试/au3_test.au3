; ====================== 顶部配置区（可自行修改，24小时制，HH:MM） ======================
Local $sTimeStart1 = "00:01"   ; 00:01 分支1起始时间 06:01
Local $sTimeEnd1   = "00:15"   ; 00:15 分支1结束时间 07:15
Local $sTimeStart2 = "00:16"   ; 00:16 分支2起始时间
Local $sTimeEnd2   = "00:30"   ; 00:30分支2结束时间
; =====================================================================================

; 函数：判断当前时间是否在 [sStart, sEnd) 区间内，左闭右开，避免交界重复执行
Func TimeIsBetween($sStart, $sEnd)
    Local $sNow = @HOUR & ":" & @MIN
    Local $aNow  = StringSplit($sNow,  ":")
    Local $aS    = StringSplit($sStart,":")
    Local $aE    = StringSplit($sEnd,  ":")
    Local $iNow  = $aNow[1]*60 + $aNow[2]
    Local $iS    = $aS[1]*60   + $aS[2]
    Local $iE    = $aE[1]*60   + $aE[2]
    Return ($iNow >= $iS And $iNow < $iE)
EndFunc   ;==>TimeIsBetween

; 时间分流判断
If TimeIsBetween($sTimeStart1, $sTimeEnd1) Then
    ConsoleWrite("当前时间属于【分支2】" & @CRLF)
    ; ========== 分支1代码放这里 ==========
    $sDeviceName = "工脑模拟器-0"
    MsgBox(0, "提示", $sDeviceName)
ElseIf TimeIsBetween($sTimeStart2, $sTimeEnd2) Then
    ConsoleWrite("当前时间属于【分支3】" & @CRLF)
    ; ========== 分支2代码放这里 ==========
    $sDeviceName = "工脑模拟器-1"
        MsgBox(0, "提示", $sDeviceName)
Else
    ConsoleWrite("当前时间不在指定时段" & @CRLF)
    ; ========== 其余时间分支 ==========

EndIf
