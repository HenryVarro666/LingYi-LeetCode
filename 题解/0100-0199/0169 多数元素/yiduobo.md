---
title: "169. 多数元素"
aliases: ["yiduobo的每日leetcode 169.多数元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/bian-li", "题单/数学算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/数学算法/七-杂项", "题单/LeetCode-热题-100/技巧", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144788323"
zhihu_id: "144788323"
zhihu_title: "yiduobo的每日leetcode 169.多数元素"
question_id: "169"
question: "多数元素"
problem_url: "https://leetcode.cn/problems/majority-element/"
difficulty: "Easy"
created: "2020-05-30T23:08:06+08:00"
updated: "2020-05-30T23:08:06+08:00"
upvotes: 2
comments: 0
---

# 169. 多数元素

> **[yiduobo的每日leetcode 169.多数元素](https://zhuanlan.zhihu.com/p/144788323) · 知乎 · 2020-05-30 · 赞同 2**
> 力扣：[169. 多数元素](https://leetcode.cn/problems/majority-element/) · Easy · 灵茶山艾府：[O(n) 武林大会打擂台，严谨证明（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

169.多数元素<https://leetcode-cn.com/problems/majority-element/>

很有意思的题目，可以排序后统计，也可以直接用dict来统计，不过这个问题最优的解法是线性的时间复杂度以及常数的空间复杂度。

题目保证了多数元素出现次数大于n/2，意味着我们随机从里面拿一个数，拿到多数元素的概率超过1/2。于是我们可以每次随机从里面取一个数，然后扫描一次统计这个数出现的次数。如果这个数就是多数元素，那么就找到了答案，否则随机另取一个数重复这个过程即可。通过计算概率可以得到这个做法重复次数的期望值为2次，性能还是有保证的。

另一种做法可以认为是某种投票法，即维护一个当前候选者与票数，然后往后扫描数组。若下一个数与当前候选者相同，则票数加一，否则票数减一。当票数为0时，取下一个数作为新的候选者。不知道如何严格给出证明，但是可以发现极端情况下，多数元素与其他数字各自抵消了票数，那么由于多数元素出现的次数大于n/2，那么最终的候选者一定会是多数元素。

最后附上第二种做法的python代码：

```python
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = None
        cnt = 0

        for num in nums:
            if cnt == 0:
                res = num
                cnt = 1
            elif res == num:
                cnt += 1
            else:
                cnt -= 1
                
        return res
```
