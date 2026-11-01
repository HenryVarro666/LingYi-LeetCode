# 105. 从前序与中序遍历序列构造二叉树

Medium · [力扣原题](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

所在刷题路径：labuladong、灵神突击、灵神题单·链表树与回溯

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](0105%20从前序与中序遍历序列构造二叉树%20·%20灵茶山艾府.gif) · [mp4 文件](0105%20从前序与中序遍历序列构造二叉树%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](0105%20从前序与中序遍历序列构造二叉树%20·%20yiduobo.gif) · [mp4 文件](0105%20从前序与中序遍历序列构造二叉树%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![0105 从前序与中序遍历序列构造二叉树 · 灵茶山艾府](0105%20从前序与中序遍历序列构造二叉树%20·%20灵茶山艾府.gif)

### yiduobo

![0105 从前序与中序遍历序列构造二叉树 · yiduobo](0105%20从前序与中序遍历序列构造二叉树%20·%20yiduobo.gif)


## 题目描述

给定两个整数数组 `preorder` 和 `inorder` ，其中 `preorder` 是二叉树的**先序遍历**， `inorder` 是同一棵树的**中序遍历**，请构造二叉树并返回其根节点。

**示例 1:**

![](../../_assets/灵茶山艾府/cee2cc9e1f78d716.jpg)

```

输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]
```

**示例 2:**

```

输入: preorder = [-1], inorder = [-1]
输出: [-1]
```

**提示:**

- `1 <= preorder.length <= 3000`

- `inorder.length == preorder.length`

- `-3000 <= preorder[i], inorder[i] <= 3000`

- `preorder` 和 `inorder` 均 **无重复** 元素

- `inorder` 均出现在 `preorder`

- `preorder` **保证** 为二叉树的前序遍历序列

- `inorder` **保证** 为二叉树的中序遍历序列

---
[↑ 返回 0100-0199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
