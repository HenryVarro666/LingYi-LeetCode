---
title: "325. 和等于k的最长子数组长度"
aliases: ["yiduobo的每日leetcode 325.和等于k的最长子数组长度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596390106"
zhihu_id: "596390106"
zhihu_title: "yiduobo的每日leetcode 325.和等于k的最长子数组长度"
question_id: "325"
question: "和等于k的最长子数组长度"
problem_url: "https://leetcode.cn/problems/maximum-size-subarray-sum-equals-k/"
created: "2023-01-04T03:13:26+08:00"
updated: "2023-01-04T03:13:26+08:00"
upvotes: 0
comments: 0
---

# 325. 和等于k的最长子数组长度

> **[yiduobo的每日leetcode 325.和等于k的最长子数组长度](https://zhuanlan.zhihu.com/p/596390106) · 知乎 · 2023-01-04 · 赞同 0**
> 力扣：[325. 和等于k的最长子数组长度](https://leetcode.cn/problems/maximum-size-subarray-sum-equals-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

325.和等于k的最长子数组长度

[力扣](https://leetcode.cn/problems/maximum-size-subarray-sum-equals-k/)

对于子数组和，也就是区间和问题，一种常见的处理方法是将其转化为前缀和之差。对于本题，为了找出满足条件的子数组，可以枚举right的位置，同时计算前缀和s[right]。若right左侧存在某个left满足s[left - 1] \= s[right] - k，那么(left, right)就是一个满足条件的子数组。为了高效寻找left，可以使用哈希表储存每种s[left - 1]首次出现的位置。在这里之储存首次出现位置的理由是为了使得答案数组最长，因此left越小越好。

于是现在就得到了一种算法。初始化哈希表first_pos为{0 : -1}，接下来从头开始枚举nums。对于当前枚举到的nums[index]，先将其累加到前缀和now中。若now - k存在与first_pos中，那么说明(first_pos[now - k] + 1, index)就是一个满足条件的子数组，此时应该使用index - first_pos[now - k]来更新答案。另外，若now自身还未出现在哈希表中，那么就将其加入哈希表中，即first_pos[now] \= index。

最后附上python代码：

```python
class Solution(object):
    def maxSubArrayLen(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        first_pos = {}
        first_pos[0] = -1
        now = 0
        res = 0
        for index, num in enumerate(nums):
            now += num
            if now - k in first_pos:
                res = max(res, index - first_pos[now - k])
            
            if now not in first_pos:
                first_pos[now] = index
        
        return res
```
