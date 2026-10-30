---
title: "2048. 下一个更大的数值平衡数"
aliases: ["yiduobo的每日leetcode 2048.下一个更大的数值平衡数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/bao-li", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/511261013"
zhihu_id: "511261013"
zhihu_title: "yiduobo的每日leetcode 2048.下一个更大的数值平衡数"
question_id: "2048"
question: "下一个更大的数值平衡数"
problem_url: "https://leetcode.cn/problems/next-greater-numerically-balanced-number/"
difficulty: "Medium"
created: "2022-05-08T22:14:42+08:00"
updated: "2022-05-08T22:14:43+08:00"
upvotes: 0
comments: 0
---

# 2048. 下一个更大的数值平衡数

> **[yiduobo的每日leetcode 2048.下一个更大的数值平衡数](https://zhuanlan.zhihu.com/p/511261013) · 知乎 · 2022-05-08 · 赞同 0**
> 力扣：[2048. 下一个更大的数值平衡数](https://leetcode.cn/problems/next-greater-numerically-balanced-number/) · Medium · 灵茶山艾府：[两种方法：枚举 / 倒序贪心 + 0-1 背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2048.下一个更大的数值平衡数

[力扣](https://leetcode-cn.com/problems/next-greater-numerically-balanced-number/)

乍一看感觉是数位动态规划的问题，不过在这里n的范围比较小，在这个范围内的数值平衡数应该是比较少的，完全可以暴力计算或者打表。我在这里采用的是手动输入几种初始情况，然后利用全排列来得到所有的数值平衡数，然后将这些数收集起来后排序得到数值平衡数的表，再一趟遍历找出大于n的下一个数值平衡数。

最后附上python代码：

```python
class Solution(object):
    def nextBeautifulNumber(self, n):
        """
        :type n: int
        :rtype: int
        """

        def generate(base):
            n = len(base)
            res = []
            now = 0
            for index in range(n):
                now = now * 10 + base[index]
            res.append(now)

            while True:
                p = None
                for index in range(n - 2, -1, -1):
                    if base[index] < base[index + 1]:
                        p = index
                        break
                if p is None:
                    break
                
                q = n - 1
                for index in range(p + 1, n):
                    if base[index] <= base[p]:
                        q = index - 1
                        break
                
                base[p], base[q] = base[q], base[p]
                l = p + 1
                r = n - 1
                while l < r:
                    base[l], base[r] = base[r], base[l]
                    l += 1
                    r -= 1
                
                now = 0
                for index in range(n):
                    now = now * 10 + base[index]
                res.append(now)

            
            return res

        num_list = [1, 22, 333, 4444, 55555, 666666, 1224444]
        num_list.extend(generate([1, 2, 2]))
        num_list.extend(generate([1, 3, 3, 3]))
        num_list.extend(generate([1, 4, 4, 4, 4]))
        num_list.extend(generate([1, 5, 5, 5, 5, 5]))
        num_list.extend(generate([1, 2, 2, 3, 3, 3]))
        num_list.extend(generate([2, 2, 3, 3, 3]))
        num_list.extend(generate([2, 2, 4, 4, 4, 4]))
        for num in sorted(num_list):
            if n < num:
                return num
```
