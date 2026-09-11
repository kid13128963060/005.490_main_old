//节点9
let total = Number(auto.getVar("总数据条数")) || 0;
let written = Number(auto.getVar("已写入计数")) || 1;
let realDone = written - 1;

if (realDone >= total) {
  auto.setVar("提前终止本轮循环", 1);
} else {
  auto.setVar("提前终止本轮循环", 0);
}

auto.log(
  "【5‑5终止判断】真实完成条数=" +
    realDone +
    "｜总条数=" +
    total +
    "｜提前终止=" +
    auto.getVar("提前终止本轮循环"),
);
