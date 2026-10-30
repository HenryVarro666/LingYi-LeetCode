---
title: "2733. 既不是最小值也不是最大值"
aliases: ["yiduobo的每日leetcode 2733.既不是最小值也不是最大值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652582223"
zhihu_id: "652582223"
zhihu_title: "yiduobo的每日leetcode 2733.既不是最小值也不是最大值"
question_id: "2733"
question: "既不是最小值也不是最大值"
problem_url: "https://leetcode.cn/problems/neither-minimum-nor-maximum/"
difficulty: "Easy"
rating: 1148
created: "2023-08-27T02:42:25+08:00"
updated: "2023-08-27T02:42:25+08:00"
upvotes: 0
comments: 0
---

# 2733. 既不是最小值也不是最大值

> **[yiduobo的每日leetcode 2733.既不是最小值也不是最大值](https://zhuanlan.zhihu.com/p/652582223) · 知乎 · 2023-08-27 · 赞同 0**
> 力扣：[2733. 既不是最小值也不是最大值](https://leetcode.cn/problems/neither-minimum-nor-maximum/) · Easy · 灵茶山艾府：[O(1) 时间做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2733.既不是最小值也不是最大值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/neither-minimum-nor-maximum/)

首先考虑边界情况。若数组的长度不超过2，那么数组中的数要么是最小值要么是最大值，此时直接返回-1即可。

而对于数组长度大于2的情况，由于题目保证了数组中的每个数都互不相同，那么只需选择数组中的次小值就能满足题目要求，于是只需一趟遍历，找出数组中的次小值。

最后附上python代码：

```python
class Solution(object):
    def findNonMinOrMax(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if len(nums) <= 2:
            return -1
        
        mi = nums[0]
        res = nums[1]
        if mi > res:
            res, mi = mi, res
        
        for v in nums[2:]:
            if v < mi:
                mi, res = v, mi
            elif v < res:
                res = v
            
        return res
```
