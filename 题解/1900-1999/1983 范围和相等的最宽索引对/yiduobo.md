---
title: "1983. 范围和相等的最宽索引对"
aliases: ["yiduobo的每日leetcode 1983.范围和相等的最宽索引对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624348095"
zhihu_id: "624348095"
zhihu_title: "yiduobo的每日leetcode 1983.范围和相等的最宽索引对"
question_id: "1983"
question: "范围和相等的最宽索引对"
problem_url: "https://leetcode.cn/problems/widest-pair-of-indices-with-equal-range-sum/"
created: "2023-04-24T00:25:10+08:00"
updated: "2023-04-24T00:25:10+08:00"
upvotes: 0
comments: 0
---

# 1983. 范围和相等的最宽索引对

> **[yiduobo的每日leetcode 1983.范围和相等的最宽索引对](https://zhuanlan.zhihu.com/p/624348095) · 知乎 · 2023-04-24 · 赞同 0**
> 力扣：[1983. 范围和相等的最宽索引对](https://leetcode.cn/problems/widest-pair-of-indices-with-equal-range-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1983.范围和相等的最宽索引对

[力扣](https://leetcode.cn/problems/widest-pair-of-indices-with-equal-range-sum/)

题目要求找出最长的区间[left, right]，要求nums1中left到right这一段之和恰好等于nums2中left到right这一段之和。

为了方便处理，在这里可以用nums1中每个数减去nums2中下标相同的数得到新数组d，那么问题就转化成了找出d中最长的区间[left，right]，要求区间中数值之和为0。

对于这个问题，则可以进一步进行转化，也就是d的前缀和d[0] + d[1] + ... + d[left - 1]恰好等于前缀和d[0] + d[1] + ... + d[right]，于是只需一趟遍历计算d数组的前缀和，同时使用哈希表记录每种前缀和第一次出现的下标位置。对于当前的前缀和s，若s已经出现在哈希表中，那么就使用当前坐标与哈希表中记录s首次出现的下标来更新最终答案，否则就将s加入到哈希表中。

最后附上python代码：

```python
class Solution(object):
    def widestPairOfIndices(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        res = 0
        first_pos = {0: 0}
        s = 0
        n = len(nums1)
        for index in range(n):
            s += nums1[index] - nums2[index]
            if s in first_pos:
                res = max(res, index - first_pos[s] + 1)
            else:
                first_pos[s] = index + 1
        
        return res
```
