auto.setVar("选择", 1);

try {
    // =====================【第二阶段：标签文本预处理，生成标签数组】=====================
    let rawText = auto.getVar("gKey_varAddOne01") || "";
    auto.log(`【标签源文本】${rawText}`);

    // 分割+去空格+过滤空字符
    let splitList = rawText.split(",").map(s => s.trim()).filter(Boolean);
    let labelArr = splitList.map(item => item.replace(/^"+|"+$/g, ""));

    auto.log(`【清洗后标签数组】${JSON.stringify(labelArr)}`);
    auto.setVar("GLOBAL_TEXT_ARRAY01", JSON.stringify(labelArr));

    // =====================【第三阶段：解析二维数据表】=====================
    let rawDataText = auto.getVar("gKey_varAddOne02") || "";
    auto.log(`【数据表源文本】${rawDataText}`);

    let rowStrArr = rawDataText.split("|").map(s => s.trim()).filter(Boolean);
    let twoDimensionTable = rowStrArr.map(row => row.split(",").map(cell => cell.trim()));

    auto.log(`【解析后二维表格】${JSON.stringify(twoDimensionTable)}`);
    auto.setVar("GLOBAL_TEXT_ARRAY02", JSON.stringify(twoDimensionTable));

    // =====================【第四阶段：分流赋值逻辑】=====================
    let selectIndex = Number(auto.getVar("选择")) || 1;
    let arrIndex = selectIndex - 1;
    auto.log(`【当前选中行号】原始选择值${selectIndex}，数组下标${arrIndex}`);

    // 下标越界拦截
    if (arrIndex < 0 || arrIndex >= twoDimensionTable.length) {
        auto.log("警告：选择序号超出数据表总行范围，终止赋值");
    } else {
        let targetRowData = twoDimensionTable[arrIndex];
        auto.log(`【待赋值行数据】${JSON.stringify(targetRowData)}`);

        // 字段循环批量赋值
        for (let i = 0; i < labelArr.length; i++) {
            let fieldName = labelArr[i];
            let fieldValue = targetRowData[i];

            // 节点深度强制转数字
            if (fieldName === "节点深度") {
                fieldValue = Number(fieldValue);
            }

            auto.setVar(fieldName, fieldValue);
            auto.setVar(`步序01_${fieldName}`, fieldValue);
            auto.log(`赋值完成 | ${fieldName} = ${fieldValue}`);
            auto.log(`赋值完成 | 步序01_${fieldName} = ${fieldValue}`);
        }
    }

    auto.log("==========解析赋值模块执行完毕==========");
} catch (err) {
    auto.log(`【解析赋值模块异常】${err.message}`);
}
let text0 = auto.getVar("节点深度");
auto.log("我读取到的内容："+ text0);
let text01 = auto.getVar("节点类名");
auto.log("我读取到的内容："+ text01);