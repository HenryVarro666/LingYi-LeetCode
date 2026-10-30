---
title: "1671. 得到山形数组的最少删除次数"
aliases: ["yiduobo的每日leetcode 1671.得到山形数组的最少删除次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/443876582"
zhihu_id: "443876582"
zhihu_title: "yiduobo的每日leetcode 1671.得到山形数组的最少删除次数"
question_id: "1671"
question: "得到山形数组的最少删除次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-removals-to-make-mountain-array/"
difficulty: "Hard"
rating: 1913
created: "2021-12-11T00:15:53+08:00"
updated: "2021-12-11T00:15:53+08:00"
upvotes: 0
comments: 0
---

# 1671. 得到山形数组的最少删除次数

> **[yiduobo的每日leetcode 1671.得到山形数组的最少删除次数](https://zhuanlan.zhihu.com/p/443876582) · 知乎 · 2021-12-11 · 赞同 0**
> 力扣：[1671. 得到山形数组的最少删除次数](https://leetcode.cn/problems/minimum-number-of-removals-to-make-mountain-array/) · Hard · 灵茶山艾府：[前后缀分解+最长递增子序列，附题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1671.得到山形数组的最少删除次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-removals-to-make-mountain-array/)

对于山形数组这种类型的问题，通常的做法就是枚举这个山的山顶，然后分别考察两侧应该如何处理。本题也适用这种做法，枚举山顶后要求左侧单调递增，右侧单调递减。为了使得删除的数尽量的少，那么就应该让左侧和右侧这两个单调的数组尽可能的长。

到了这里可以发现，这里左侧数据实际上就是固定了结尾位置的最长上升子序列，而右侧的数组则是反过来看的最长上升子序列。于是可以先使用贪心法求出以每个位置结尾的最长上升子序列的长度，然后一趟扫描枚举山顶，根据左右两侧以山顶为结尾的最长上升子序列的长度来更新答案即可。

需要注意的是，这里题目要求的是山峰，因此左右两侧的最长上升子序列的长度必须都要大于1，这样才能算是有效的山峰。

最后附上python代码：

```python
class Solution(object):
    def minimumMountainRemovals(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = [1]
        f_pos = [nums[0]]

        for num in nums[1:]:
            if num > f_pos[-1]:
                f_pos.append(num)
                f.append(len(f_pos))
            else:
                l = 0
                r = len(f_pos) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if f_pos[mid] < num:
                        l = mid + 1
                    else:
                        r = mid
                    
                f.append(l + 1)
                f_pos[l] = num
        
        n = len(nums)
        g = [1]
        g_pos = [nums[-1]]
        for num in nums[-2::-1]:
            if num > g_pos[-1]:
                g_pos.append(num)
                g.append(len(g_pos))
            else:
                l = 0
                r = len(g_pos) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if g_pos[mid] < num:
                        l = mid + 1
                    else:
                        r = mid
                
                g.append(l + 1)
                g_pos[l] = num
        
        g.reverse()

        res = n
        for index in range(n):
            if f[index] > 1 and g[index] > 1:
                res = min(res, n - (f[index] + g[index] - 1))
        
        return res
```
