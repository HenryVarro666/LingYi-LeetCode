---
title: "1932. 合并多棵二叉搜索树"
aliases: ["yiduobo的每日leetcode 1932.合并多棵二叉搜索树"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/488089150"
zhihu_id: "488089150"
zhihu_title: "yiduobo的每日leetcode 1932.合并多棵二叉搜索树"
question_id: "1932"
question: "合并多棵二叉搜索树"
problem_url: "https://leetcode.cn/problems/merge-bsts-to-create-single-bst/"
difficulty: "Hard"
rating: 2484
created: "2022-03-26T18:21:14+08:00"
updated: "2022-03-26T18:21:15+08:00"
upvotes: 0
comments: 0
---

# 1932. 合并多棵二叉搜索树

> **[yiduobo的每日leetcode 1932.合并多棵二叉搜索树](https://zhuanlan.zhihu.com/p/488089150) · 知乎 · 2022-03-26 · 赞同 0**
> 力扣：[1932. 合并多棵二叉搜索树](https://leetcode.cn/problems/merge-bsts-to-create-single-bst/) · Hard · 灵茶山艾府：[根据二叉搜索树的性质合并](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1932.合并多棵二叉搜索树

[力扣](https://leetcode-cn.com/problems/merge-bsts-to-create-single-bst/)

题目要求将这n棵二叉树合并成一棵，说明这里其中的n - 1棵二叉树根节点的值必然等于其他二叉树叶子节点的值，而剩下这一棵二叉树的根节点就是合并后最终的根节点。

由于题目保证了每棵数根节点的值不同，那么可以使用哈希表root_dict建立值到节点的唯一映射，方便后续的合并操作。

接下来，收集每个树叶子节点的值。由于这是一颗严格的二叉搜索树，那么树中不能出现两个相同的节点值，因此每个叶子节点的值只能出现一次，在这里就可以使用一个集合收集这些叶子节点的值，并判断是否重复出现。

到了这一步，已经有了叶子节点的值和根节点的值，那么可以遍历所有根节点的值，如果其没有出现在叶子节点值的集合中，说明其对应的根节点就是最终的根节点。当然，如果存在两个或以上这样的节点，那么说明最终无法整合成一棵树，直接返回空即可。

得到了最终的根节点之后，就可以从这个根节点开始向下进行中序遍历。

与常规的中序遍历相比，对于当前节点now：

1、依然是先考察now.left。若now.left存在，那么可能有两种情况：

1-1）now.left.val存在于root_dict中，说明需要将对应的二叉树合并到now.left上，因此更新now.left为root_dict[now.left.val]，并将now.left.val从root_dict中弹出，表示这棵子树已经被合并进来。然后再递归求解now.left

1-2）now.left.val不存在于root_dict中，说明此时的now.left就是个普通的叶子节点，用now.left.val更新中序遍历的结果即可

2、接下来是now本身，直接用now.val更新中序遍历的结果即可

3、最后是now.right。若now.right存在，那么也是两种可能：

3-1）now.right.val存在于root_dict中。与1-1)类似，更新now.right为root_dict[now.right.val]，并将now.right.val从root_dict中弹出，然后递归求解now.right

3-2）now.right.val不存在于root_dict中，说明此时的now.right就是个普通的叶子节点，用now.right.val更新中序遍历的结果即可

中序遍历完成后，若中序遍历的结果不是单调递增的，那么说明最终并不是二叉搜索树，直接返回空。

若最终root_dict中剩下的key大于1个，说明有子树没有被合并进来，此时也是返回空。

其他情况下，说明合并成功，返回最终的根节点。

另外，在这里只是要求中序遍历结果单调递增，因此并不需要全部保存下来，而是使用一个变量保存上一个遍历到的节点的值，然后与当前节点值的大小进行比较即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def canMerge(self, trees):
        """
        :type trees: List[TreeNode]
        :rtype: TreeNode
        """

        root_dict = {}
        leaf_set = set()

        for root in trees:
            root_dict[root.val] = root
            if root.left:
                if root.left.val not in leaf_set:
                    leaf_set.add(root.left.val)
                else:
                    return None
            if root.right:
                if root.right.val not in leaf_set:
                    leaf_set.add(root.right.val)
                else:
                    return None
        
        final_root = None
        for key in root_dict:
            if key not in leaf_set:
                if final_root is None:
                    final_root = root_dict[key]
                else:
                    return None
        
        if final_root is None:
            return None

        self.last_v = 0
        if not self.dfs(final_root, root_dict):
            return None
        if len(root_dict) != 1:
            return None
        return final_root
    
    def dfs(self, now, root_dict):
        if now.left:
            if now.left.val in root_dict:
                now.left = root_dict[now.left.val]
                root_dict.pop(now.left.val)
                if not self.dfs(now.left, root_dict):
                    return False
            elif now.left.val <= self.last_v:
                return False
            else:
                self.last_v = now.left.val

        if now.val <= self.last_v:
            return False
        self.last_v = now.val

        if now.right:
            if now.right.val in root_dict:
                now.right = root_dict[now.right.val]
                root_dict.pop(now.right.val)
                if not self.dfs(now.right, root_dict):
                    return False
            elif now.right.val <= self.last_v:
                return False
            else:
                self.last_v = now.right.val
        
        return True
```
