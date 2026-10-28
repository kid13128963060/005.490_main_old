// 通用解析函数
function parseNumberList(text) {
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
        arr = raw.split(",")
            .map(item => Number(item.trim()))
            .filter(n => !isNaN(n));
    }
    return arr;
}

// 读取数据源文本，生成arr数组（缺失的关键代码）
let rawText = auto.getVar("excel_文行列数") || "";
let arr = parseNumberList(rawText);

// 你文档中原有的逻辑
let index = Number(auto.getVar("计数")) || 0;
let targetRow;
if(arr.length > 0 && index >= 0 && index < arr.length){
    targetRow = arr[index];
}else{
    targetRow = 0;
}
auto.setVar("步序0_行数", targetRow);
