---
title: "2419. 按位与最大的最长子数组"
aliases: ["yiduobo的每日leetcode 2419.按位与最大的最长子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/brainteaser", "题单/位运算", "题单/贪心算法", "题单/位运算/三-与或-AND/OR-的性质", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569864033"
zhihu_id: "569864033"
zhihu_title: "yiduobo的每日leetcode 2419.按位与最大的最长子数组"
question_id: "2419"
question: "按位与最大的最长子数组"
problem_url: "https://leetcode.cn/problems/longest-subarray-with-maximum-bitwise-and/"
difficulty: "Medium"
rating: 1496
created: "2022-10-01T00:53:42+08:00"
updated: "2022-10-01T00:53:42+08:00"
upvotes: 0
comments: 0
---

# 2419. 按位与最大的最长子数组

> **[yiduobo的每日leetcode 2419.按位与最大的最长子数组](https://zhuanlan.zhihu.com/p/569864033) · 知乎 · 2022-10-01 · 赞同 0**
> 力扣：[2419. 按位与最大的最长子数组](https://leetcode.cn/problems/longest-subarray-with-maximum-bitwise-and/) · Medium · 灵茶山艾府：[脑筋急转弯，从两次遍历到一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2419.按位与最大的最长子数组

[力扣](https://leetcode.cn/problems/longest-subarray-with-maximum-bitwise-and/)

两个正数按位与运算的结果必然是小于等于二者中的较大值，因此本题按位与的最大结果必然是数组中的最大值ma，那么题目就变成了求数组中等于ma的连续子数组的最大长度。

于是可以一趟遍历，使用一个变量cnt记录等于ma的子数组的长度，对于当前遍历到的数num：

1、当num \= ma，那么可以将num加入到子数组中，此时应该将cnt加上1

2、当num > ma，说明之前记录的数并不是数组实际的最大值，也就是说之前统计的最大值都是无效的，此时应该更新ma为num，同时更新cnt和答案为1

3、当num \< ma，说明上一个子数组已经完结，此时应该使用cnt来更新答案，然后更新cnt为0

需要注意的是，在遍历完成后还没有使用最后这个子数组的长度来更新答案，因此还需要使用当前的cnt来更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = 0
        res = 0
        cnt = 0
        for num in nums:
            if num == ma:
                cnt += 1
            elif num > ma:
                ma = num
                res = cnt = 1
            else:
                res = max(res, cnt)
                cnt = 0
        
        return max(res, cnt)
```
