---
title: "2375. 根据模式串构造最小数字"
aliases: ["yiduobo的每日leetcode 2375.根据模式串构造最小数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/三-字符串贪心", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/564125115"
zhihu_id: "564125115"
zhihu_title: "yiduobo的每日leetcode 2375.根据模式串构造最小数字"
question_id: "2375"
question: "根据模式串构造最小数字"
problem_url: "https://leetcode.cn/problems/construct-smallest-number-from-di-string/"
difficulty: "Medium"
rating: 1642
created: "2022-09-14T02:55:51+08:00"
updated: "2022-09-14T02:55:51+08:00"
upvotes: 0
comments: 0
---

# 2375. 根据模式串构造最小数字

> **[yiduobo的每日leetcode 2375.根据模式串构造最小数字](https://zhuanlan.zhihu.com/p/564125115) · 知乎 · 2022-09-14 · 赞同 0**
> 力扣：[2375. 根据模式串构造最小数字](https://leetcode.cn/problems/construct-smallest-number-from-di-string/) · Medium · 灵茶山艾府：[贪心 O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2375.根据模式串构造最小数字

[力扣](https://leetcode.cn/problems/construct-smallest-number-from-di-string/)

由于题目的数字串最多只有9个数字，那么完全可以直接暴力搜索每一种情况，时间复杂度方面是可以勉强过关的。不过题目要找的是最小的数字，那么也可以尝试基于贪心法去构造一组解。

为了使得答案最小，就应该将较小的数字放在靠前的位置，但是这样做有一个问题是对于D，尤其是连续出现的D可能会出现没有数字可用的情况。例如样例二中，出现了连续三个D，就意味着第一个数字必然要从现存数字中第四小的数字开始选起，否则后面的数字就不够了。

另一方面，如果按照选择当前可用的最小且不会影响到连续D的数字来进行填充的话，必然是符合I的要求的。

综合上面两点，说明对于本题，如果基于贪心来做，那么在D出现的时候预留出足够的后续数字，这个预留的大小取决于这一组连续D的数目，而在I出现的时候，则只需将剩余的最小数字填充进去就行了。

可以发现，按上面的方法构造出来的结果就相当于首先按照1到n + 1排列好，然后对于连续D，将D影响到的部分翻转过来就行了。

最后附上python代码：

```python
class Solution(object):
    def smallestNumber(self, pattern):
        """
        :type pattern: str
        :rtype: str
        """

        n = len(pattern)
        res = range(1, n + 2)
        p = 0
        while p < n:
            while p < n and pattern[p] == 'I':
                p += 1
            
            if p == n:
                break

            left = p
            while p < n and pattern[p] == 'D':
                p += 1

            right = p
            while left < right:
                res[left], res[right] = res[right], res[left]
                left += 1
                right -= 1
        
        return ''.join([str(x) for x in res])
```
