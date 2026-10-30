---
title: "1748. 唯一元素的和"
aliases: ["yiduobo的每日leetcode 1748.唯一元素的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/454630070"
zhihu_id: "454630070"
zhihu_title: "yiduobo的每日leetcode 1748.唯一元素的和"
question_id: "1748"
question: "唯一元素的和"
problem_url: "https://leetcode.cn/problems/sum-of-unique-elements/"
created: "2022-01-07T23:50:45+08:00"
updated: "2022-01-07T23:50:45+08:00"
upvotes: 0
comments: 0
---

# 1748. 唯一元素的和

> **[yiduobo的每日leetcode 1748.唯一元素的和](https://zhuanlan.zhihu.com/p/454630070) · 知乎 · 2022-01-07 · 赞同 0**
> 力扣：[1748. 唯一元素的和](https://leetcode.cn/problems/sum-of-unique-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1748.唯一元素的和

[力扣](https://leetcode-cn.com/problems/sum-of-unique-elements/)

比较基础的题目。利用dict统计每个元素出现的次数，然后将其中只出现一次的元素相加即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1

        res = 0
        for num, cnt in num_dict.items():
            if cnt == 1:
                res += num
        
        return res
```
