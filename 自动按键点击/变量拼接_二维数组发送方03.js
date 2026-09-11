try {
    // 从全局变量获取目标存储名称
    let targetVar = auto.getVar("store_var_name") || "table_data_01";

    let selectNum = Number(auto.getVar("选择")) || 0;
    let textList = [];
    for (let i = 0; i < selectNum; i++) {
        let indexStr = i === 0 ? "0" : String(i).padStart(2, "0");
        let keyName = `步序${indexStr}_文`;
        let rawText = auto.getVar(keyName) || "";
        textList.push(rawText);
    }
    let mergedCombineText = textList.join(",");
    auto.setVar(targetVar, mergedCombineText);
    let globalStoreText = auto.getVar(targetVar);
    auto.log(`拼接完成文本[${targetVar}]：${globalStoreText}`);
} catch (err) {
    let targetVar = auto.getVar("store_var_name") || "table_data_01";
    auto.log(`【步序拼接模块异常-${targetVar}】${err.message}`);
}