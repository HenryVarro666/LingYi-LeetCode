---
title: "870. 优势洗牌"
aliases: ["yiduobo的每日leetcode 870.优势洗牌"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350260481"
zhihu_id: "350260481"
zhihu_title: "yiduobo的每日leetcode 870.优势洗牌"
question_id: "870"
question: "优势洗牌"
problem_url: "https://leetcode.cn/problems/advantage-shuffle/"
difficulty: "Medium"
rating: 1648
created: "2021-02-12T20:14:25+08:00"
updated: "2021-02-12T20:14:25+08:00"
upvotes: 0
comments: 0
---

# 870. 优势洗牌

> **[yiduobo的每日leetcode 870.优势洗牌](https://zhuanlan.zhihu.com/p/350260481) · 知乎 · 2021-02-12 · 赞同 0**
> 力扣：[870. 优势洗牌](https://leetcode.cn/problems/advantage-shuffle/) · Medium · 灵茶山艾府：[田忌赛马（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

870.优势洗牌

[力扣](https://leetcode-cn.com/problems/advantage-shuffle/)

田忌赛马问题，思路就是用A的下等牌去对B的上等牌。

将A和B都按从小到大进行排序，使用两个变量l和r来表示当前B中的下等牌和上等牌的下标，然后对排好序的A从头到尾进行一趟扫描，对于当前的A[index]：

1、若A[index] \<\= B[l]，说明A[index]甚至都打不过B的下等牌，于是只能安排A[index]去对上B的上等牌B[r]，然后将r往前移动一位

2、若A[index] > B[l]，那么就让A[index]发挥作用去对上B[l]，然后将l往后移动一位

最后附上python代码：

```python
class Solution(object):
    def advantageCount(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: List[int]
        """

        n = len(A)
        l, r = 0, n - 1
        res = [0] * n
        sorted_B = sorted(zip(B, range(n)), key=lambda d:d[0])
        for num in sorted(A):
            if num > sorted_B[l][0]:
                res[sorted_B[l][1]] = num
                l += 1
            else:
                res[sorted_B[r][1]] = num
                r -= 1
        
        return res
```
