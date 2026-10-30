# 1261. 在受污染的二叉树中查找元素

Medium · 难度分 1440 · [力扣原题](https://leetcode.cn/problems/find-elements-in-a-contaminated-binary-tree/)

所在刷题路径：灵神题单·位运算、灵神题单·链表树与回溯

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 1261 在受污染的二叉树中查找元素 · 灵茶山艾府.mp4](1261%20在受污染的二叉树中查找元素%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 1261 在受污染的二叉树中查找元素 · yiduobo.mp4](1261%20在受污染的二叉树中查找元素%20·%20yiduobo.mp4) |

## 题目描述

给出一个满足下述规则的二叉树：

1. `root.val == 0`

2. 对于任意 `treeNode`：

    1. 如果 `treeNode.val` 为 `x` 且 `treeNode.left != null`，那么 `treeNode.left.val == 2 * x + 1`

    2. 如果 `treeNode.val` 为 `x` 且 `treeNode.right != null`，那么 `treeNode.right.val == 2 * x + 2`

现在这个二叉树受到「污染」，所有的 `treeNode.val` 都变成了 `-1`。

请你先还原二叉树，然后实现 `FindElements` 类：

- `FindElements(TreeNode* root)` 用受污染的二叉树初始化对象，你需要先把它还原。

- `bool find(int target)` 判断目标值 `target` 是否存在于还原后的二叉树中并返回结果。

**示例 1：**

![](../../_assets/灵茶山艾府/9047b1eb48eaaaaf.jpg)

```

输入：
["FindElements","find","find"]
[[[-1,null,-1]],[1],[2]]
输出：
[null,false,true]
解释：
FindElements findElements = new FindElements([-1,null,-1]);
findElements.find(1); // return False
findElements.find(2); // return True
```

**示例 2：**

![](../../_assets/灵茶山艾府/57c41e8cd097db7f.jpg)

```

输入：
["FindElements","find","find","find"]
[[[-1,-1,-1,-1,-1]],[1],[3],[5]]
输出：
[null,true,true,false]
解释：
FindElements findElements = new FindElements([-1,-1,-1,-1,-1]);
findElements.find(1); // return True
findElements.find(3); // return True
findElements.find(5); // return False
```

**示例 3：**

![](../../_assets/灵茶山艾府/5ee1345f52e3f8fd.jpg)

```

输入：
["FindElements","find","find","find","find"]
[[[-1,null,-1,-1,null,-1]],[2],[3],[4],[5]]
输出：
[null,true,false,false,true]
解释：
FindElements findElements = new FindElements([-1,null,-1,-1,null,-1]);
findElements.find(2); // return True
findElements.find(3); // return False
findElements.find(4); // return False
findElements.find(5); // return True
```

**提示：**

- `TreeNode.val == -1`

- 二叉树的高度不超过 `20`

- 节点的总数在 `[1, 10⁴]` 之间

- 调用 `find()` 的总次数在 `[1, 10⁴]` 之间

- `0 <= target <= 10⁶`

---
[↑ 返回 1200-1299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
