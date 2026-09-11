//读取原始字符串（行号数组来源 excel_文行列数）
let rawText = auto.getVar("excel_文行列数") || "";
let arr = [];

if (rawText.trim().startsWith("[")) {
  //标准JSON数组解析分支
  try {
    arr = JSON.parse(rawText);
  } catch (e) {
    arr = [];
    auto.log("解析JSON数组失败，置空数组");
  }
} else {
  //逗号分隔数字字符串处理分支
  arr = rawText
    .split(",")
    .map(function (item) {
      return Number(item.trim());
    })
    .filter(function (n) {
      return !isNaN(n);
    });
}

// 根据全局变量【计数】作为数组下标取出目标行号
let index = Number(auto.getVar("计数")) || 0;
let targetRow;

//越界兜底，下标超出数组范围赋值0避免读取Excel报错
if (arr.length > 0 && index >= 0 && index < arr.length) {
  targetRow = arr[index];
} else {
  targetRow = 0;
  auto.log("下标越界或数组为空，步序0_行数赋值为0");
}

auto.setVar("步序0_行数", targetRow);
auto.log("计数值=" + index + "，取数组对应下标，步序0_行数 = " + targetRow);
