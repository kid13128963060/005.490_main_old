#include <Excel.au3>
#include <Array.au3>
local $AutoItExe, $ScriptDir

RunWait('"' & @AutoItExe & '" /AutoIt3ExecuteScript "' & @ScriptDir & "\子脚本.au3" & '"', "", @SW_HIDE)