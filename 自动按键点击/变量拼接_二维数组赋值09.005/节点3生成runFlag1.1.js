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

let rawText = auto.getVar("excel_文行列数") || "";
let arr = parseNumberList(rawText);

let index = Number(auto.getVar("计数")) || 0;
let targetRow =
  arr.length > 0 && index >= 0 && index < arr.length ? arr[index] : 0;
auto.setVar("步序0_行数", targetRow);

let written = Number(auto.getVar("已写入计数")) || 1;
let realDone = written - 1;
let srcIndex = Number(auto.getVar("数据源序号")) || 0;

let newRunFlag = 0;
// 规则1A：6倍数，数据源≠1、≠3、≠2（仅src0触发）
const rule1A =
  realDone !== 0 &&
  realDone % 6 === 0 &&
  srcIndex !== 1 &&
  srcIndex !== 2 &&
  srcIndex !== 3;
// 规则1B：数据源=2，realDone=6倍数+1，排除7
const rule1B = srcIndex === 2 && (realDone - 1) % 6 === 0 && realDone !== 7;
const condition1 = rule1A || rule1B;
// 规则2：下标1~5且行等于0，所有数据源生效
const condition2 = index >= 1 && index <= 5 && targetRow === 0;

if (condition1 || condition2) {
  newRunFlag = 1;
}

auto.setVar("runFlag", newRunFlag);
auto.log(
  `【生成runFlag】src=${srcIndex} index=${index} row=${targetRow} realDone=${realDone} flag=${newRunFlag}`,
);
