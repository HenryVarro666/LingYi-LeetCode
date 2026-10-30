---
title: "LCP 34. 二叉树染色"
aliases: ["yiduobo的每日leetcode LCP34.二叉树染色"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574592607"
zhihu_id: "574592607"
zhihu_title: "yiduobo的每日leetcode LCP34.二叉树染色"
question_id: "LCP 34"
question: "二叉树染色"
problem_url: "https://leetcode.cn/problems/er-cha-shu-ran-se-/"
created: "2022-10-18T02:35:34+08:00"
updated: "2022-10-18T02:35:34+08:00"
upvotes: 1
comments: 0
---

# LCP 34. 二叉树染色

> **[yiduobo的每日leetcode LCP34.二叉树染色](https://zhuanlan.zhihu.com/p/574592607) · 知乎 · 2022-10-18 · 赞同 1**
> 力扣：[LCP 34. 二叉树染色](https://leetcode.cn/problems/er-cha-shu-ran-se-/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP34.二叉树染色

[力扣](https://leetcode.cn/problems/er-cha-shu-ran-se-UGC/)

经典的树形动态规划问题，先来分析一下蓝色块的构成。

如果色块只位于单侧的子树中，那么可以先默认问题在子树的递归求解中已经解决了，现在需要解决是包含当前子树根节点的色块。由于题目中的k规模很小，那么完全可以将其表示在状态中，即f[now][cnt]表示以now为根节点，且包含根节点的蓝色块大小为cnt时，子树中蓝色节点的最大和。那么对于f[now]，首先递归求解左右子树，得到f[left]和f[right]，接下来：

1、可以选择不对now进行染色，此时就有f[now][0] \= max(f[left]) + max(f[right])

2、如果要对now进行染色，那么最终染色块的构成必然是now、左子树中包含now.left的染色块、右子树中包含now.right的染色块三个部分构成。在这里可以直接枚举左右子树染色块的大小left_cnt和right_cnt，那么就有f[now][left_cnt + right_cnt + 1] \= max(f[now][left_cnt + right_cnt + 1], f[left][left_cnt] + f[right][right_cnt] + now.val)，在这里需要满足left_cnt + right_cnt + 1 \<\= k

从root开始向下递归求解，完成后max(f[root])就是最终答案了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def maxValue(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """

        def dfs(now):
            if now.left:
                left_res = dfs(now.left)
            else:
                left_res = [0] * k
            
            if now.right:
                right_res = dfs(now.right)
            else:
                right_res = [0] * k
            
            res = [max(left_res) + max(right_res)]
            for cnt in range(1, k + 1):
                res.append(0)
                for left_cnt in range(cnt):
                    res[-1] = max(res[-1], left_res[left_cnt] + right_res[cnt - left_cnt - 1] + now.val)

            return res

        return max(dfs(root))
```
