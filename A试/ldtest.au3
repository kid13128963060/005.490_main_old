Local $sAdb = "E:\Program Files\leidian\LDPlayer9\adb.exe"
Local $sWorkDir = "E:\Program Files\leidian\LDPlayer9"
Local $sDnConsole = "E:\Program Files\leidian\LDPlayer9\dnconsole.exe" ;dnplayer

Run($sDnConsole & " launch --index 0", $sWorkDir, @SW_HIDE)

Local $sDnConsole = '"E:\Program Files\leidian\LDPlayer9\dnconsole.exe"'
; 启动【工脑模拟器】
;Run($sDnConsole & ' launch --name "工脑模拟器"', "E:\Program Files\leidian\LDPlayer9", @SW_HIDE)
