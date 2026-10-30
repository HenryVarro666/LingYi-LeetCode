---
title: "2523. 范围内最接近的两个质数"
aliases: ["yiduobo的每日leetcode 2523.范围内最接近的两个质数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636189796"
zhihu_id: "636189796"
zhihu_title: "yiduobo的每日leetcode 2523.范围内最接近的两个质数"
question_id: "2523"
question: "范围内最接近的两个质数"
problem_url: "https://leetcode.cn/problems/closest-prime-numbers-in-range/"
difficulty: "Medium"
rating: 1650
created: "2023-06-11T00:05:30+08:00"
updated: "2023-06-11T00:05:30+08:00"
upvotes: 0
comments: 0
---

# 2523. 范围内最接近的两个质数

> **[yiduobo的每日leetcode 2523.范围内最接近的两个质数](https://zhuanlan.zhihu.com/p/636189796) · 知乎 · 2023-06-11 · 赞同 0**
> 力扣：[2523. 范围内最接近的两个质数](https://leetcode.cn/problems/closest-prime-numbers-in-range/) · Medium · 灵茶山艾府：[预处理质数 + 枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2523.范围内最接近的两个质数

[力扣](https://leetcode.cn/problems/closest-prime-numbers-in-range/)

本题的数据规模比较大，直接使用暴力枚举left到right中的每个数并检测是否为质数的话时间复杂度为O(n \* sqrt(n))，直观感觉上可能需要使用筛法找出范围内的所有质数然后再进行遍历，但是实际上使用暴力算法是完全没有问题的。

由于大于2的所有偶数都不是质数，因此最终答案如果不是（2， 3）这一组间距为1的质数，那么就很可能是两个连续的奇数构成的，也就是说最终答案为2。因此对于本题，只需在暴力计算的过程中判断当前答案是否为1或者2，如果是，那么直接返回答案就行了。

最后附上python代码：

```python
class Solution(object):
    def closestPrimes(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: List[int]
        """

        pre = None
        res = [-1, -1]
        if left == 1:
            left += 1

        for x in range(left, right + 1):
            sqrt_x = int(sqrt(x)) + 1
            flag = True
            for y in range(2, sqrt_x):
                if x % y == 0:
                    flag = False
                    break
            
            if flag:
                if pre is not None and (res[0] == -1 or x - pre < res[1] - res[0]):
                    res[0] = pre
                    res[1] = x
                pre = x
        
            if res[1] - res[0] == 1 or res[1] - res[0] == 2:
                break

        return res
```
