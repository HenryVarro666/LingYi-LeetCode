---
title: "3483. 不同三位偶数的数目"
aliases: ["yiduobo的每日leetcode 3483.不同三位偶数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/四-回溯", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897405564788658558"
zhihu_id: "1897405564788658558"
zhihu_title: "yiduobo的每日leetcode 3483.不同三位偶数的数目"
question_id: "3483"
question: "不同三位偶数的数目"
problem_url: "https://leetcode.cn/problems/unique-3-digit-even-numbers/"
difficulty: "Easy"
rating: 2094
created: "2025-04-22T21:37:33+08:00"
updated: "2025-04-22T21:37:33+08:00"
upvotes: 0
comments: 0
---

# 3483. 不同三位偶数的数目

> **[yiduobo的每日leetcode 3483.不同三位偶数的数目](https://zhuanlan.zhihu.com/p/1897405564788658558) · 知乎 · 2025-04-22 · 赞同 0**
> 力扣：[3483. 不同三位偶数的数目](https://leetcode.cn/problems/unique-3-digit-even-numbers/) · Easy · 灵茶山艾府：[两种方法：暴力枚举 / 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3483.不同三位偶数的数目

[3483. 不同三位偶数的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/unique-3-digit-even-numbers/description/)

题目给出一个数字数组digits，需要从中选出三个数字组成一个三位偶数，问可以得到的不同三位偶数的数目。

由于题目需要计算的是可以得到的不同三位偶数的数目，那么在这里就可以从100开始到998，以步长为2进行一趟遍历，检测所有的三位偶数能否被构造出来。对于当前遍历到的target，将target中的三个数位都分离出来，然后对比digits中对应的数位是否足够，就可以判断能否构造出target了。

最后附上python代码：

```python
class Solution(object):
    def totalNumbers(self, digits):
        """
        :type digits: List[int]
        :rtype: int
        """
        
        cnt = Counter(digits)
        res = 0
        for target in range(100, 1000, 2):
            first = target // 100
            second = target // 10 % 10
            third = target % 10
            need = Counter([first, second, third])
            flag = True
            for v in need:
                if need[v] > cnt[v]:
                    flag = False
                    break
            
            if flag:
                res += 1

        return res
```
