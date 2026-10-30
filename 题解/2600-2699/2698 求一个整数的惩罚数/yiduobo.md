---
title: "2698. 求一个整数的惩罚数"
aliases: ["yiduobo的每日leetcode 2698.求一个整数的惩罚数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650507898"
zhihu_id: "650507898"
zhihu_title: "yiduobo的每日leetcode 2698.求一个整数的惩罚数"
question_id: "2698"
question: "求一个整数的惩罚数"
problem_url: "https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/"
difficulty: "Medium"
rating: 1679
created: "2023-08-17T00:16:23+08:00"
updated: "2023-08-17T00:16:23+08:00"
upvotes: 0
comments: 0
---

# 2698. 求一个整数的惩罚数

> **[yiduobo的每日leetcode 2698.求一个整数的惩罚数](https://zhuanlan.zhihu.com/p/650507898) · 知乎 · 2023-08-17 · 赞同 0**
> 力扣：[2698. 求一个整数的惩罚数](https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/) · Medium · 灵茶山艾府：[预处理+递归，两种写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2698.求一个整数的惩罚数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/)

题目的数据规模较小，因此可以直接从1到n遍历i，计算i \* i，然后尝试将i \* i拆解成若干个部分并使得这些部分的和为i。对于这个拆解的过程，可以使用动态规划，不过在这里最大的i \* i也不过是10^6，因此我在这里使用的是直接搜索回溯暴力拆解。

最后附上python代码：

```python
class Solution(object):
    def punishmentNumber(self, n):
        """
        :type n: int
        :rtype: int
        """

        def check(level, now, pre, digits, target):
            if level == len(digits):
                return now + pre == target
            
            num = pre * 10 + int(digits[level])
            if check(level + 1, now, num, digits, target):
                return True

            return check(level + 1, now + num, 0, digits, target)

        res = 0
        for i in range(1, n + 1):
            p = i * i
            if check(0, 0, 0, list(str(p)), i):
                res += p
        
        return res
```
