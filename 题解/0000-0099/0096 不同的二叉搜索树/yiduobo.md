---
title: "96. 不同的二叉搜索树"
aliases: ["yiduobo的每日leetcode 96.不同的二叉搜索树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137318258"
zhihu_id: "137318258"
zhihu_title: "yiduobo的每日leetcode 96.不同的二叉搜索树"
question_id: "96"
question: "不同的二叉搜索树"
problem_url: "https://leetcode.cn/problems/unique-binary-search-trees/"
created: "2020-04-29T21:33:09+08:00"
updated: "2020-04-29T21:33:09+08:00"
upvotes: 0
comments: 0
---

# 96. 不同的二叉搜索树

> **[yiduobo的每日leetcode 96.不同的二叉搜索树](https://zhuanlan.zhihu.com/p/137318258) · 知乎 · 2020-04-29 · 赞同 0**
> 力扣：[96. 不同的二叉搜索树](https://leetcode.cn/problems/unique-binary-search-trees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

96.不同的二叉搜索树<https://leetcode-cn.com/problems/unique-binary-search-trees/>

上一题的简化版本，当然也可以用上一题的方法来做。

f[i]代表i个节点能形成多少颗不同的二叉树，那么就有

f[i] \= f[0] \* f[i - 1] + f[1] \* f[i - 2] + ... + f[i - 1] \* f[0]

其中当i为0或1时，f[i] \= 1。

这样做的具体含义遇上一题的做法一样，即依次选择根节点，然后将左右子树的所有可能情况进行组合后相加。

上面这个式子被称作卡特兰数，其递推公式为f[i + 1] \= f[i] \* 2 \* (2 \* i + 1) / (i + 2)。具体的推算过程比较复杂，这里就不展开了。

于是最后也可以直接递推计算出结果。

最后附上python代码：

```python
class Solution(object):
    def numTrees(self, n):
        """
        :type n: int
        :rtype: int
        """

        f = 1
        for index in range(1, n):
            f = f * 2 * (index + index + 1) / (index + 2)
        return f
```
