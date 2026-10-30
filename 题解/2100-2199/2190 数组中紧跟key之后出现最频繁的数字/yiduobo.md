---
title: "2190. 数组中紧跟key之后出现最频繁的数字"
aliases: ["yiduobo的每日leetcode 2190.数组中紧跟key之后出现最频繁的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/537143665"
zhihu_id: "537143665"
zhihu_title: "yiduobo的每日leetcode 2190.数组中紧跟key之后出现最频繁的数字"
question_id: "2190"
question: "数组中紧跟key之后出现最频繁的数字"
problem_url: "https://leetcode.cn/problems/most-frequent-number-following-key-in-an-array/"
created: "2022-07-04T01:26:47+08:00"
updated: "2022-07-04T01:26:47+08:00"
upvotes: 0
comments: 0
---

# 2190. 数组中紧跟key之后出现最频繁的数字

> **[yiduobo的每日leetcode 2190.数组中紧跟key之后出现最频繁的数字](https://zhuanlan.zhihu.com/p/537143665) · 知乎 · 2022-07-04 · 赞同 0**
> 力扣：[2190. 数组中紧跟key之后出现最频繁的数字](https://leetcode.cn/problems/most-frequent-number-following-key-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2190.数组中紧跟key之后出现最频繁的数字

[力扣](https://leetcode.cn/problems/most-frequent-number-following-key-in-an-array/)

直接一趟遍历，使用哈希表统计每个key之后的下一个数字的出现次数，然后取其中出现次数最多的作为答案。

最后附上python代码：

```python
class Solution(object):
    def mostFrequent(self, nums, key):
        """
        :type nums: List[int]
        :type key: int
        :rtype: int
        """

        cnt_dict = {}
        for index in range(len(nums) - 1):
            if nums[index] == key:
                target = nums[index + 1]
                cnt_dict[target] = cnt_dict.get(target, 0) + 1
        
        res = None
        max_cnt = 0
        for num, cnt in cnt_dict.items():
            if cnt > max_cnt:
                max_cnt = cnt
                res = num
        
        return res
```
