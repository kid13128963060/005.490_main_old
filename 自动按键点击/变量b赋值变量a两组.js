/**
 * 脚本名称：数据源数组推送脚本
 * 功能：一维数据，存入全局存储
 * 规范：仅输出2个全局存储KEY，赋值脚本统一读取
 */
// ====================== 1. 统一字段标签常量（唯一文字源头） ======================
const fieldLabelTextArr = ["步序0_数", "步序01_数"];

// ====================== 2.一维数据， ======================
let gKey_varAddOne0 = auto.getVar("剪贴板_图数");
let gKey_varAddOne01 = auto.getVar("剪贴板历史_图");
const tableDataArr = [
  // 选择序号1
  ["gKey_varAddOne0", "gKey_varAddOne01"],
];

// ====================== 3. 全局存储常量（精简仅2个） ======================
const CONST_STORAGE_LABEL_ARR = "GLOBAL_TEXT_ARRAY01"; // 字段标签一维数组
const CONST_STORAGE_TABLE_ARR = "GLOBAL_TEXT_TABLE"; // 合并后的二维数据表数组

// ====================== 4. 序列化存入全局变量 ======================
auto.setVar(CONST_STORAGE_LABEL_ARR, JSON.stringify(fieldLabelTextArr));
auto.setVar(CONST_STORAGE_TABLE_ARR, JSON.stringify(tableDataArr));

// ====================== 5. 新增：数据合法性校验（修复隐性风险） ======================
const fieldCount = fieldLabelTextArr.length;
tableDataArr.forEach((row, idx) => {
  if (row.length !== fieldCount) {
    auto.log(
      `【数据警告】序号${idx + 1}行字段数量不匹配！标签总字段：${fieldCount}，当前行：${row.length}`,
    );
  }
});

// ====================== 6. 写入校验日志 ======================
auto.log("【数据源推送】===== 合并二维数组写入完成 ===== ");
auto.log(`【数据源推送】字段标签数组：${JSON.stringify(fieldLabelTextArr)}`);
auto.log(`【数据源推送】合并数据表二维数组：${JSON.stringify(tableDataArr)}`);

// 读取校验存储变量
auto.log(
  `【数据源校验】标签存储 GLOBAL_TEXT_ARRAY01：${auto.getVar(CONST_STORAGE_LABEL_ARR)}`,
);
auto.log(
  `【数据源校验】合并数据表 GLOBAL_TEXT_TABLE：${auto.getVar(CONST_STORAGE_TABLE_ARR)}`,
);

auto.log("【数据源推送】二维总表、标签数组已存入全局存储，等待赋值脚本读取");

/**
 * 脚本名称：数据源数组推送脚本
 * 功能：合并4组业务数据为二维数组 + 标签数组，存入全局存储
 * 规范：仅输出2个全局存储KEY，赋值脚本统一读取
 */
// ====================== 1. 统一字段标签常量（唯一文字源头） ======================
const fieldLabelTextArr = [
  "步序01_节点深度",
  "步序01_节点类名",
  "应用包名",
  "步序01_节点ID",
];

// ====================== 2. 原始4组一维数据，合并为单二维数组 ======================
const tableDataArr = [
  // 选择序号1
  [
    20,
    "android.widget.TextView",
    "com.ss.android.article.lite",
    "com.ss.android.article.lite:id/ay",
  ],
  // 选择序号2
  [
    25,
    "android.widget.TextView",
    "com.alicloud.databox",
    "com.alicloud.databox:id/featureTextView",
  ],
];

// ====================== 3. 全局存储常量（精简仅2个） ======================
const CONST_STORAGE_LABEL_ARR = "GLOBAL_TEXT_ARRAY01"; // 字段标签一维数组
const CONST_STORAGE_TABLE_ARR = "GLOBAL_TEXT_TABLE"; // 合并后的二维数据表数组

// ====================== 4. 序列化存入全局变量 ======================
auto.setVar(CONST_STORAGE_LABEL_ARR, JSON.stringify(fieldLabelTextArr));
auto.setVar(CONST_STORAGE_TABLE_ARR, JSON.stringify(tableDataArr));

// ====================== 5. 新增：数据合法性校验（修复隐性风险） ======================
const fieldCount = fieldLabelTextArr.length;
tableDataArr.forEach((row, idx) => {
  if (row.length !== fieldCount) {
    auto.log(
      `【数据警告】序号${idx + 1}行字段数量不匹配！标签总字段：${fieldCount}，当前行：${row.length}`,
    );
  }
});

// ====================== 6. 写入校验日志 ======================
auto.log("【数据源推送】===== 合并二维数组写入完成 ===== ");
auto.log(`【数据源推送】字段标签数组：${JSON.stringify(fieldLabelTextArr)}`);
auto.log(`【数据源推送】合并数据表二维数组：${JSON.stringify(tableDataArr)}`);

// 读取校验存储变量
auto.log(
  `【数据源校验】标签存储 GLOBAL_TEXT_ARRAY01：${auto.getVar(CONST_STORAGE_LABEL_ARR)}`,
);
auto.log(
  `【数据源校验】合并数据表 GLOBAL_TEXT_TABLE：${auto.getVar(CONST_STORAGE_TABLE_ARR)}`,
);

auto.log("【数据源推送】二维总表、标签数组已存入全局存储，等待赋值脚本读取");

// 通用_多数组选择赋值全局变量脚本（适配合并二维数据表）
// 原有分流、长度校验、日志、赋值逻辑全部保留，仅修改数组读取方式
const AUTO_SHUNT_LIMIT_BY_ARRAY = true;
const MANUAL_MAX_SHUNT = 6;
const CONST_KEY_SELECT = "选择";
const DEFAULT_EMPTY_VAL = "";

// 1. 读取全局统一字段标签常量数组（无中文硬编码）
const labelJsonRaw = auto.getVar("GLOBAL_TEXT_ARRAY01") || "[]";
let FIELD_CONST_ARR = [];
try {
  FIELD_CONST_ARR = JSON.parse(labelJsonRaw);
} catch (err) {
  auto.log(
    `【常量解析失败】字段标签数组JSON错误，原始：${labelJsonRaw}，报错：${err}`,
  );
  FIELD_CONST_ARR = ["未知1", "未知2", "未知3", "未知4"];
}

// 2. 读取合并后的二维总数据表（替代原来4个独立数组）
const tableJsonRaw = auto.getVar("GLOBAL_TEXT_TABLE") || "[]";
let tableDataArr = [];
try {
  tableDataArr = JSON.parse(tableJsonRaw);
} catch (err) {
  auto.log(
    `【数据表解析失败】二维数据表JSON错误，原始：${tableJsonRaw}，报错：${err}`,
  );
  tableDataArr = [];
}

// 3. 下标映射：仅存字段索引，无任何中文硬编码
const sourceMapping = [
  { fieldIndex: 0 },
  { fieldIndex: 1 },
  { fieldIndex: 2 },
  { fieldIndex: 3 },
];

// 4. 动态生成fieldList，targetKey/label全部取自常量数组
const fieldList = sourceMapping.map((item) => {
  const fieldName = FIELD_CONST_ARR[item.fieldIndex];
  return {
    fieldIndex: item.fieldIndex,
    targetKey: fieldName,
    label: fieldName,
  };
});

// 初始化变量标签（原始逻辑不变）
fieldList.forEach((item) => {
  auto.setVar(item.targetKey, item.label);
});

// ====================== 原脚本校验、分流、赋值逻辑完整保留 ======================
// 基准行数 = 二维数组总行数
const baseArrLen = tableDataArr.length;
let lengthWarning = false;

// 空数据表警告
if (baseArrLen === 0) {
  auto.log(`【警告】合并数据表为空，无法赋值`);
  lengthWarning = true;
}

// 分流上限计算
const maxShunt = AUTO_SHUNT_LIMIT_BY_ARRAY ? baseArrLen : MANUAL_MAX_SHUNT;
const selectNum = Number(auto.getVar(CONST_KEY_SELECT)) || 0;
const realIndex = selectNum - 1;
const assignResult = {};

// 合法选择序号批量赋值（核心逻辑不变，从二维单行取对应列）
if (selectNum >= 1 && selectNum <= maxShunt) {
  // 获取选中整行数据
  const rowData = tableDataArr[realIndex] || [];
  fieldList.forEach((item) => {
    // 从单行中按字段下标取值
    const writeVal = rowData[item.fieldIndex] ?? DEFAULT_EMPTY_VAL;
    assignResult[item.label] = writeVal;
    auto.setVar(item.targetKey, writeVal);
    // 写入校验日志
    const afterWrite = auto.getVar(item.targetKey);
    auto.log(
      `【写入校验】变量[${item.targetKey}]预期值：${writeVal}，实际读取：${afterWrite}`,
    );
  });
} else {
  auto.log(
    `【分流非法】合法范围 1~${maxShunt}，传入选择值：${selectNum}；数据表总行数：${baseArrLen}`,
  );
}

// 配置日志（原样保留）
auto.log(`===== 脚本配置信息 =====`);
auto.log(`自动分流上限开关 = ${AUTO_SHUNT_LIMIT_BY_ARRAY}`);
auto.log(`数据表总行数 = ${baseArrLen}，当前生效最大分流数 = ${maxShunt}`);
auto.log(`分流选择值 selectIndex = ${selectNum}`);

// 单变量详情日志
fieldList.forEach((item) => {
  auto.log(
    `待赋值全局变量名 ${item.targetKey}(${item.label}) = ${assignResult[item.label]}`,
  );
});

// 汇总日志
let logStr = "";
fieldList.forEach((item, idx) => {
  if (idx > 0) logStr += "，";
  logStr += `${item.label}赋值内容 = ${assignResult[item.label]}`;
});
auto.log(logStr);
