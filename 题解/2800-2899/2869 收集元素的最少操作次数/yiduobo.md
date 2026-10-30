---
title: "2869. 收集元素的最少操作次数"
aliases: ["yiduobo的每日leetcode 2869.收集元素的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662327567"
zhihu_id: "662327567"
zhihu_title: "yiduobo的每日leetcode 2869.收集元素的最少操作次数"
question_id: "2869"
question: "收集元素的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-collect-elements/"
difficulty: "Easy"
created: "2023-10-20T03:46:14+08:00"
updated: "2023-10-20T03:46:14+08:00"
upvotes: 0
comments: 0
---

# 2869. 收集元素的最少操作次数

> **[yiduobo的每日leetcode 2869.收集元素的最少操作次数](https://zhuanlan.zhihu.com/p/662327567) · 知乎 · 2023-10-20 · 赞同 0**
> 力扣：[2869. 收集元素的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-collect-elements/) · Easy · 灵茶山艾府：[位运算 O(1) 空间做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2869.收集元素的最少操作次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-operations-to-collect-elements/)

直接按照题目描述进行模拟，从后向前不断将数组的末尾元素弹出，并将小于等于k的元素加入到集合中。若某一时刻集合的大小等于k，说明里面恰好包含了1到k，返回此时弹出元素的总次数即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        vis = set()
        res = 0
        while len(vis) < k:
            if nums[-1] <= k:
                vis.add(nums[-1])
            
            nums.pop()
            res += 1
        
        return res
```
