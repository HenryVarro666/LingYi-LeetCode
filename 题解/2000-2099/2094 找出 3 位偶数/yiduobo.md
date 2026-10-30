---
title: "2094. 找出三位偶数"
aliases: ["yiduobo的每日leetcode 2094.找出三位偶数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/backtracking", "leetcode/enumeration", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/520546135"
zhihu_id: "520546135"
zhihu_title: "yiduobo的每日leetcode 2094.找出三位偶数"
question_id: "2094"
question: "找出 3 位偶数"
problem_url: "https://leetcode.cn/problems/finding-3-digit-even-numbers/"
difficulty: "Easy"
created: "2022-05-27T01:02:33+08:00"
updated: "2022-05-27T01:02:33+08:00"
upvotes: 0
comments: 0
---

# 2094. 找出三位偶数

> **[yiduobo的每日leetcode 2094.找出三位偶数](https://zhuanlan.zhihu.com/p/520546135) · 知乎 · 2022-05-27 · 赞同 0**
> 力扣：[2094. 找出 3 位偶数](https://leetcode.cn/problems/finding-3-digit-even-numbers/) · Easy · 灵茶山艾府：[两种方法：暴力枚举 / 回溯（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2094.找出三位偶数

[力扣](https://leetcode.cn/problems/finding-3-digit-even-numbers/)

题目给出若干数字，要求找出这些数字所能组成的所有不重复的三位偶数。由于三位偶数的数量非常少，那么完全可以直接枚举每个三位偶数，然后将每一位分离出来，并借助哈希表来判断是否有足够的数字可以用来构成当前枚举到的这个三位偶数。

最后附上python代码：

```python
class Solution(object):
    def findEvenNumbers(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """

        digit_dict = {}
        for digit in digits:
            digit_dict[digit] = digit_dict.get(digit, 0) + 1
        
        res = []
        for num in range(100, 1000, 2):
            first = num / 100
            if digit_dict.get(first, 0) > 0:
                digit_dict[first] -= 1
            else:
                continue

            second = num / 10 % 10
            if digit_dict.get(second, 0) > 0:
                digit_dict[second] -= 1
            else:
                digit_dict[first] += 1
                continue

            third = num % 10
            if digit_dict.get(third, 0) > 0:
                res.append(num)
            digit_dict[first] += 1
            digit_dict[second] += 1
        
        return res
```
