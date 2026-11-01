# LCR 147. 最小栈

Easy · [力扣原题](https://leetcode.cn/problems/bao-han-minhan-shu-de-zhan-lcof/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](LCR%20147%20最小栈%20·%20灵茶山艾府.gif) · [mp4 文件](LCR%20147%20最小栈%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![LCR 147 最小栈 · 灵茶山艾府](LCR%20147%20最小栈%20·%20灵茶山艾府.gif)


## 题目描述

请你设计一个 **最小栈** 。它提供 `push` ，`pop` ，`top` 操作，并能在常数时间内检索到最小元素的栈。

实现 `MinStack` 类:

- `MinStack()` 初始化堆栈对象。

- `void push(int val)` 将元素val推入堆栈。

- `void pop()` 删除堆栈顶部的元素。

- `int top()` 获取堆栈顶部的元素。

- `int getMin()` 获取堆栈中的最小元素。

**示例 1：**

```

输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]

解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> 返回 -3.
minStack.pop();
minStack.top();      --> 返回 0.
minStack.getMin();   --> 返回 -2.
```

**提示：**

- `-2³¹ <= val <= 2³¹ - 1`

- `pop`、`top` 和 `getMin` 操作总是在 **非空栈** 上调用

- `push`、`pop`、`top` 和 `getMin` 最多被调用 `3 * 10⁴` 次

注意：本题与主站 155 题相同：[https://leetcode.cn/problems/min-stack/](https://leetcode.cn/problems/min-stack/)

---
[↑ 返回 LCR](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
