# 2363. 合并相似的物品

Easy · [力扣原题](https://leetcode.cn/problems/merge-similar-items/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](2363%20合并相似的物品%20·%20灵茶山艾府.gif) · [mp4 文件](2363%20合并相似的物品%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](2363%20合并相似的物品%20·%20yiduobo.gif) · [mp4 文件](2363%20合并相似的物品%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![2363 合并相似的物品 · 灵茶山艾府](2363%20合并相似的物品%20·%20灵茶山艾府.gif)

### yiduobo

![2363 合并相似的物品 · yiduobo](2363%20合并相似的物品%20·%20yiduobo.gif)


## 题目描述

给你两个二维整数数组 `items1` 和 `items2` ，表示两个物品集合。每个数组 `items` 有以下特质：

- `items[i] = [value_i, weight_i]` 其中 `value_i` 表示第 `i` 件物品的 **价值** ，`weight_i` 表示第 `i` 件物品的 **重量** 。

- `items` 中每件物品的价值都是 **唯一的** 。

请你返回一个二维数组 `ret`，其中 `ret[i] = [value_i, weight_i]`， `weight_i` 是所有价值为 `value_i`<sub> </sub>物品的 **重量之和** 。

**注意：**`ret` 应该按价值 **升序** 排序后返回。

**示例 1：**

```

输入：items1 = [[1,1],[4,5],[3,8]], items2 = [[3,1],[1,5]]
输出：[[1,6],[3,9],[4,5]]
解释：
value = 1 的物品在 items1 中 weight = 1 ，在 items2 中 weight = 5 ，总重量为 1 + 5 = 6 。
value = 3 的物品在 items1 中 weight = 8 ，在 items2 中 weight = 1 ，总重量为 8 + 1 = 9 。
value = 4 的物品在 items1 中 weight = 5 ，总重量为 5 。
所以，我们返回 [[1,6],[3,9],[4,5]] 。
```

**示例 2：**

```

输入：items1 = [[1,1],[3,2],[2,3]], items2 = [[2,1],[3,2],[1,3]]
输出：[[1,4],[2,4],[3,4]]
解释：
value = 1 的物品在 items1 中 weight = 1 ，在 items2 中 weight = 3 ，总重量为 1 + 3 = 4 。
value = 2 的物品在 items1 中 weight = 3 ，在 items2 中 weight = 1 ，总重量为 3 + 1 = 4 。
value = 3 的物品在 items1 中 weight = 2 ，在 items2 中 weight = 2 ，总重量为 2 + 2 = 4 。
所以，我们返回 [[1,4],[2,4],[3,4]] 。
```

**示例 3：**

```

输入：items1 = [[1,3],[2,2]], items2 = [[7,1],[2,2],[1,4]]
输出：[[1,7],[2,4],[7,1]]
解释：
value = 1 的物品在 items1 中 weight = 3 ，在 items2 中 weight = 4 ，总重量为 3 + 4 = 7 。
value = 2 的物品在 items1 中 weight = 2 ，在 items2 中 weight = 2 ，总重量为 2 + 2 = 4 。
value = 7 的物品在 items2 中 weight = 1 ，总重量为 1 。
所以，我们返回 [[1,7],[2,4],[7,1]] 。
```

**提示：**

- `1 <= items1.length, items2.length <= 1000`

- `items1[i].length == items2[i].length == 2`

- `1 <= value_i, weight_i <= 1000`

- `items1` 中每个 `value_i` 都是 **唯一的** 。

- `items2` 中每个 `value_i` 都是 **唯一的** 。

---
[↑ 返回 2300-2399](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
