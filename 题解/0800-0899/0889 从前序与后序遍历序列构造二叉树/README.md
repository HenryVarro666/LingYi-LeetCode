# 889. 从前序与后序遍历序列构造二叉树

Medium · 难度分 1732 · [力扣原题](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-postorder-traversal/)

所在刷题路径：labuladong、灵神题单·链表树与回溯

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0889 从前序与后序遍历序列构造二叉树 · 灵茶山艾府.mp4](0889%20从前序与后序遍历序列构造二叉树%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0889 从前序与后序遍历序列构造二叉树 · yiduobo.mp4](0889%20从前序与后序遍历序列构造二叉树%20·%20yiduobo.mp4) |

## 题目描述

给定两个整数数组，`preorder` 和 `postorder` ，其中 `preorder` 是一个具有 **无重复** 值的二叉树的前序遍历，`postorder` 是同一棵树的后序遍历，重构并返回二叉树。

如果存在多个答案，您可以返回其中 **任何** 一个。

**示例 1：**

![](../../_assets/灵茶山艾府/6b8daf2e3d74e7ca.jpg)

```

输入：preorder = [1,2,4,5,3,6,7], postorder = [4,5,2,6,7,3,1]
输出：[1,2,3,4,5,6,7]
```

**示例 2:**

```

输入: preorder = [1], postorder = [1]
输出: [1]
```

**提示：**

- `1 <= preorder.length <= 30`

- `1 <= preorder[i] <= preorder.length`

- `preorder` 中所有值都 **不同**

- `postorder.length == preorder.length`

- `1 <= postorder[i] <= postorder.length`

- `postorder` 中所有值都 **不同**

- 保证 `preorder` 和 `postorder` 是同一棵二叉树的前序遍历和后序遍历

---
[↑ 返回 0800-0899](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
