// 增加空值兜底，彻底解决数组length报错
function parseNumberList(text) {
  if (text === undefined || text === null || text.trim() === "") {
    return [];
  }
  let arr = [];
  const raw = text || "";
  if (raw.trim().startsWith("[")) {
    try {
      arr = JSON.parse(raw);
    } catch (e) {
      arr = [];
      auto.log("解析数组失败，置空");
    }
  } else {
    arr = raw
      .split(",")
      .map((item) => Number(item.trim()))
      .filter((n) => !isNaN(n));
  }
  return arr;
}

// 加载文档4组全局数据源
const source0_text = auto.getVar("source0_text") || "";
const source01_text = auto.getVar("source01_text") || "";
const source02_text = auto.getVar("source02_text") || "";
const source03_text = auto.getVar("source03_text") || "";
const sourceList = [source0_text, source01_text, source02_text, source03_text];

let srcIndex = Number(auto.getVar("数据源序号")) || 0;
let runFlagVal = Number(auto.getVar("runFlag")) || 0;
let written = Number(auto.getVar("已写入计数")) || 1;
let realDone = written - 1;

auto.log(
  "【切换脚本入口】runFlag=" +
    runFlagVal +
    "｜当前数据源序号=" +
    srcIndex +
    "｜已完成=" +
    realDone,
);

// 仅runFlag=1才轮换数据源序号
if (runFlagVal === 1) {
  srcIndex = srcIndex >= sourceList.length - 1 ? 0 : srcIndex + 1;
  auto.setVar("数据源序号", srcIndex);
  auto.setVar("excel_文行列数", sourceList[srcIndex]);
  auto.setVar("计数", 0);
  auto.log("✅数据源切换成功，新序号=" + srcIndex + "，计数重置0");
} else {
  auto.setVar("excel_文行列数", sourceList[srcIndex]);
  auto.log("runFlag=0，不切换，保持数据源序号=" + srcIndex);
}

// 切换完成强制清空runFlag，阻断单次循环无限跳转
auto.setVar("runFlag", 0);

let arr = parseNumberList(auto.getVar("excel_文行列数"));
let newIdx = Number(auto.getVar("计数")) || 0;
let newRow =
  arr.length > 0 && newIdx >= 0 && newIdx < arr.length ? arr[newIdx] : -1;
auto.setVar("步序0_行数", newRow);

auto.log(
  "【切换脚本结束】待读取行号=" + newRow + "｜最终数据源序号=" + srcIndex,
);

// 调试日志
let text0 = auto.getVar("步序0_行数");
let srcIndexLog = Number(auto.getVar("数据源序号")) || 0;
let total = Number(auto.getVar("总数据条数")) || 0;
let writtenLog = Number(auto.getVar("已写入计数")) || 0;
let runFlagLog = Number(auto.getVar("runFlag")) || 0;
auto.log(
  "【节点2调试】本轮要读行号=" +
    text0 +
    "，数据源序号：" +
    srcIndexLog +
    "，已写入计数=" +
    writtenLog +
    "，runFlag=" +
    runFlagLog,
);
