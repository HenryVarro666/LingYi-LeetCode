---
title: "3802. 给纸张涂色的方式数量"
aliases: ["yiduobo的每日leetcode 3802.给纸张涂色的方式数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1993010809199162263"
zhihu_id: "1993010809199162263"
zhihu_title: "yiduobo的每日leetcode 3802.给纸张涂色的方式数量"
question_id: "3802"
question: "给纸张涂色的方式数量"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-paint-sheets/"
difficulty: "Hard"
created: "2026-01-09T22:11:37+08:00"
updated: "2026-01-09T22:11:41+08:00"
upvotes: 1
comments: 0
---

# 3802. 给纸张涂色的方式数量

> **[yiduobo的每日leetcode 3802.给纸张涂色的方式数量](https://zhuanlan.zhihu.com/p/1993010809199162263) · 知乎 · 2026-01-09 · 赞同 1**
> 力扣：[3802. 给纸张涂色的方式数量](https://leetcode.cn/problems/number-of-ways-to-paint-sheets/) · Hard · 灵茶山艾府：[排序+相向双指针，O(1) 空间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3802.给纸张涂色的方式数量

[3802. 给纸张涂色的方式数量 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-ways-to-paint-sheets/description/)

题目给出一个整数n，表示纸张的数量。

同时给定一个长度为m的整数数组limit，其中limit[index]表示使用颜色index可以涂色的最大纸张数。

现在要求给所有n张纸涂色：

- 需要恰好使用两种不同的颜色
- 每种颜色必须覆盖连续的一段纸张
- 用颜色index涂的纸张数量不能超过limit[index]

现在要求计算给所有纸张染色的不同方案数量。

首先，对于a、b这两种颜色，若limit[a] + limit[b] \< n，那么就无法使用这两种颜色涂色。

如果在这里不考虑涂色的方案数，而是只考虑可以涂色的颜色对数量，问题就转化成了经典的两数之和，排序后使用两个指针从两侧向中间移动就行了。

因此，一种自然的想法就是将limit先进行排序，然后从前往后枚举涂前半段的颜色p，那么可用的且limit最小的涂后半段的颜色q必然是随着p的增加单调不增的。

接下来考虑如何计算涂色方案数。在计算之前，可以先将所有大于等于n的limit修改为n - 1，理由是必须恰好使用两种颜色，也就是说对于每种颜色对，其中至少有一张纸是某一种颜色涂的，因此另一种颜色最多只能涂n - 1张纸，那么大于等于n的limit就可以先统一修改成n - 1。

对于两种颜色a和b，在这里考虑a涂前半段，b涂后半段的涂色方案数。

如果抛开limit[a]的限制，那么颜色b可以涂色的纸张数量就是1到limit[b]，此时a对应的涂色数量就是n - 1到n - limit[b]。如果加入limit[a]的限制，那么a可用的涂色数量就在n - limit[b]到limit[a]之间，也就是说，一共有limit[a] - (n - limit[b]) + 1种可行的涂色方案。这里有个隐藏的条件是limit[a] + limit[b] >\= n，因此n - limit[b] \<\= limit[a]。

更进一步的，对于当前枚举的颜色p以及其对应的颜色q，此时p实际上可以与q、q + 1、q + 2、...、m - 1这些颜色进行组队，可以得到的总的涂色方案数量就是

(limit[p] - (n - limit[q]) + 1) + (limit[p] - (n - limit[q + 1]) + 1) + ... + (limit[p] - (n - limit[m - 1]) + 1)

将其中的limit[p] - n + 1提出来，就可以写成

(limit[p] - n + 1) \* (m - q) + (limit[q] + limit[q + 1] + ... + limit[m - 1])

也就是说，在这里可以使用一个变量s来维护后面这一项后缀和，随着q的移动同步更新这个s，然后使用s来更新最终答案就行了。

需要特别注意的是，随着p的增大，q可能会变得小于等于p，而对于p和q相等的情况，实际上是不能计算到答案里的，因为这种情况相当于用同一种颜色涂了前半段和后半段。因此在计算时，若limit[p] \* 2 >\= n，就需要将其与自身形成的涂色方案数量从答案中减去，即减去limit[p] - (n - limit[p]) + 1。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, n, limit):
        """
        :type n: int
        :type limit: List[int]
        :rtype: int
        """
        
        for index, v in enumerate(limit):
            limit[index] = min(v, n - 1)

        limit.sort()
        q = len(limit)
        s = 0
        res = 0
        mod = 10 ** 9 + 7
        for p in range(len(limit)):
            while q > 0 and limit[p] + limit[q - 1] >= n:
                q -= 1
                s += limit[q]
            
            res = (res + (limit[p] - n + 1) * (len(limit) - q) % mod + s) % mod
            if limit[p] * 2 >= n:
                res = (res - (limit[p] - (n - limit[p]) + 1) + mod) % mod

        return res
```
