---
title: "508. 出现次数最多的子树元素和"
aliases: ["yiduobo的每日leetcode 508.出现次数最多的子树元素和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/259571989"
zhihu_id: "259571989"
zhihu_title: "yiduobo的每日leetcode 508.出现次数最多的子树元素和"
question_id: "508"
question: "出现次数最多的子树元素和"
problem_url: "https://leetcode.cn/problems/most-frequent-subtree-sum/"
created: "2020-09-26T15:14:49+08:00"
updated: "2020-09-26T15:14:49+08:00"
upvotes: 1
comments: 0
---

# 508. 出现次数最多的子树元素和

> **[yiduobo的每日leetcode 508.出现次数最多的子树元素和](https://zhuanlan.zhihu.com/p/259571989) · 知乎 · 2020-09-26 · 赞同 1**
> 力扣：[508. 出现次数最多的子树元素和](https://leetcode.cn/problems/most-frequent-subtree-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

508.出现次数最多的子树元素和<https://leetcode-cn.com/problems/most-frequent-subtree-sum/>

对于某棵子树，其树中元素之和应该等于这棵树根节点的val加上其左子树元素之和以及右子树元素之和，于是可以优先递归求解其左右子树的元素和，然后再求当前子树的元素和。使用一个dict将这些元素和储存起来，最后一趟扫描找出其中出现次数最多的即为答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def findFrequentTreeSum(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """

        if not root:
            return []

        sum_dict = {}
        self.dfs(root, sum_dict)

        res = []
        max_freq = 0
        for s, cnt in sum_dict.items():
            if cnt > max_freq:
                max_freq = cnt
                res = [s]
            elif cnt == max_freq:
                res.append(s)
        return res

    def dfs(self, now, sum_dict):
        left_sum = right_sum = 0
        if now.left:
            left_sum = self.dfs(now.left, sum_dict)
        if now.right:
            right_sum = self.dfs(now.right, sum_dict)
        now_sum = left_sum + right_sum + now.val
        sum_dict[now_sum] = sum_dict.get(now_sum, 0) + 1
        return now_sum
```
