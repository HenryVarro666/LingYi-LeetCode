---
title: "3870. 统计范围内的逗号 & 3871. 统计范围内的逗号II"
aliases: ["yiduobo的每日leetcode 3870.统计范围内的逗号 && 3871.统计范围内的逗号II", "3870. 统计范围内的逗号", "3871. 统计范围内的逗号II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/medium", "题单/动态规划", "题单/贪心算法", "题单/动态规划/十-数位-DP", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2018768951874699802"
zhihu_id: "2018768951874699802"
zhihu_title: "yiduobo的每日leetcode 3870.统计范围内的逗号 && 3871.统计范围内的逗号II"
question_id: ["3870", "3871"]
question: ["统计范围内的逗号", "统计范围内的逗号 II"]
problem_url: ["https://leetcode.cn/problems/count-commas-in-range/", "https://leetcode.cn/problems/count-commas-in-range-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1381
created: "2026-03-21T19:44:30+08:00"
updated: "2026-03-21T19:44:30+08:00"
upvotes: 1
comments: 0
---

# 3870. 统计范围内的逗号 & 3871. 统计范围内的逗号II

> **[yiduobo的每日leetcode 3870.统计范围内的逗号 && 3871.统计范围内的逗号II](https://zhuanlan.zhihu.com/p/2018768951874699802) · 知乎 · 2026-03-21 · 赞同 1**
> 力扣：[3870. 统计范围内的逗号](https://leetcode.cn/problems/count-commas-in-range/) · Easy · 灵茶山艾府：[O(log n) 非暴力做法（Python/Java/C++/Go）](../3870%20统计范围内的逗号/灵茶山艾府.md)
> 力扣：[3871. 统计范围内的逗号 II](https://leetcode.cn/problems/count-commas-in-range-ii/) · Medium · 灵茶山艾府：[横看成岭侧成峰，贡献法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3870.统计范围内的逗号

<https://leetcode.cn/problems/count-commas-in-range/description/>

3871.统计范围内的逗号II

<https://leetcode.cn/problems/count-commas-in-range-ii/description/>

题目给出一个整数n，要求返回1到n之间所有整数以标准数字格式书写时所用到的逗号总数。

在标准格式中：

- 从右边开始，每三位数字后插入一个逗号
- 位数不足四位的数字不包含逗号

两题的题设相同，第二题的数据规模较大，n可达10^15。

由于n的数据规模较大，直接计算显然是不行的，必须找规律。

注意到逗号的数量与n的位数有关，因此在这里可以按10的幂次来计算逗号的数量。具体来说：

- 所有的一位数、两位数、三位数都没有逗号，一位数共9 \* 1 \= 9个，两位数共9 \* 10 \= 90个，三位数共9 \* 100共900个
- 所有的四位数、五位数、六位数都仅有一个逗号，四位数共9 \* 1000 \= 9000个，五位数共9 \* 10000 \= 90000个，六位数共9 \* 100000 \= 900000个
- 以此类推

更一般的情况，对于一个length位数，其具有(length - 1) // 3个逗号，同时一共有从10^(length - 1)到10^length - 1，这一共有9 \* 10^(length - 1)个length位数。

基于这一点，就可以使用一个变量p10从1开始每次乘以10，用来表示10的幂次；同时使用另一个变量length从1开始每次加上1，同来表示当前的数位。

每一轮计算，先将(length - 1) // 3 \* p10 \* 9累加到答案中，最后将p10乘以10，将length加上1，直到p10 \* 10 > n为止。

计算完成后，还需要计算从当前的p10到n这些元素中逗号的数量。一共有(n - p10 + 1)个元素，每个元素中的逗号数量为(length - 1) // 3个，于是将(length - 1) // 3 \* (n - p10 + 1)累积到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def countCommas(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        length = 1
        p10 = 1
        res = 0
        while p10 * 10 - 1 < n:
            res += (length - 1) // 3 * p10 * 9
            p10 *= 10
            length += 1
        
        return res + (length - 1) // 3 * (n - p10 + 1)
```
