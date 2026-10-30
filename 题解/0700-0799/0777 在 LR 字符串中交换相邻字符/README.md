# 777. 在 LR 字符串中交换相邻字符

Medium · 难度分 2337 · [力扣原题](https://leetcode.cn/problems/swap-adjacent-in-lr-string/)

所在刷题路径：灵神题单·滑动窗口与双指针

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0777 在 LR 字符串中交换相邻字符 · 灵茶山艾府.mp4](0777%20在%20LR%20字符串中交换相邻字符%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0777 在 LR 字符串中交换相邻字符 · yiduobo.mp4](0777%20在%20LR%20字符串中交换相邻字符%20·%20yiduobo.mp4) |

## 题目描述

在一个由 `'L'` , `'R'` 和 `'X'` 三个字符组成的字符串（例如`"RXXLRXRXL"`）中进行移动操作。一次移动操作指用一个 `"LX"` 替换一个 `"XL"`，或者用一个 `"XR"` 替换一个 `"RX"`。现给定起始字符串 `start` 和结束字符串 `result`，请编写代码，当且仅当存在一系列移动操作使得 `start` 可以转换成 `result` 时， 返回 `True`。

**示例 1：**

```

输入：start = "RXXLRXRXL", result = "XRLXXRRLX"
输出：true
解释：通过以下步骤我们可以将 start 转化为 result：
RXXLRXRXL ->
XRXLRXRXL ->
XRLXRXRXL ->
XRLXXRRXL ->
XRLXXRRLX
```

**示例 2：**

```

输入：start = "X", result = "L"
输出：false
```

**提示：**

- `1 <= start.length <= 10⁴`

- `start.length == result.length`

- `start` 和 `result` 都只包含 `'L'`, `'R'` 或 `'X'`。

---
[↑ 返回 0700-0799](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
