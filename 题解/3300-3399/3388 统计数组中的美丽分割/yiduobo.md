---
title: "3388. 统计数组中的美丽分割"
aliases: ["yiduobo的每日leetcode 3388.统计数组中的美丽分割"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/string-matching", "题单/字符串", "题单/字符串/二-Z-函数-后缀的前缀", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29833190623"
zhihu_id: "29833190623"
zhihu_title: "yiduobo的每日leetcode 3388.统计数组中的美丽分割"
question_id: "3388"
question: "统计数组中的美丽分割"
problem_url: "https://leetcode.cn/problems/count-beautiful-splits-in-an-array/"
difficulty: "Medium"
rating: 2365
created: "2025-03-12T22:52:01+08:00"
updated: "2025-03-12T22:52:01+08:00"
upvotes: 1
comments: 0
---

# 3388. 统计数组中的美丽分割

> **[yiduobo的每日leetcode 3388.统计数组中的美丽分割](https://zhuanlan.zhihu.com/p/29833190623) · 知乎 · 2025-03-12 · 赞同 1**
> 力扣：[3388. 统计数组中的美丽分割](https://leetcode.cn/problems/count-beautiful-splits-in-an-array/) · Medium · 灵茶山艾府：[两种方法：LCP 数组 / Z 数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3388.统计数组中的美丽分割

[3388. 统计数组中的美丽分割 - 力扣（LeetCode）](https://leetcode.cn/problems/count-beautiful-splits-in-an-array/description/)

题目给出一个整数数组nums，nums的长度不超过5000。如果nums的一个分割满足：

1、将nums分割成三段非空子数组nums1、nums2、nums3，这三段子数组可以拼接得到nums

2、nums1是nums2的前缀，或者nums2是nums3的前缀

那么就称这个分割是美丽分割。

问美丽分割的数目是多少。

由于nums的规模不大，那么最直观的想法就是直接枚举两个分割点i和j，那么得到的三个子数组就分别为nums[:i]、nums[i: j]、nums[j:]，接下来需要检测nums[:i]是否为nums[i: j]的前缀以及nums[i: j]是否为nums[j:]的前缀。

对于子串的公共前缀长度问题，则可以通过子串的长度以及后缀间的最长公共前缀长度来进行判断。方便起见，记f[i][j]为nums中的后缀nums[i:]与nums[j:]的最长公共前缀长度，那么就有：

1、若nums[:i]是nums[i: j]的前缀：

nums[:i]的长度必须小于等于nums[i: j]的长度，即i \<\= j - i

nums与nums[i:]的最长公共前缀长度必须大于等于nums[:i]的长度，即f[0][i] >\= i

2、若nums[i: j]是nums[j:]的前缀：

nums[i: j]的长度必须小于等于nums[j:]的长度，即j - i \<\= n - j

nums[i:]与nums[j:]的最长公共前缀长度必须大于等于nums[i: j]的长度，即f[i][j] >\= j - i

对于这种情况，如果最长公共前缀长度达标，那么子数组长度必然也达标，因此可以只检测后面这个条件

综合起来，就是当f[0][i] >\= i且j - i >\= i，或者f[i][j] >\= j - i时，i和j就是一个美丽分割。

剩下的问题就是如何求解f[i][j]。这是一个经典的动态规划问题。从后往前分别遍历i和j，对于当前遍历到的f[i][j]，若nums[i]与nums[j]不同，那么f[i][j]自然就等于0；反之若j + 1 \< n，那么就有f[i][j] \= f[i +1][j + 1] + 1，否则就有f[i][j] \= 1。

最后附上python代码：

```python
class Solution(object):
    def beautifulSplits(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        f = [[0] * n for _ in range(n)]

        for i in range(n - 2, -1, -1):
            for j in range(n - 1, i, -1):
                if nums[i] == nums[j]:
                    if j + 1 < n:
                        f[i][j] = f[i + 1][j + 1] + 1
                    else:
                        f[i][j] = 1
        
        res = 0
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if (f[0][i] >= i and j - i >= i) or f[i][j] >= j - i:
                    res += 1
                    
        return res
```
