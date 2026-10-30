---
title: "1431. 拥有最多糖果的孩子"
aliases: ["yiduobo的每日leetcode 1431.拥有最多糖果的孩子"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/408809135"
zhihu_id: "408809135"
zhihu_title: "yiduobo的每日leetcode 1431.拥有最多糖果的孩子"
question_id: "1431"
question: "拥有最多糖果的孩子"
problem_url: "https://leetcode.cn/problems/kids-with-the-greatest-number-of-candies/"
difficulty: "Easy"
created: "2021-09-09T23:40:08+08:00"
updated: "2021-09-09T23:40:08+08:00"
upvotes: 0
comments: 0
---

# 1431. 拥有最多糖果的孩子

> **[yiduobo的每日leetcode 1431.拥有最多糖果的孩子](https://zhuanlan.zhihu.com/p/408809135) · 知乎 · 2021-09-09 · 赞同 0**
> 力扣：[1431. 拥有最多糖果的孩子](https://leetcode.cn/problems/kids-with-the-greatest-number-of-candies/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1431.拥有最多糖果的孩子

[力扣](https://leetcode-cn.com/problems/kids-with-the-greatest-number-of-candies/)

比较基础的题目。首先一趟遍历找出初始状态下糖果数最多的孩子拥有的糖果数，记为now_max。接下来再一趟遍历，考察当前孩子加上额外糖果之后拥有的糖果数目与now_max的大小即可。

最后附上python代码：

```python
class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        """
        :type candies: List[int]
        :type extraCandies: int
        :rtype: List[bool]
        """

        now_max = max(candies)
        return [candy + extraCandies >= now_max for candy in candies]
```
