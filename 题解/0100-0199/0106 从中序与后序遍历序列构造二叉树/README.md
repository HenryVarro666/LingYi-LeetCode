# 106. 从中序与后序遍历序列构造二叉树

Medium · [力扣原题](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)

所在刷题路径：labuladong、灵神突击、灵神题单·链表树与回溯

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](0106%20从中序与后序遍历序列构造二叉树%20·%20灵茶山艾府.gif) · [mp4 文件](0106%20从中序与后序遍历序列构造二叉树%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](0106%20从中序与后序遍历序列构造二叉树%20·%20yiduobo.gif) · [mp4 文件](0106%20从中序与后序遍历序列构造二叉树%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![0106 从中序与后序遍历序列构造二叉树 · 灵茶山艾府](0106%20从中序与后序遍历序列构造二叉树%20·%20灵茶山艾府.gif)

### yiduobo

![0106 从中序与后序遍历序列构造二叉树 · yiduobo](0106%20从中序与后序遍历序列构造二叉树%20·%20yiduobo.gif)


## 题目描述

给定两个整数数组 `inorder` 和 `postorder` ，其中 `inorder` 是二叉树的中序遍历， `postorder` 是同一棵树的后序遍历，请你构造并返回这颗 <em>二叉树</em> 。

**示例 1:**

![](../../_assets/灵茶山艾府/cee2cc9e1f78d716.jpg)

```

输入：inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
输出：[3,9,20,null,null,15,7]
```

**示例 2:**

```

输入：inorder = [-1], postorder = [-1]
输出：[-1]
```

**提示:**

- `1 <= inorder.length <= 3000`

- `postorder.length == inorder.length`

- `-3000 <= inorder[i], postorder[i] <= 3000`

- `inorder` 和 `postorder` 都由 **不同** 的值组成

- `postorder` 中每一个值都在 `inorder` 中

- `inorder` **保证**是树的中序遍历

- `postorder` **保证**是树的后序遍历

---
[↑ 返回 0100-0199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
