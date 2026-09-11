// ========== 初始化：强制全部重置，清除全局旧残留 ==========
auto.setVar("总数据条数", 7);
// 禁止嵌套setVar(..., getVar())，拆分为中间变量
let inner_total_data = auto.getVar("总数据条数");
auto.setVar("选择", inner_total_data);

auto.setVar("计数", 0);
auto.setVar("已写入计数", 0);
auto.setVar("单次循环上限", 6);
auto.setVar("提前终止本轮循环", 0);
auto.setVar("步序0_行数", 0);
auto.setVar("数据源序号", 0);

// 从全局变量读取两组数据源（前置节点提前赋值好）
const source0_text = auto.getVar("source0_text") || "";
const source01_text = auto.getVar("source01_text") || "";

const sourceList = [source0_text, source01_text];

// 初始化加载第0组数据源
auto.setVar("excel_文行列数", sourceList[0]);

let rawText = auto.getVar("excel_文行列数") || "";
let arr = [];

if (rawText.trim().startsWith("[")) {
  try {
    arr = JSON.parse(rawText);
  } catch (e) {
    arr = [];
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
}

auto.setVar("步序0_行数", targetRow);
