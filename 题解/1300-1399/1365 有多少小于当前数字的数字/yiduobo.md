---
title: "1365. 有多少小于当前数字的数字"
aliases: ["yiduobo的每日leetcode 1365.有多少小于当前数字的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/399741229"
zhihu_id: "399741229"
zhihu_title: "yiduobo的每日leetcode 1365.有多少小于当前数字的数字"
question_id: "1365"
question: "有多少小于当前数字的数字"
problem_url: "https://leetcode.cn/problems/how-many-numbers-are-smaller-than-the-current-number/"
created: "2021-08-14T14:34:27+08:00"
updated: "2021-08-14T14:34:27+08:00"
upvotes: 0
comments: 0
---

# 1365. 有多少小于当前数字的数字

> **[yiduobo的每日leetcode 1365.有多少小于当前数字的数字](https://zhuanlan.zhihu.com/p/399741229) · 知乎 · 2021-08-14 · 赞同 0**
> 力扣：[1365. 有多少小于当前数字的数字](https://leetcode.cn/problems/how-many-numbers-are-smaller-than-the-current-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1365.有多少小于当前数字的数字

[力扣](https://leetcode-cn.com/problems/how-many-numbers-are-smaller-than-the-current-number/)

比较直观的做法是先从小到大进行排序，然后一趟扫描统计。由于这里数字最多到100，因此我在这里采用的是桶排。

最后附上python代码：

```python
class Solution(object):
    def smallerNumbersThanCurrent(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        cnt_list = [0] * 101
        for num in nums:
            cnt_list[num] += 1
        
        res = [0]
        for num in range(1, 101):
            res.append(res[-1] + cnt_list[num - 1])
        
        return [res[num] for num in nums]
```
