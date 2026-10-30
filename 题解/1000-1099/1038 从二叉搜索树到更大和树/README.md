# 1038. 从二叉搜索树到更大和树

Medium · [力扣原题](https://leetcode.cn/problems/binary-search-tree-to-greater-sum-tree/)

所在刷题路径：labuladong、灵神题单·链表树与回溯

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 1038 从二叉搜索树到更大和树 · 灵茶山艾府.mp4](1038%20从二叉搜索树到更大和树%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 题目描述

给定一个二叉搜索树 `root` (BST)，请将它的每个节点的值替换成树中大于或者等于该节点值的所有节点值之和。

提醒一下， <em>二叉搜索树</em> 满足下列约束条件：

- 节点的左子树仅包含键 **小于** 节点键的节点。

- 节点的右子树仅包含键 **大于** 节点键的节点。

- 左右子树也必须是二叉搜索树。

**示例 1：**

![](../../_assets/灵茶山艾府/40de3af1bd3ce0bf.png)

```

输入：[4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
输出：[30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
```

**示例 2：**

```

输入：root = [0,null,1]
输出：[1,null,1]
```

**提示：**

- 树中的节点数在 `[1, 100]` 范围内。

- `0 <= Node.val <= 100`

- 树中的所有值均 **不重复** 。

**注意：**该题目与 538: [https://leetcode.cn/problems/convert-bst-to-greater-tree/  ](https://leetcode.cn/problems/convert-bst-to-greater-tree/)相同

---
[↑ 返回 1000-1099](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
