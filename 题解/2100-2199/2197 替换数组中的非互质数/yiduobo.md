---
title: "2197. 替换数组中的非互质数"
aliases: ["yiduobo的每日leetcode 2197.替换数组中的非互质数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/math", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/三-栈", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/538513832"
zhihu_id: "538513832"
zhihu_title: "yiduobo的每日leetcode 2197.替换数组中的非互质数"
question_id: "2197"
question: "替换数组中的非互质数"
problem_url: "https://leetcode.cn/problems/replace-non-coprime-numbers-in-array/"
difficulty: "Hard"
rating: 2057
created: "2022-07-07T00:16:51+08:00"
updated: "2022-07-07T00:19:08+08:00"
upvotes: 0
comments: 0
---

# 2197. 替换数组中的非互质数

> **[yiduobo的每日leetcode 2197.替换数组中的非互质数](https://zhuanlan.zhihu.com/p/538513832) · 知乎 · 2022-07-07 · 赞同 0**
> 力扣：[2197. 替换数组中的非互质数](https://leetcode.cn/problems/replace-non-coprime-numbers-in-array/) · Hard · 灵茶山艾府：[邻项消除问题的通用做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2197.替换数组中的非互质数

[力扣](https://leetcode.cn/problems/replace-non-coprime-numbers-in-array/)

由于题目已经表示了不管哪种替换顺序最后的结果都一样，虽然不知道怎么证明，但是可以利用这一点，每次将当前已知的两个不互质的数合并起来就好了。

一个直观的想法是从左向右一趟遍历，同时使用某种数据结构储存当前已经合并完成的数。对于当前遍历到的数num，若num与之前储存的相邻的数不互质，那么就将这个相邻的数删去，同时将num更新为二者的最小公倍数。重复此过程直到没有数剩下或者num与相邻的数互质为止。接下来将num储存起来，然后继续向后遍历。

可以发现，为了实现上述过程需要能高效得到最近一个储存起来的数，遵从的是后进先出的逻辑，也就是说可以利用栈来实现上述的运算过程。

由于每个数最多只会进出栈一次，因此最终的时间复杂度为O(nlogC)，其中logC为通过计算最大公约数来判断两个数是否互质的复杂度。

最后附上python代码：

```python
class Solution(object):
    def replaceNonCoprimes(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        res = [nums[0]]
        for num in nums[1:]:
            while res:
                last = res.pop()
                x, y = last, num
                while y:
                    x, y = y, x % y

                if x == 1:
                    res.append(last)
                    break
                else:
                    num *= last / x
        
            res.append(num)

        return res
```
