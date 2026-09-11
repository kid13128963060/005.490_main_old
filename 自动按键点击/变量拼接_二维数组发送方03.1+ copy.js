// 从全局变量获取目标存储变量名
let targetVar = auto.getVar("store_var_name") || "table_data_01";

// 读取原有变量，空值兜底空字符串
let rawStoreText = auto.getVar(targetVar) || "";

// 根据全局变量"选择"数值读取对应数量步序文本
let selectNum = Number(auto.getVar("选择")) || 0;
let stepTextList = [];

for (let i = 0; i < selectNum; i++) {
  let indexStr;
  if (i === 0) {
    indexStr = "0";
  } else {
    indexStr = String(i).padStart(2, "0");
  }
  let keyName = `步序${indexStr}_文`;
  let rawStepText = auto.getVar(keyName) || "";
  stepTextList.push(rawStepText);
}

// 拼接所有步序文本
let allStepText = stepTextList.join("");

// 原有变量值 + 步序文本拼接
let mergedCombineText = rawStoreText + allStepText;

// 移除字符串最后一位逗号（如果末尾存在逗号）
if (mergedCombineText.endsWith(",")) {
  mergedCombineText = mergedCombineText.slice(0, -1);
}

auto.setVar(targetVar, mergedCombineText);
let text0 = auto.getVar(targetVar);
auto.log(`我读取到${targetVar}的内容：` + text0);
