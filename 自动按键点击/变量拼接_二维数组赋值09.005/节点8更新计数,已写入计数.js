//节点 8
// 读取状态变量，打印前置调试日志
let text0 = auto.getVar("步序0_行数");
let srcIndex = Number(auto.getVar("数据源序号")) || 0;
let total = Number(auto.getVar("总数据条数")) || 0;
let written = Number(auto.getVar("已写入计数")) || 0;
let runFlag = Number(auto.getVar("runFlag")) || 0;
auto.log(
  "【节点7调试】读取前本轮要读行号=" +
    text0 +
    "，当前数据源序号：" +
    srcIndex +
    "，已写入计数=" +
    written +
    "，runFlag=" +
    runFlag,
);

// 1. 当前数据源内计数自增
let countVal = Number(auto.getVar("计数")) || 0;
auto.log("自增前 计数 = " + countVal);
countVal = countVal + 1;
auto.setVar("计数", countVal);
auto.log("自增后 计数 = " + auto.getVar("计数"));

// 2. 全局总写入条数自增
let wCnt = Number(auto.getVar("已写入计数")) || 0;
wCnt = wCnt + 1;
auto.setVar("已写入计数", wCnt);
auto.log("自增后 已写入计数 = " + auto.getVar("已写入计数"));

// 3. 解析当前数据源文本，预读取下一轮待读取行号
let rawText = auto.getVar("excel_文行列数") || "";
let arr = [];
if (rawText.trim().startsWith("[")) {
  try {
    arr = JSON.parse(rawText);
  } catch (e) {
    arr = [];
    auto.log("解析JSON数组失败，置空数组");
  }
} else {
  arr = rawText
    .split(",")
    .map(function (item) {
      return Number(item.trim());
    })
    .filter(function (n) {
      return !isNaN(n);
    });
}

let index = Number(auto.getVar("计数")) || 0;
let targetRow;
if (arr.length > 0 && index >= 0 && index < arr.length) {
  targetRow = arr[index];
} else {
  targetRow = 0;
  auto.log("下标越界或数组为空，步序0_行数赋值为0");
}
auto.setVar("步序0_行数", targetRow);

// 循环调试日志
let curSrcNo = Number(auto.getVar("数据源序号"));
auto.log(
  "【循环内合并脚本调试】数据源序号=" +
    curSrcNo +
    "｜计数值=" +
    index +
    "，下一轮步序0_行数 = " +
    targetRow,
);
