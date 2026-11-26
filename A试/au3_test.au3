; 导入公共库，写对network_helper.au3的路径
#include "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\module\network_helper.au3"


; 一键调用整套网络检测+断网自动开关WiFi
Local $bNetState = NetworkCheckAndWifiReset()

; 也可以单独调用：
; $bNetState = CheckNetwork()   ;只检测网络
; WifiToggle(1)                 ;只执行WiFi切换
