auto.setVar("总数据条数", 14);
auto.setVar("runFlag", 0);
auto.setVar("计数", 0);
auto.setVar("已写入计数", 1);
auto.setVar("单次循环上限", 6);
auto.setVar("提前终止本轮循环", 0);
auto.setVar("数据源序号", 0);

// 初始化加载第0组数据源
const source0_text = auto.getVar("source0_text") || "";
auto.setVar("excel_文行列数", source0_text);

auto.log("【初始化完成】数据源序号=0，计数初始0");
