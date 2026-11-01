# 1622. 奇妙序列

Hard · 难度分 2476 · [力扣原题](https://leetcode.cn/problems/fancy-sequence/)

所在刷题路径：灵神题单·常用数据结构、灵神题单·贪心与思维

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](1622%20奇妙序列%20·%20灵茶山艾府.gif) · [mp4 文件](1622%20奇妙序列%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](1622%20奇妙序列%20·%20yiduobo.gif) · [mp4 文件](1622%20奇妙序列%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![1622 奇妙序列 · 灵茶山艾府](1622%20奇妙序列%20·%20灵茶山艾府.gif)

### yiduobo

![1622 奇妙序列 · yiduobo](1622%20奇妙序列%20·%20yiduobo.gif)


## 题目描述

请你实现三个 API `append`，`addAll` 和 `multAll` 来实现奇妙序列。

请实现 `Fancy` 类 ：

- `Fancy()` 初始化一个空序列对象。

- `void append(val)` 将整数 `val` 添加在序列末尾。

- `void addAll(inc)` 将所有序列中的现有数值都增加 `inc` 。

- `void multAll(m)` 将序列中的所有现有数值都乘以整数 `m` 。

- `int getIndex(idx)` 得到下标为 `idx` 处的数值（下标从 0 开始），并将结果对 `10⁹ + 7` 取余。如果下标大于等于序列的长度，请返回 `-1` 。

**示例：**

```

输入：
["Fancy", "append", "addAll", "append", "multAll", "getIndex", "addAll", "append", "multAll", "getIndex", "getIndex", "getIndex"]
[[], [2], [3], [7], [2], [0], [3], [10], [2], [0], [1], [2]]
输出：
[null, null, null, null, null, 10, null, null, null, 26, 34, 20]

解释：
Fancy fancy = new Fancy();
fancy.append(2);   // 奇妙序列：[2]
fancy.addAll(3);   // 奇妙序列：[2+3] -> [5]
fancy.append(7);   // 奇妙序列：[5, 7]
fancy.multAll(2);  // 奇妙序列：[5*2, 7*2] -> [10, 14]
fancy.getIndex(0); // 返回 10
fancy.addAll(3);   // 奇妙序列：[10+3, 14+3] -> [13, 17]
fancy.append(10);  // 奇妙序列：[13, 17, 10]
fancy.multAll(2);  // 奇妙序列：[13*2, 17*2, 10*2] -> [26, 34, 20]
fancy.getIndex(0); // 返回 26
fancy.getIndex(1); // 返回 34
fancy.getIndex(2); // 返回 20
```

**提示：**

- `1 <= val, inc, m <= 100`

- `0 <= idx <= 10⁵`

- 总共最多会有 `10⁵` 次对 `append`，`addAll`，`multAll` 和 `getIndex` 的调用。

---
[↑ 返回 1600-1699](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
