#include <Excel.au3>
#include <Array.au3>
#include <GDIPlus.au3>

; ==================== 【配置区】 ====================
Local $sImgPath = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\ld_sim_auto_tap_by_device\pop-up.png"

; 👉 双坐标：指定矩形区域的左上角和右下角
Local $iX1 = 160      ; 区域左上角 X
Local $iY1 = 1220      ; 区域左上角 Y
Local $iX2 = 910      ; 区域右下角 X
Local $iY2 = 1480      ; 区域右下角 Y

Local $sTarget = "知道了"
Local $sTesseract = "tesseract.exe"
Local $sLang = "chi_sim+eng"
; =====================================================

; 检查坐标合法性
If $iX2 <= $iX1 Or $iY2 <= $iY1 Then
    MsgBox(16, "错误", "右下角坐标必须大于左上角坐标！")
    Exit
EndIf

; 根据双坐标自动计算宽高
Local $iROI_X = $iX1
Local $iROI_Y = $iY1
Local $iROI_W = $iX2 - $iX1
Local $iROI_H = $iY2 - $iY1

Local $sCropImg = @TempDir & "\crop_roi.png"
Local $sOutTxt = @TempDir & "\ocr_result"

; 裁剪指定区域
_GDIPlus_Startup()
Local $hSrcBmp = _GDIPlus_ImageLoadFromFile($sImgPath)
If $hSrcBmp = 0 Then
    MsgBox(16, "错误", "加载原图失败！")
    _GDIPlus_Shutdown()
    Exit
EndIf

Local $hCropBmp = _GDIPlus_BitmapCreateFromScan0($iROI_W, $iROI_H)
Local $hG = _GDIPlus_ImageGetGraphicsContext($hCropBmp)
_GDIPlus_GraphicsDrawImageRectRect($hG, $hSrcBmp, $iROI_X, $iROI_Y, $iROI_W, $iROI_H, 0, 0, $iROI_W, $iROI_H)
_GDIPlus_ImageSaveToFile($hCropBmp, $sCropImg)

_GDIPlus_GraphicsDispose($hG)
_GDIPlus_ImageDispose($hCropBmp)
_GDIPlus_ImageDispose($hSrcBmp)
_GDIPlus_Shutdown()

; OCR识别裁剪区域
Local $sCmd = $sTesseract & " """ & $sCropImg & """ """ & $sOutTxt & """ -l " & $sLang & " --psm 6"
ConsoleWrite("执行OCR命令：" & $sCmd & @CRLF)
RunWait($sCmd, @TempDir, @SW_HIDE)

Local $sResult = FileRead($sOutTxt & ".txt")
ConsoleWrite("====识别结果====" & @CRLF & $sResult & @CRLF)
MsgBox(0, "OCR识别结果", $sResult)

; 查找目标文字
If StringInStr($sResult, $sTarget) Then
    ConsoleWrite("✅ 在指定区域识别到目标文字：" & $sTarget & @CRLF)
    MsgBox(0, "识别结果", "找到：" & $sTarget)
Else
    ConsoleWrite("❌ 在指定区域未识别到：" & $sTarget & @CRLF)
    MsgBox(0, "识别结果", "未找到：" & $sTarget)
EndIf

; 清理临时文件
FileDelete($sCropImg)
FileDelete($sOutTxt & ".txt")
