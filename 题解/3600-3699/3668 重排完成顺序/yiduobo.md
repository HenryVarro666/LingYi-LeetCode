---
title: "3668. 重排完成顺序"
aliases: ["yiduobo的每日leetcode 3668.重排完成顺序"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950328549828458464"
zhihu_id: "1950328549828458464"
zhihu_title: "yiduobo的每日leetcode 3668.重排完成顺序"
question_id: "3668"
question: "重排完成顺序"
problem_url: "https://leetcode.cn/problems/restore-finishing-order/"
difficulty: "Easy"
created: "2025-09-18T22:41:23+08:00"
updated: "2025-09-18T22:41:24+08:00"
upvotes: 0
comments: 0
---

# 3668. 重排完成顺序

> **[yiduobo的每日leetcode 3668.重排完成顺序](https://zhuanlan.zhihu.com/p/1950328549828458464) · 知乎 · 2025-09-18 · 赞同 0**
> 力扣：[3668. 重排完成顺序](https://leetcode.cn/problems/restore-finishing-order/) · Easy · 灵茶山艾府：[线性做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3668.重排完成顺序

<https://leetcode.cn/problems/restore-finishing-order/>

题目给出一个长度为n的整数数组order以及一个整数数组friends。

order为1到n的一个排列，表示比赛中参赛者按照完成顺序的id。friends则表示朋友们的id，按照严格递增的顺序排列。题目保证friends中的每个id都出现在order数组中。

要求返回一个数组，包含朋友们的id，按照他们的完成顺序排列。

题目实际上就是要将friends数组按照其在order中的位置进行排序，因此在这里需要先建立起order中每个id到顺序的映射，然后根据这个映射对friends进行排序。

另一种处理方法则是反过来，直接遍历order数组，若当前遍历到的id出现在friends中，则将这个id加入到答案数组中。

最后附上python代码：

```python
class Solution(object):
    def recoverOrder(self, order, friends):
        """
        :type order: List[int]
        :type friends: List[int]
        :rtype: List[int]
        """
        
        friends_set = set(friends)
        res = []
        for v in order:
            if v in friends_set:
                res.append(v)
        return res
```
