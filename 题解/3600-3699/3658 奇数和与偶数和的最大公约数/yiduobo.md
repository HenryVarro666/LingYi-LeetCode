---
title: "3658. 奇数和与偶数和的最大公约数"
aliases: ["yiduobo的每日leetcode 3658.奇数和与偶数和的最大公约数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1949265120640348774"
zhihu_id: "1949265120640348774"
zhihu_title: "yiduobo的每日leetcode 3658.奇数和与偶数和的最大公约数"
question_id: "3658"
question: "奇数和与偶数和的最大公约数"
problem_url: "https://leetcode.cn/problems/gcd-of-odd-and-even-sums/"
difficulty: "Easy"
rating: 1220
created: "2025-09-13T14:31:58+08:00"
updated: "2025-09-13T14:32:02+08:00"
upvotes: 0
comments: 0
---

# 3658. 奇数和与偶数和的最大公约数

> **[yiduobo的每日leetcode 3658.奇数和与偶数和的最大公约数](https://zhuanlan.zhihu.com/p/1949265120640348774) · 知乎 · 2025-09-13 · 赞同 0**
> 力扣：[3658. 奇数和与偶数和的最大公约数](https://leetcode.cn/problems/gcd-of-odd-and-even-sums/) · Easy · 灵茶山艾府：[答案就是 n（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3658.奇数和与偶数和的最大公约数

[3658. 奇数和与偶数和的最大公约数 - 力扣（LeetCode）](https://leetcode.cn/problems/gcd-of-odd-and-even-sums/description/)

题目给出一个整数n，要求计算前n个正奇数之和sumOdd与前n个正偶数之和sumEven的最大公约数是多少。

前n个正奇数之和为1 + 3 + ... + n \* 2 - 1 \= (1 + n \* 2 - 1) \* n / 2 \= n^2

前n个正偶数之和为2 + 4 + ... + n \* 2 \= (2 + n \* 2) \* n / 2 \= n \* (n + 1)

由于n和n + 1必然是互质的，因此以上两个值的最大公约数就是n。

最后附上python代码：

```python
class Solution(object):
    def gcdOfOddEvenSums(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        return n
```
