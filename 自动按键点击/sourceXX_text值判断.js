// 封装函数，最终return runFlag数值
function calcRunFlag() {
  auto.setVar("runFlag", 0);

  const sourceRaw = auto.getVar("excel_文行列数") || "";
  let arr = [];
  try {
    if (sourceRaw.trim().startsWith("[")) {
      arr = JSON.parse(sourceRaw);
    } else {
      arr = sourceRaw
        .split(",")
        .map((item) => Number(item.trim()))
        .filter((n) => !isNaN(n));
    }
  } catch (e) {
    arr = [];
    auto.log("数据源数组解析失败");
  }

  const countVal = Number(auto.getVar("计数")) || 0;
  let runFlag = Number(auto.getVar("runFlag")) || 0;
  let extractVal;

  const targetIndex = countVal - 1;

  if (targetIndex >= 0 && targetIndex < arr.length) {
    extractVal = arr[targetIndex];
    auto.log("数组下标:" + targetIndex + "，提取数值=" + extractVal);
    runFlag = extractVal === 0 ? 1 : 0;
  } else {
    auto.log("下标越界，runFlag置1");
    runFlag = 1;
  }

  auto.setVar("runFlag", runFlag);
  auto.setVar("提取数值", extractVal);

  // 返回0或1
  return runFlag;
}

// 调用函数，接收返回值存入变量 receiveFlag
let receiveFlag = calcRunFlag();
auto.log("接收函数返回值：" + receiveFlag);
