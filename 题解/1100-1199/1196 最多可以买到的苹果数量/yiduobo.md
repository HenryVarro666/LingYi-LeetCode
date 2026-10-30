---
title: "1196. 最多可以买到的苹果数量"
aliases: ["yiduobo的每日leetcode 1196.最多可以买到的苹果数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/612452736"
zhihu_id: "612452736"
zhihu_title: "yiduobo的每日leetcode 1196.最多可以买到的苹果数量"
question_id: "1196"
question: "最多可以买到的苹果数量"
problem_url: "https://leetcode.cn/problems/how-many-apples-can-you-put-into-the-basket/"
created: "2023-03-08T23:21:17+08:00"
updated: "2023-03-08T23:21:17+08:00"
upvotes: 0
comments: 0
---

# 1196. 最多可以买到的苹果数量

> **[yiduobo的每日leetcode 1196.最多可以买到的苹果数量](https://zhuanlan.zhihu.com/p/612452736) · 知乎 · 2023-03-08 · 赞同 0**
> 力扣：[1196. 最多可以买到的苹果数量](https://leetcode.cn/problems/how-many-apples-can-you-put-into-the-basket/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1196.最多可以买到的苹果数量

[力扣](https://leetcode.cn/problems/how-many-apples-can-you-put-into-the-basket/)

题目只是要求买到的苹果数量最多，并不是要求重量最大，因此在这里就应该优先选择重量较小的苹果，于是只需要对苹果重量从小到大一趟排序，然后一趟遍历，不断选择苹果直到重量超标为止。

最后附上python代码：

```python
class Solution(object):
    def maxNumberOfApples(self, weight):
        """
        :type weight: List[int]
        :rtype: int
        """

        cnt = 0
        res = 0
        for w in sorted(weight):
            if cnt + w > 5000:
                break

            cnt += w
            res += 1
        
        return res
```
