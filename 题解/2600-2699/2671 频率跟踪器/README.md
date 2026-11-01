# 2671. 频率跟踪器

Medium · [力扣原题](https://leetcode.cn/problems/frequency-tracker/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](2671%20频率跟踪器%20·%20灵茶山艾府.gif) · [mp4 文件](2671%20频率跟踪器%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](2671%20频率跟踪器%20·%20yiduobo.gif) · [mp4 文件](2671%20频率跟踪器%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![2671 频率跟踪器 · 灵茶山艾府](2671%20频率跟踪器%20·%20灵茶山艾府.gif)

### yiduobo

![2671 频率跟踪器 · yiduobo](2671%20频率跟踪器%20·%20yiduobo.gif)


## 题目描述

请你设计并实现一个能够对其中的值进行跟踪的数据结构，并支持对频率相关查询进行应答。

实现 `FrequencyTracker` 类：

- `FrequencyTracker()`：使用一个空数组初始化 `FrequencyTracker` 对象。

- `void add(int number)`：添加一个 `number` 到数据结构中。

- `void deleteOne(int number)`：从数据结构中删除一个 `number` 。数据结构 **可能不包含** `number` ，在这种情况下不删除任何内容。

- `bool hasFrequency(int frequency)`: 如果数据结构中存在出现 `frequency` 次的数字，则返回 `true`，否则返回 `false`。

**示例 1：**

```

输入
["FrequencyTracker", "add", "add", "hasFrequency"]
[[], [3], [3], [2]]
输出
[null, null, null, true]

解释
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(3); // 数据结构现在包含 [3]
frequencyTracker.add(3); // 数据结构现在包含 [3, 3]
frequencyTracker.hasFrequency(2); // 返回 true ，因为 3 出现 2 次
```

**示例 2：**

```

输入
["FrequencyTracker", "add", "deleteOne", "hasFrequency"]
[[], [1], [1], [1]]
输出
[null, null, null, false]

解释
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.add(1); // 数据结构现在包含 [1]
frequencyTracker.deleteOne(1); // 数据结构现在为空 []
frequencyTracker.hasFrequency(1); // 返回 false ，因为数据结构为空
```

**示例 3：**

```

输入
["FrequencyTracker", "hasFrequency", "add", "hasFrequency"]
[[], [2], [3], [1]]
输出
[null, false, null, true]

解释
FrequencyTracker frequencyTracker = new FrequencyTracker();
frequencyTracker.hasFrequency(2); // 返回 false ，因为数据结构为空
frequencyTracker.add(3); // 数据结构现在包含 [3]
frequencyTracker.hasFrequency(1); // 返回 true ，因为 3 出现 1 次
```

**提示：**

- `1 <= number <= 10⁵`

- `1 <= frequency <= 10⁵`

- 最多调用 `add`、`deleteOne` 和 `hasFrequency` **共计** `2 * 10⁵` 次

---
[↑ 返回 2600-2699](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
