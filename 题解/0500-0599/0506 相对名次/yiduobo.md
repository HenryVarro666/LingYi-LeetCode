---
title: "506. 相对名次"
aliases: ["yiduobo的每日leetcode 506.相对名次"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/259363054"
zhihu_id: "259363054"
zhihu_title: "yiduobo的每日leetcode 506.相对名次"
question_id: "506"
question: "相对名次"
problem_url: "https://leetcode.cn/problems/relative-ranks/"
created: "2020-09-25T20:25:55+08:00"
updated: "2020-09-25T20:25:55+08:00"
upvotes: 0
comments: 0
---

# 506. 相对名次

> **[yiduobo的每日leetcode 506.相对名次](https://zhuanlan.zhihu.com/p/259363054) · 知乎 · 2020-09-25 · 赞同 0**
> 力扣：[506. 相对名次](https://leetcode.cn/problems/relative-ranks/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

506.相对名次<https://leetcode-cn.com/problems/relative-ranks/>

比较基础的题目，按照分数从大到小排序后输出即可。

最后附上python代码：

```python
class Solution(object):
    def findRelativeRanks(self, nums):
        """
        :type nums: List[int]
        :rtype: List[str]
        """

        score_dict = {}
        for index, score in enumerate(sorted(nums, reverse=True)):
            score_dict[score] = index + 1

        res = []
        for num in nums:
            if score_dict[num] == 1:
                res.append('Gold Medal')
            elif score_dict[num] == 2:
                res.append('Silver Medal')
            elif score_dict[num] == 3:
                res.append('Bronze Medal')
            else:
                res.append(str(score_dict[num]))

        return res
```
