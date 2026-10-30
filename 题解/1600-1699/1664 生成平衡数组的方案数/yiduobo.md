---
title: "1664. 生成平衡数组的方案数"
aliases: ["yiduobo的每日leetcode 1664.生成平衡数组的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/442496544"
zhihu_id: "442496544"
zhihu_title: "yiduobo的每日leetcode 1664.生成平衡数组的方案数"
question_id: "1664"
question: "生成平衡数组的方案数"
problem_url: "https://leetcode.cn/problems/ways-to-make-a-fair-array/"
created: "2021-12-08T00:09:08+08:00"
updated: "2021-12-08T00:09:08+08:00"
upvotes: 0
comments: 0
---

# 1664. 生成平衡数组的方案数

> **[yiduobo的每日leetcode 1664.生成平衡数组的方案数](https://zhuanlan.zhihu.com/p/442496544) · 知乎 · 2021-12-08 · 赞同 0**
> 力扣：[1664. 生成平衡数组的方案数](https://leetcode.cn/problems/ways-to-make-a-fair-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1664.生成平衡数组的方案数

[力扣](https://leetcode-cn.com/problems/ways-to-make-a-fair-array/)

不妨设删除了位置p的元素，那么最终两部分的值就是

1、0到p - 1之间所有奇数下标的值，加上p + 1到n - 1之间所有偶数下标的值

2、0到p - 1之间所有偶数下标的值，加上p + 1到n - 1之间所有奇数下标的值

这是分奇偶下标的区间和问题，那么自然可以通过分奇偶下标计算前缀和来求解。

设odd[index]表示0到index之间所有奇数下标的和，even[index]表示0到index之间所有偶数下标的和，那么上面两种情况分别为

1、odd[p - 1] + even[n - 1] - even[p]

2、even[p - 1] + odd[n - 1] - odd[p]

在有了odd和even的前提下，就可以一趟遍历p的位置，然后逐位判断上面两个式子是否相等了。

另外，注意到这里的区间和实际上只用了全体区间的值，以及两组临近的前缀和，那么完全可以省略掉前缀和数组，通过全体奇数下标和偶数下标的和来替代odd[n - 1]以及even[n - 1]，同时在遍历枚举p的过程中顺便计算前缀和，同时利用当前p的奇偶性判断even[p]和odd[p]是否需要在even[p - 1]和odd[p - 1]的基础上加上nums[p]，从而将空降复杂度从O(n)降到O(1)。

除此之外还有一点是可以利用全体数的和减去奇数下标的和来得到偶数下标的和，不过这个并不能给时空复杂度带来本质的区别，所以我在这里就没有实现了。

最后附上python代码：

```python
class Solution(object):
    def waysToMakeFair(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s_odd = s_even = 0
        for index in range(len(nums)):
            if index & 1:
                s_odd += nums[index]
            else:
                s_even += nums[index]
        
        now_odd = now_even = 0
        res = 0
        for index in range(len(nums)):
            if index == 0:
                suffix_even = s_odd
                suffix_odd = s_even - nums[0]
            else:
                suffix_even = s_odd - now_odd
                suffix_odd = s_even - now_even
                if index & 1:
                    suffix_even -= nums[index]
                else:
                    suffix_odd -= nums[index]
            
            if suffix_odd + now_odd == suffix_even + now_even:
                res += 1

            if index & 1:
                now_odd += nums[index]
            else:
                now_even += nums[index]
        
        return res
```
