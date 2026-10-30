# 155. 最小栈

Medium · [力扣原题](https://leetcode.cn/problems/min-stack/)

所在刷题路径：labuladong、灵神核心路线、灵神突击、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0155 最小栈 · 灵茶山艾府.mp4](0155%20最小栈%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0155 最小栈 · yiduobo.mp4](0155%20最小栈%20·%20yiduobo.mp4) |

## 题目描述

设计一个支持 `push` ，`pop` ，`top` 操作，并能在常数时间内检索到最小元素的栈。

实现 `MinStack` 类:

- `MinStack()` 初始化堆栈对象。

- `void push(int value)` 将元素 `value` 推入堆栈。

- `void pop()` 删除堆栈顶部的元素。

- `int top()` 获取堆栈顶部的元素。

- `int getMin()` 获取堆栈中的最小元素。

**示例 1:**

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

- `push`, `pop`, `top`, and `getMin`最多被调用 `3 * 10⁴` 次

---
[↑ 返回 0100-0199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
