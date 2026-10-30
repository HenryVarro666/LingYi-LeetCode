---
title: "406. 根据身高重建队列"
aliases: ["yiduobo的每日leetcode 406.根据身高重建队列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/184994392"
zhihu_id: "184994392"
zhihu_title: "yiduobo的每日leetcode 406.根据身高重建队列"
question_id: "406"
question: "根据身高重建队列"
problem_url: "https://leetcode.cn/problems/queue-reconstruction-by-height/"
created: "2020-08-15T21:06:17+08:00"
updated: "2020-08-15T21:06:17+08:00"
upvotes: 0
comments: 0
---

# 406. 根据身高重建队列

> **[yiduobo的每日leetcode 406.根据身高重建队列](https://zhuanlan.zhihu.com/p/184994392) · 知乎 · 2020-08-15 · 赞同 0**
> 力扣：[406. 根据身高重建队列](https://leetcode.cn/problems/queue-reconstruction-by-height/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

406.根据身高重建队列<https://leetcode-cn.com/problems/queue-reconstruction-by-height/>

贪心法的题目。对于每个人来说，身高比这个人矮的人是不会影响到这个人的排位的，因此可以先按h降序，按k升序进行排序。排好序之后按身高逐个插入。

这里的插入涉及到动态区间第k大值的求解，可以使用平衡树来进行优化，不过这里人数的规模较小，直接使用n^2的做法也可以。

最后附上python代码：

```python
class Solution(object):
    def reconstructQueue(self, people):
        """
        :type people: List[List[int]]
        :rtype: List[List[int]]
        """

        sorted_people = sorted(people, key=lambda d:(-d[0], d[1]))
        res = []
        for height, pos in sorted_people:
            if pos == 0:
                res = [[height, pos]] + res
            elif pos == len(res):
                res.append([height, pos])
            else:
                res = res[:pos] + [[height, pos]] + res[pos:]

        return res
```
