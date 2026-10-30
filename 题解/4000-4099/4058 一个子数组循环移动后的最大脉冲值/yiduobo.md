---
title: "4058. 一个子数组循环移动后的最大脉冲值"
aliases: ["yiduobo的每日leetcode 4058.一个子数组循环移动后的最大脉冲值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2085174195231658679"
zhihu_id: "2085174195231658679"
zhihu_title: "yiduobo的每日leetcode 4058.一个子数组循环移动后的最大脉冲值"
question_id: "4058"
question: "一个子数组循环移动后的最大脉冲值"
problem_url: "https://leetcode.cn/problems/maximum-pulse-value-after-one-subarray-rotation/"
difficulty: "Medium"
rating: 1899
created: "2026-09-21T01:31:46+08:00"
updated: "2026-09-21T01:31:46+08:00"
upvotes: 3
comments: 0
---

# 4058. 一个子数组循环移动后的最大脉冲值

> **[yiduobo的每日leetcode 4058.一个子数组循环移动后的最大脉冲值](https://zhuanlan.zhihu.com/p/2085174195231658679) · 知乎 · 2026-09-21 · 赞同 3**
> 力扣：[4058. 一个子数组循环移动后的最大脉冲值](https://leetcode.cn/problems/maximum-pulse-value-after-one-subarray-rotation/) · Medium · 灵茶山艾府：[转化成最大子数组和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4058.一个子数组循环移动后的最大脉冲值

<https://leetcode.cn/problems/maximum-pulse-value-after-one-subarray-rotation/description/>

题目给出一个长度为n的整数数组nums。

定义整数数组的脉冲值为从下标0开始的交替和，即nums[0] - nums[1] + nums[2] - nums[3] + ...

现在可以对nums执行至多一个操作：选择一个子数组，将这个子数组中所有的元素都循环左移一位，例如子数组[a, b, c, d]将变为[b, c, d, a]。

问执行至多一次操作后，可以得到的最大脉冲值。

题目中关于脉冲值的计算是偶加奇减的，因此对于操作的子数组，其起点和终点的奇偶性就有必要分开进行讨论了。具体来说：

1、起点x为偶数，终点y也为偶数：

在原脉冲的计算中，计算方式为

nums[x] - nums[x + 1] + nums[x + 2] - nums[x + 3] + ... - nums[y - 1] + nums[y]

在循环左移一位后，将变为

nums[x + 1] - nums[x + 2] + nums[x + 3] - ... + nums[y - 1] - nums[y] + nums[x]

对比上下两式可以发现，nums[x]抵消之后，实际上就是将

-nums[x + 1] + nums[x + 2] - nums[x + 3] + ... + nums[y]

这一段取反了

2、起点x为偶数，终点y为奇数：

在原脉冲的计算中，计算方式为

nums[x] - nums[x + 1] + nums[x + 2] - nums[x + 3] + ... + nums[y - 1] - nums[y]

在循环左移一位后，将变为

nums[x + 1] - nums[x + 2] + nums[x + 3] - ... - nums[y - 1] + nums[y] - nums[x]

可以发现，这种情况下是将

nums[x] - nums[x + 1] + nums[x + 2] - nums[x + 3] + ... + nums[y - 1] - nums[y]

这一段整段取反

3、起点x为奇数，终点y为偶数：

在原脉冲的计算中，计算方式为

-nums[x] + nums[x + 1] - nums[x + 2] + nums[x + 3] - ... - nums[y - 1] + nums[y]

在循环左移一位后，将变为

-nums[x + 1] + nums[x + 2] - nums[x + 3] + ... + nums[y - 1] - nums[y] + nums[x]

可以发现，这种情况下是将

-nums[x] + nums[x + 1] - nums[x + 2] + nums[x + 3] - ... - nums[y - 1] + nums[y]

这一段整段取反

4、起点x为奇数，终点y也为奇数：

在原脉冲的计算中，计算方式为

-nums[x] + nums[x + 1] - nums[x + 2] + nums[x + 3] - ... + nums[y - 1] - nums[y]

在循环左移一位后，将变为

-nums[x + 1] + nums[x + 2] - nums[x + 3] + ... - nums[y - 1] + nums[y] - nums[x]

对比上下两式可以发现，-nums[x]抵消之后，实际上就是将

nums[x + 1] - nums[x + 2] + nums[x + 3] - ... - nums[y]

这一段取反了

综合以上情况可以发现，如果执行操作，那么操作的结果一定会落在以下两种情况之一：

要么是将起点为偶数，终点为奇数的一整段取反，要么是将起点为奇数，终点为偶数的一整段取反。另一方面，题目要求使得最终的脉冲值最大，那么在这里就应该找出一段负得最多的子数组将其取反，这样才能使得最终结果最大。也就是说明，题目到了这里就是要出一段偶数长度的子数组，这个子数组在原脉冲计算中的结果最小。

基于偶数以及脉冲计算可以视为相邻元素互相减去这一特点，在这里就可以构造两个数组f和g，其中f中储存的是所有偶数下标index对应的nums[index] - nums[index + 1]，而g中存储的则是所有奇数下标对应的- nums[index] + nums[index + 1]。这样一来，找出起点为偶数的，长度为偶数的最优子数组就相当于找出f中的最小子段和，而找出起点为奇数，长度为偶数的最优子数组则相当于找出g中的最小子段和。

对于最小子段和问题，则只需一趟遍历，使用贪心求解就行了。

得到f和g中的最小子段和后，设其中较小的那个为mi，那么最终答案就是原始nums的脉冲值减去两倍的mi。

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ori = 0
        f = []
        g = []
        for index, v in enumerate(nums):
            if index % 2 == 0:
                ori += v
                if index + 1 < len(nums):
                    f.append(v - nums[index + 1])
            else:
                ori -= v
                if index + 1 < len(nums):
                    g.append(nums[index + 1] - v)
        
        def calc(arr):
            mi = 0
            s = 0
            for v in arr:
                s += v
                if s > 0:
                    s = 0
                else:
                    mi = min(mi, s)
            
            return mi

        return ori - min(calc(f), calc(g)) * 2
```
