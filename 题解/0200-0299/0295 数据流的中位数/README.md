# 295. 数据流的中位数

Hard · [力扣原题](https://leetcode.cn/problems/find-median-from-data-stream/)

所在刷题路径：labuladong、灵神突击、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0295 数据流的中位数 · 灵茶山艾府.mp4](0295%20数据流的中位数%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0295 数据流的中位数 · yiduobo.mp4](0295%20数据流的中位数%20·%20yiduobo.mp4) |

## 题目描述

**中位数**是有序整数列表中的中间值。如果列表的大小是偶数，则没有中间值，中位数是两个中间值的平均值。

- 例如 `arr = [2,3,4]` 的中位数是 `3` 。

- 例如 `arr = [2,3]` 的中位数是 `(2 + 3) / 2 = 2.5` 。

实现 MedianFinder 类:

-

`MedianFinder()` 初始化 `MedianFinder` 对象。

-

`void addNum(int num)` 将数据流中的整数 `num` 添加到数据结构中。

-

`double findMedian()` 返回到目前为止所有元素的中位数。与实际答案相差 `10⁻⁵` 以内的答案将被接受。

**示例 1：**

```

输入
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
输出
[null, null, null, 1.5, null, 2.0]

解释
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // 返回 1.5 ((1 + 2) / 2)
medianFinder.addNum(3);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

**提示:**

- `-10⁵ <= num <= 10⁵`

- 在调用 `findMedian` 之前，数据结构中至少有一个元素

- 最多 `5 * 10⁴` 次调用 `addNum` 和 `findMedian`

---
[↑ 返回 0200-0299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
