const source0_text = auto.getVar("source0_text") || "";
const source01_text = auto.getVar("source01_text") || "";
const sourceList = [source0_text, source01_text];
const PER_SOURCE_LIMIT = 6; // 单个数据源最多写6条

let srcIndex = Number(auto.getVar("数据源序号")) || 0;
let total = Number(auto.getVar("总数据条数")) || 0;
let written = Number(auto.getVar("已写入计数")) || 0;
let runFlag = Number(auto.getVar("runFlag")) || 0;

auto.log("【节点2调试】当前数据源序号：" + srcIndex + "，已写入计数=" + written + "，runFlag=" + runFlag);

// 新触发条件：已写入>0 且 (未写完全部数据 || runFlag值为1)
if (written > 0 && (written < total || runFlag === 1)) {
    // 双向切换 0<->1
    srcIndex = srcIndex === 0 ? 1 : 0;
    auto.setVar("数据源序号", srcIndex);
    auto.setVar("excel_文行列数", sourceList[srcIndex]);
    auto.setVar("计数", 0);
    // ✅切换数据源之后，把全局runFlag置0
    auto.setVar("runFlag", 0);
    auto.log("✅【切换数据源】切换到序号" + srcIndex + "，读取下标计数重置为0，runFlag已置0");

    let rawText = auto.getVar("excel_文行列数") || "";
    let arr = [];
    if (rawText.trim().startsWith("[")) {
        try { arr = JSON.parse(rawText); } catch (e) { arr = []; }
    } else {
        arr = rawText.split(",").map(x => Number(x.trim())).filter(n => !isNaN(n));
    }
    let newIdx = Number(auto.getVar("计数"));
    let newRow;
    if (arr.length > 0 && newIdx >= 0 && newIdx < arr.length) {
        newRow = arr[newIdx];
    } else {
        newRow = -1; // 越界标记，不修改提前终止变量
    }
    auto.setVar("步序0_行数", newRow);
    auto.log("【切换数据源完成】步序0_行数 = " + newRow);
} else {
    auto.log("【节点2】条件不满足，不切换数据源");
    // 不切换时也要刷新当前数据源的行号
    let rawText = auto.getVar("excel_文行列数") || "";
    let arr = [];
    if (rawText.trim().startsWith("[")) {
        try { arr = JSON.parse(rawText); } catch (e) { arr = []; }
    } else {
        arr = rawText.split(",").map(x => Number(x.trim())).filter(n => !isNaN(n));
    }
    let newIdx = Number(auto.getVar("计数"));
    let newRow;
    if (arr.length > 0 && newIdx >= 0 && newIdx < arr.length) {
        newRow = arr[newIdx];
    } else {
        newRow = -1;
    }
    auto.setVar("步序0_行数", newRow);
}