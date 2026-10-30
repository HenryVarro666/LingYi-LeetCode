---
title: "1630. 等差子数组"
aliases: ["yiduobo的每日leetcode 1630.等差子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/437824960"
zhihu_id: "437824960"
zhihu_title: "yiduobo的每日leetcode 1630.等差子数组"
question_id: "1630"
question: "等差子数组"
problem_url: "https://leetcode.cn/problems/arithmetic-subarrays/"
created: "2021-11-25T23:03:06+08:00"
updated: "2021-11-25T23:03:06+08:00"
upvotes: 0
comments: 0
---

# 1630. 等差子数组

> **[yiduobo的每日leetcode 1630.等差子数组](https://zhuanlan.zhihu.com/p/437824960) · 知乎 · 2021-11-25 · 赞同 0**
> 力扣：[1630. 等差子数组](https://leetcode.cn/problems/arithmetic-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1630.等差子数组

[力扣](https://leetcode-cn.com/problems/arithmetic-subarrays/)

题目给出了一个原始数组nums和若干组区间，问每一组区间内的数能否形成等差数列。

对于一个长度固定的等差数列而言，只要知道了这个数列的首项以及公差，那么后面所有的项就都知道了。在这里，首项自然是区间中的最小值，而公差则可以通过找到区间中第二小的值，与最小值作差得到。

于是一个自然的想法就是一趟扫描，找出区间中最小的两个数m1和m2，那么就有公差delta \= m2 - m1。接下来，只需要检测m1 + delta \* 2、m1 + detla \* 3、...、m1 + delta \* (r - l + 1)是否都在区间中即可。对于这个问题，则可以在找m1和m2的过程中使用一个哈希表记录下所有出现过的数，然后通过哈希表来进行判断。

另外，需要注意一种特殊情况就是公差为0，此时只有当区间中所有数都一样时才会是等差数列。

最后附上python代码：

```python
class Solution(object):
    def checkArithmeticSubarrays(self, nums, l, r):
        """
        :type nums: List[int]
        :type l: List[int]
        :type r: List[int]
        :rtype: List[bool]
        """

        m = len(l)
        res = []
        for index in range(m):
            m1 = m2 = None
            num_set = set()
            for num in nums[l[index]: r[index] + 1]:
                if m1 is None or num < m1:
                    m1, m2 = num, m1
                elif m2 is None or num < m2:
                    m2 = num
            
                num_set.add(num)

            delta = m2 - m1
            if delta == 0:
                res.append(len(num_set) == 1)
            else:
                flag = True
                for multi in range(r[index] - l[index] + 1):
                    tmp = m1 + delta* multi
                    if tmp not in num_set:
                        flag = False
                        break
                res.append(flag)
        
        return res
```
