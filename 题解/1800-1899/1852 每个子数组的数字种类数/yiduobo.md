---
title: "1852. 每个子数组的数字种类数"
aliases: ["yiduobo的每日leetcode 1852.每个子数组的数字种类数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622264787"
zhihu_id: "622264787"
zhihu_title: "yiduobo的每日leetcode 1852.每个子数组的数字种类数"
question_id: "1852"
question: "每个子数组的数字种类数"
problem_url: "https://leetcode.cn/problems/distinct-numbers-in-each-subarray/"
created: "2023-04-16T04:09:52+08:00"
updated: "2023-04-16T04:09:52+08:00"
upvotes: 0
comments: 0
---

# 1852. 每个子数组的数字种类数

> **[yiduobo的每日leetcode 1852.每个子数组的数字种类数](https://zhuanlan.zhihu.com/p/622264787) · 知乎 · 2023-04-16 · 赞同 0**
> 力扣：[1852. 每个子数组的数字种类数](https://leetcode.cn/problems/distinct-numbers-in-each-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1852.每个子数组的数字种类数

[力扣](https://leetcode.cn/problems/distinct-numbers-in-each-subarray/)

非常标准的滑动窗口问题。

维护一个长度为k的窗口，从数组左侧开始向右滑动，过程中使用哈希表记录当前窗口中每种数字出现的次数即可。

最后附上python代码：

```python
class Solution(object):
    def distinctNumbers(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        cnt = {}
        for v in nums[:k]:
            cnt[v] = cnt.get(v, 0) + 1
        
        res = [len(cnt)]
        for index, v in enumerate(nums[k:]):
            cnt[v] = cnt.get(v, 0) + 1
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                cnt.pop(nums[index])
            
            res.append(len(cnt))
        
        return res
```
