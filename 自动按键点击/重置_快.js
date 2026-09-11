auto.setVar("脚本模块_选择","Js模块");
auto.setVar("gKey_scriptModuleSelect","变量批量一维赋值");

try {
    // 1. 标签列表，拼接为纯逗号分隔字符串存入gKey_varAddOne01（不JSON序列化）
    let labelList = [
        "节点深度",
        "节点类名",
        "应用包名",
        "节点ID",
        "步序01_节点深度",
"步序01_节点类名",
"步序01_节点ID",
"gKey_varAddOne01",
"gKey_varAddOne02",
    ];
    let labelRawStr = labelList.join(",");
    auto.setVar("gKey_varAddOne01", labelRawStr);
    auto.log("标签原始拼接文本：" + labelRawStr);

    // 2. 单条一维业务数据，拼接逗号分隔纯文本存入gKey_varAddOne02
    let singleDataArr = [
        0,
        "1Js模块",
        "2Js模块",
        "3Js模块",
        0,
        "5Js模块",
        "6Js模块",
        "7Js模块",
        "8Js模块",
    ];
    let dataRawStr = singleDataArr.join(",");
    auto.setVar("gKey_varAddOne02", dataRawStr);
    auto.log("一维数据原始拼接文本：" + dataRawStr);

    auto.log("【源数组发送脚本执行完成】gKey_varAddOne01/gKey_varAddOne02均为未序列化逗号字符串");
} catch (err) {
    auto.log("【源数组发送模块异常】" + err.message);
}