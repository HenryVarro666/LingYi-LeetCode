---
title: "3233. 统计不是特殊数字的数字数量"
aliases: ["yiduobo的每日leetcode 3233.统计不是特殊数字的数字数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720353226"
zhihu_id: "720353226"
zhihu_title: "yiduobo的每日leetcode 3233.统计不是特殊数字的数字数量"
question_id: "3233"
question: "统计不是特殊数字的数字数量"
problem_url: "https://leetcode.cn/problems/find-the-count-of-numbers-which-are-not-special/"
difficulty: "Medium"
rating: 1509
created: "2024-09-15T22:07:55+08:00"
updated: "2024-09-15T22:07:55+08:00"
upvotes: 1
comments: 0
---

# 3233. 统计不是特殊数字的数字数量

> **[yiduobo的每日leetcode 3233.统计不是特殊数字的数字数量](https://zhuanlan.zhihu.com/p/720353226) · 知乎 · 2024-09-15 · 赞同 1**
> 力扣：[3233. 统计不是特殊数字的数字数量](https://leetcode.cn/problems/find-the-count-of-numbers-which-are-not-special/) · Medium · 灵茶山艾府：[预处理质数+O(1)回答（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3233.统计不是特殊数字的数字数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-count-of-numbers-which-are-not-special/)

题目定于对于任意整数x，除了x自身之外的其他正因数都是x的真因数。若一个数字恰好有两个真因数，那么就称该数字为特殊数字。现在给出两个正整数l和r，问l到r之间有多少个数不是特殊数字。

要计算不是特殊数字的数量，可以反过来计算l到r之间特殊数字的数量，然后用r - l + 1减去特殊数字的数量即为最终答案。

而对于特殊数字而言，首先可以明确的是特殊数字必然不会是1，也不会是质数，因为1没有真因数，而质数只有唯一的真因数1。

接下来对于任意合数x，如果x是特殊数字，就说明x除了1和其自身以外只能有一个因子p。

这里的p必然是个质数，否则p的任意真因数也会是x的正因数，同时p必然等于x除以p，否则x除以p就是x除了p之外的的另一个真因数。

综合起来就可以发现，所有的特殊数字必然是某个质数的平方。

根据上面的结论，就可以从sqrt(l)开始枚举到sqrt(r)，计算期间质数的数量，然后用r - l + 1减去这个数量即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def nonSpecialCount(self, l, r):
        """
        :type l: int
        :type r: int
        :rtype: int
        """

        res = r - l + 1
        for x in range(int(sqrt(l)), int(sqrt(r)) + 1):
            if x < 2:
                continue
            y = 2
            prime = True
            while y * y <= x:
                if x % y == 0:
                    prime = False
                    break
                y += 1
            
            if prime and l <= x * x <= r:
                res -= 1
        
        return res
```
