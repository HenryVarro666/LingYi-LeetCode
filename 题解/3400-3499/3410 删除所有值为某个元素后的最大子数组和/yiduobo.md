---
title: "3410. 删除所有值为某个元素后的最大子数组和"
aliases: ["yiduobo的每日leetcode 3410.删除所有值为某个元素后的最大子数组和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31926122186"
zhihu_id: "31926122186"
zhihu_title: "yiduobo的每日leetcode 3410.删除所有值为某个元素后的最大子数组和"
question_id: "3410"
question: "删除所有值为某个元素后的最大子数组和"
problem_url: "https://leetcode.cn/problems/maximize-subarray-sum-after-removing-all-occurrences-of-one-element/"
difficulty: "Hard"
rating: 2844
created: "2025-03-22T00:03:03+08:00"
updated: "2025-03-22T00:03:03+08:00"
upvotes: 1
comments: 0
---

# 3410. 删除所有值为某个元素后的最大子数组和

> **[yiduobo的每日leetcode 3410.删除所有值为某个元素后的最大子数组和](https://zhuanlan.zhihu.com/p/31926122186) · 知乎 · 2025-03-22 · 赞同 1**
> 力扣：[3410. 删除所有值为某个元素后的最大子数组和](https://leetcode.cn/problems/maximize-subarray-sum-after-removing-all-occurrences-of-one-element/) · Hard · 灵茶山艾府：[三种方法：线段树/前后缀分解/前缀和一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3410.删除所有值为某个元素后的最大子数组和

[3410. 删除所有值为某个元素后的最大子数组和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-subarray-sum-after-removing-all-occurrences-of-one-element/)

题目给出一个整数数组nums，可以对nums执行以下操作至多一次：

选择nums中存在的任意整数x，如果nums中不全为x，则将nums中所有值为x的元素删去。

问可能得到的最大子数组和是多少。

不执行操作的情况是很好计算的，只需一趟遍历，使用贪心法计算以每个位置结尾的最大子段和就行了。

对于删除元素的情况，则可以枚举删除的元素然后计算。不过在这里不能先修改nums然后再计算，这样的话时间复杂度太高，可以考虑改成动态规划来进行求解。如果要使用动态规划，枚举的方式就需要稍微改动一下，从枚举删除的元素值，改成删除当前遍历到元素可以得到的最大子段和。更具体的，令f[index]表示以nums[index]结尾，且不执行删除操作的最大子段和，而g[index]则表示以nums[index]结尾，同时删去了所有nums[index]的最大子段和。那么对于f[index]，使用经典的贪心法求解就行了，而对于g[index]：

1、若nums[index] >\= 0：

此时不符合g的定义，可以直接置g[index]为0

2、若nums[index] \< 0，且nums[index]在之前从没出现过：

此时显然有g[index] \= f[index - 1]

3、若nums[index] \< 0，且nums[index]上一次出现的下标为pre：

此时又可以分两种情况，第一种是最大子段的起点在pre之前，那么对于g[index]，在pre之前的部分的子段和就是g[pre]，而pre之后的元素需要全部选择，也就是nums[pre + 1] + nums[pre + 2] + ... + nums[index - 1]

第二种情况则是最大子段的起点在pre之后，这种情况不太好直接计算，但是在这里可以反过来利用f的定义。具体来说，若f[index - 1]对应的子段的起点在pre之后，那么f[index - 1]就是这种情况需要计算的子段和，反之若f[index - 1]对应的子段的起点在pre之前，那么其中必然包含nums[pre] \< 0，对于这种情况，选择第一种情况显然是比f[index - 1]更优的。

综合起来，就有

g[index] \= max(g[pre] + nums[pre + 1] + nums[pre + 2] + ... + nums[index - 1], f[index - 1])

其中nums[pre + 1]到nums[index - 1]的和是区间和，可以使用前缀和之差来进行优化，而下标pre则可以通过哈希表来得到，这样一来状态转移的时间复杂度就是O(1)了。

需要特别注意的是，上面的做法得到的g是不完整的，因为对于g[index]，在删去nums[index]后，其后面还可以加入更多的元素形成更大的子段和，但是由于限定了删去的是nums[index]，也无法判断后续元素是否应该添加。一种可行的思路是反过来再计算一次f和g，即对于f_left和g_left，是从左到右遍历，计算的是以nums[index]结尾的子段和的最大值，而对于f_right和g_right，则是从右到左遍历，计算的是以nums[index]开头的子段和的最大值，那么对于nums[index]，使用g_left[index] + g_right[index]就可以得到完整的最大子段和了。

于是可以正反两趟遍历，分别计算f_left、g_left以及f_right、g_right，对于不删除的情况，最大子段和就是max(f_left)，而对于删除的情况，则可以对nums进行一趟遍历，若当前的nums[index] \< 0，则可以使用g_left[index] + g_right[index]来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxSubarraySum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        if max(nums) <= 0 and len(set(nums)) == 1:
            return nums[0]

        def calc(nums):
            f = [nums[0]]
            g = [0]
            s = [nums[0]]
            pre = {nums[0] : 0}

            now = nums[0]
            for index, v in enumerate(nums[1:], 1):
                s.append(s[-1] + v)

                if now < 0:
                    now = 0
                now += v
                f.append(now)

                if v < 0:
                    if v not in pre:
                        g.append(f[-2])
                    else:
                        pre_index = pre[v]
                        g.append(max(g[pre_index] + s[-2] - s[pre_index], f[-2]))
                else:
                    g.append(0)
            
                pre[v] = index

            return f, g
        
        f_left, g_left = calc(nums)
        f_right, g_right = calc(nums[::-1])
        f_right.reverse()
        g_right.reverse()

        res = max(f_left)
        for index, v in enumerate(nums):
            if v < 0:
                res = max(res, g_left[index] + g_right[index])
        
        return res
```
