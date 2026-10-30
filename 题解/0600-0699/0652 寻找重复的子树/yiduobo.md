---
title: "652. 寻找重复的子树"
aliases: ["yiduobo的每日leetcode 652.寻找重复的子树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/278508148"
zhihu_id: "278508148"
zhihu_title: "yiduobo的每日leetcode 652.寻找重复的子树"
question_id: "652"
question: "寻找重复的子树"
problem_url: "https://leetcode.cn/problems/find-duplicate-subtrees/"
created: "2020-11-07T23:55:05+08:00"
updated: "2020-11-07T23:55:05+08:00"
upvotes: 0
comments: 0
---

# 652. 寻找重复的子树

> **[yiduobo的每日leetcode 652.寻找重复的子树](https://zhuanlan.zhihu.com/p/278508148) · 知乎 · 2020-11-07 · 赞同 0**
> 力扣：[652. 寻找重复的子树](https://leetcode.cn/problems/find-duplicate-subtrees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

652.寻找重复的子树

[力扣](https://leetcode-cn.com/problems/find-duplicate-subtrees/)

对于重复子树问题，我们可以采用dfs得到的笛卡尔序加上字符串匹配的做法来做，不过在这里我才用的是比较偷懒的办法，利用了高级语言强力的哈希表。具体来说就是将每颗子树做成某种数据结构，然后将其放入哈希表。若某棵树在哈希表里面出现大于等于两次，那么就将这棵树的根节点。

对于将数做成某种数据结构，无非就是要保存根节点、左子树、右子树这三样东西的信息。对于根节点而言，其有用的信息只有根节点的值，而对于左右子树，我们则可以通过递归来求解。最后，将这三样东西汇总即可。需要注意必须存在某种先后顺序，用来区分左右子树。我在这里使用的是list按根节点的值，左子树、右子树顺序来进行存储。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def findDuplicateSubtrees(self, root):
        """
        :type root: TreeNode
        :rtype: List[TreeNode]
        """

        tree_dict = {}
        self.res = []
        self.dfs(root, tree_dict)
        return self.res

    def dfs(self, now, tree_dict):
        if now:
            tree_key = (now.val, self.dfs(now.left, tree_dict), self.dfs(now.right, tree_dict))
            tree_dict[tree_key] = tree_dict.get(tree_key, 0) + 1
            if tree_dict[tree_key] == 2:
                self.res.append(now)
            return tree_key
```
