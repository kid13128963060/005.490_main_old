try {
    // =====================【第二阶段：标签文本预处理，生成标签数组】=====================
    let rawText = auto.getVar("gKey_varAddOne01") || "";
    auto.log(`【标签源文本】${rawText}`);

    let splitList = rawText.split(",").map(s => s.trim()).filter(Boolean);
    let labelArr = splitList.map(item => item.replace(/^"+|"+$/g, ""));

    auto.log(`【清洗后标签数组】${JSON.stringify(labelArr)}`);
    auto.setVar("GLOBAL_TEXT_ARRAY01", JSON.stringify(labelArr));

    // =====================【第三阶段：解析一维数组】=====================
    let rawDataText = auto.getVar("gKey_varAddOne02") || "";
    auto.log(`【数据表源文本】${rawDataText}`);

    let firstRowStr = rawDataText.split("|").map(s => s.trim()).filter(Boolean)[0] || "";
    let oneDimensionArr = firstRowStr.split(",").map(cell => cell.trim());

    auto.log(`【解析后一维数组】${JSON.stringify(oneDimensionArr)}`);
    auto.setVar("GLOBAL_TEXT_ARRAY02", JSON.stringify(oneDimensionArr));

    // =====================【第四阶段：批量赋值逻辑（修复核心）】=====================
    auto.log(`【待赋值一维数组数据】${JSON.stringify(oneDimensionArr)}`);

    for (let i = 0; i < labelArr.length; i++) {
        let fieldName = labelArr[i];
        let fieldValue = oneDimensionArr[i];

        // 节点深度强制转数字
        if (fieldName === "节点深度" || fieldName === "步序01_节点深度") {
            fieldValue = Number(fieldValue);
        }

        // 重点修复：只赋值一次，fieldName本身已经包含前缀，不再额外拼接前缀！
        auto.setVar(fieldName, fieldValue);
        auto.log(`赋值完成 | ${fieldName} = ${fieldValue}`);
    }

    auto.log("==========解析赋值模块执行完毕==========");
} catch (err) {
    auto.log(`【解析赋值模块异常】${err.message}`);
}
