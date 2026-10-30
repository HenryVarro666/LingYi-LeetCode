---
title: "2709. 最大公约数遍历"
aliases: ["yiduobo的每日leetcode 2709.最大公约数遍历"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651045903"
zhihu_id: "651045903"
zhihu_title: "yiduobo的每日leetcode 2709.最大公约数遍历"
question_id: "2709"
question: "最大公约数遍历"
problem_url: "https://leetcode.cn/problems/greatest-common-divisor-traversal/"
created: "2023-08-19T18:00:24+08:00"
updated: "2023-08-19T18:00:24+08:00"
upvotes: 0
comments: 0
---

# 2709. 最大公约数遍历

> **[yiduobo的每日leetcode 2709.最大公约数遍历](https://zhuanlan.zhihu.com/p/651045903) · 知乎 · 2023-08-19 · 赞同 0**
> 力扣：[2709. 最大公约数遍历](https://leetcode.cn/problems/greatest-common-divisor-traversal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2709.最大公约数遍历

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/greatest-common-divisor-traversal/)

首先考虑特殊情况。若数组存在1，由于1和其他正整数的最大公约数必然为1，因此这个1就无法与数组中的其他位置连通，那么只有当数组中仅存在这个1时答案才为true，否则由于其他位置无法到达这个1，答案就是false。

接下来考虑一般情况。由于数组长度的规模不小，因此O(n^2)的暴力枚举是行不通的。注意到数组中的数取值范围在10^5之内，因此在这里可以通过筛法来计算下标间的连通关系。

具体来说，就是在筛法求素数的过程中，一边通过素数的倍数更新合数，一边将这些合数通过并查集连通到一起来。筛法结束后，若最终所有数都被连通到了一起，也就是所有数的父亲节点都相同，那么答案就是true，否则就是false。

最后附上python代码：

```python
class Solution(object):
    def canTraverseAllPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        distinct_nums = []
        index_dict = {}
        mi = 10 ** 5
        ma = 0
        for v in nums:
            mi = min(mi, v)
            ma = max(ma, v)
            if v not in index_dict:
                index_dict[v] = len(distinct_nums)
                distinct_nums.append(v)

        if mi == 1:
            return len(nums) == 1

        prime = [True] * (ma + 1)
        p = 2
        fa = range(len(distinct_nums) + 1)

        def find(x):
            if fa[x] != x:
                return find(fa[x])
            return fa[x]

        for p in range(2, ma + 1):
            if prime[p]:
                fa_p = None
                if p in index_dict:
                    fa_p = find(index_dict[p])
                for x in range(p + p, ma + 1, p):
                    prime[x] = False
                    if x in index_dict:
                        fa_x = find(index_dict[x])
                        if fa_p is None:
                            fa_p = fa_x
                        else:
                            fa[fa_x] = fa_p

        fa_x = find(0)
        for index in range(1, len(distinct_nums)):
            if find(index) != fa_x:
                return False
        return True
```
