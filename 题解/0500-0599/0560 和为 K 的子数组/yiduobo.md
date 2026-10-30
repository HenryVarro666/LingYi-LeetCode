---
title: "560. 和为K的子数组"
aliases: ["yiduobo的每日leetcode 560.和为K的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/常用数据结构/一-前缀和", "题单/LeetCode-热题-100/子串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266049688"
zhihu_id: "266049688"
zhihu_title: "yiduobo的每日leetcode 560.和为K的子数组"
question_id: "560"
question: "和为 K 的子数组"
problem_url: "https://leetcode.cn/problems/subarray-sum-equals-k/"
difficulty: "Medium"
created: "2020-10-15T21:51:06+08:00"
updated: "2020-10-15T21:51:06+08:00"
upvotes: 1
comments: 0
---

# 560. 和为K的子数组

> **[yiduobo的每日leetcode 560.和为K的子数组](https://zhuanlan.zhihu.com/p/266049688) · 知乎 · 2020-10-15 · 赞同 1**
> 力扣：[560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/) · Medium · 灵茶山艾府：[前缀和+哈希表：从两次遍历到一次遍历，附变形题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

昨日有事外出，今天补上。

560.和为K的子数组<https://leetcode-cn.com/problems/subarray-sum-equals-k/>

看到子数组和这类问题，很自然就联想到使用前缀和来进行处理。

求出前缀和数组后，题目就变成了对于前缀和数组prefix_sum，求里面有多少组(i, j)满足prefix_sum[j] - prefix_sum[i - 1] \= k，此时可以通过一趟扫描加哈希的方法很快解决。

需要特别注意的是，若prefix_sum[j]直接就等于k，也是一个可行的解。

最后附上python代码：

```python
class Solution(object):
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        f = [nums[0]]
        for index in range(1, len(nums)):
            f.append(f[-1] + nums[index])

        pre_dict = {}
        res = 0
        for index, pre_sum in enumerate(f):
            res += pre_dict.get(pre_sum - k, 0)
            if pre_sum == k:
                res += 1
            pre_dict[pre_sum] = pre_dict.get(pre_sum, 0) + 1

        return res
```
