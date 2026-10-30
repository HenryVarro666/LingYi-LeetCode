---
title: "455. 分发饼干"
aliases: ["yiduobo的每日leetcode 455.分发饼干"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/216567803"
zhihu_id: "216567803"
zhihu_title: "yiduobo的每日leetcode 455.分发饼干"
question_id: "455"
question: "分发饼干"
problem_url: "https://leetcode.cn/problems/assign-cookies/"
difficulty: "Easy"
rating: 1381
created: "2020-09-05T00:04:13+08:00"
updated: "2020-09-05T00:04:13+08:00"
upvotes: 0
comments: 0
---

# 455. 分发饼干

> **[yiduobo的每日leetcode 455.分发饼干](https://zhuanlan.zhihu.com/p/216567803) · 知乎 · 2020-09-05 · 赞同 0**
> 力扣：[455. 分发饼干](https://leetcode.cn/problems/assign-cookies/) · Easy · 灵茶山艾府：[排序+双指针，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

455.分发饼干<https://leetcode-cn.com/problems/assign-cookies/>

题目要求满足尽可能多的孩子，那么应该优先满足对饼干需求少的孩子，于是可以对孩子需要的饼干数从小到大排序。对于某个孩子而言，使用刚刚好能满足这个孩子的饼干数是性价比最高的，因此也可以对饼干数进行排序，然后尽量用少的饼干去满足孩子。

于是现在的做法就是分别对g和s进行排序，然后两个指针分别从g和s的头部往后扫描，若当前的g小于等于s，说明当前孩子可以被当前饼干满足，于是将其配对并考察下一个孩子，否则将s往后移动，考察下一份饼干。

最后附上python代码：

```python
class Solution(object):
    def findContentChildren(self, g, s):
        """
        :type g: List[int]
        :type s: List[int]
        :rtype: int
        """

        g = sorted(g)
        s = sorted(s)

        i = 0
        j = 0
        res = 0
        while i < len(g) and j < len(s):
            if g[i] <= s[j]:
                res += 1
                i += 1
            j += 1

        return res
```
