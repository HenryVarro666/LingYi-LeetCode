---
title: "1959. K次调整数组大小浪费的最小空间"
aliases: ["yiduobo的每日leetcode 1959.K次调整数组大小浪费的最小空间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/493112501"
zhihu_id: "493112501"
zhihu_title: "yiduobo的每日leetcode 1959.K次调整数组大小浪费的最小空间"
question_id: "1959"
question: "K次调整数组大小浪费的最小空间"
problem_url: "https://leetcode.cn/problems/minimum-total-space-wasted-with-k-resizing-operations/"
created: "2022-04-04T22:20:04+08:00"
updated: "2022-04-04T22:20:04+08:00"
upvotes: 0
comments: 0
---

# 1959. K次调整数组大小浪费的最小空间

> **[yiduobo的每日leetcode 1959.K次调整数组大小浪费的最小空间](https://zhuanlan.zhihu.com/p/493112501) · 知乎 · 2022-04-04 · 赞同 0**
> 力扣：[1959. K次调整数组大小浪费的最小空间](https://leetcode.cn/problems/minimum-total-space-wasted-with-k-resizing-operations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1959.K次调整数组大小浪费的最小空间

[力扣](https://leetcode-cn.com/problems/minimum-total-space-wasted-with-k-resizing-operations/)

经典的动态规划问题，令f[i][j]表示将数组中第0到第j个数字拆分成i个部分，最少将浪费多少空间。对于f[i][j]：

1、首先考虑边界情况。当i \= 0时，不会进行数组拆分，因此有

f[i][j] \= max(nums[0], nums[1], nums[j]) \* (j + 1) - (nums[0] + nums[1] + ... + nums[j])

这个式子由前缀最大值和前缀和组成，因此可以从头开始向后一趟遍历，一边求解前缀一边求解f。当然，前缀的max是无法推导出区间的max，因此没有必要保存下来。而前缀和可以推导出区间和，因此后半部分的前缀和有必要保存下来。

2、接下来考虑i > 0的情况。很自然的想法就是枚举最后一段数组的分割位置，那么就有

f[i][j] \= min(f[i][j], f[i - 1][cut_pos] + max(nums[cut_pos + 1], nums[cut_pos + 2], ..., nums[j] \* (j - cut_pos) - (nums[cut_pos + 1] + nums[cut_pos + 2] + ... + nums[j])

其中cut_pos的取值范围在i到j之间。

对于上面的式子，后半部分的区间和可以通过一开始得到的前缀和来计算得到，但区间最大值并不是很好求。注意到这里的区间最大值实际上是从j开始向前的后缀最大值，因此可以调换一下求解的顺序，从j开始从后向前枚举cut_pos，这样一来就可以边求解f边更新max值，最终可以在O(n)的时间复杂度内完成状态的转移。

最终的时间复杂度为O(k \* n^2)。

另外，注意到这里的f每一轮只与上一轮有关，因此可以省去i这一维。

对于这类区间最值转移的问题，可能存在单调性或者数据结构优化的可能性，不过由于上面算法的时间复杂度已经过关，我在这里就没有继续往下思考了。

最后附上python代码：

```python
class Solution(object):
    def minSpaceWastedKResizing(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        f = [0]
        s = [nums[0]]
        ma = nums[0]
        n = len(nums)
        for index in range(1, n):
            ma = max(ma, nums[index])
            s.append(s[-1] + nums[index])
            f.append(ma * (index + 1) - s[-1])
        
        res = f[-1]
        
        for i in range(1, k + 1):
            g = f[:]
            f = []
            for j in range(n - 1, -1, -1):
                if j + 1 <= i:
                    f.append(0)
                else:
                    f.append(g[j - 1])
                    ma = nums[j]
                    for cut_pos in range(j - 1, i - 1, -1):
                        ma = max(nums[cut_pos], ma)
                        f[-1] = min(f[-1], g[cut_pos - 1] + ma * (j - cut_pos + 1) - s[j] + s[cut_pos - 1])
        
            f.reverse()
            res = min(res, f[-1])
        
        return res
```
