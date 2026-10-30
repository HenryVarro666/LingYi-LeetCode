---
title: "822. 翻转卡片游戏"
aliases: ["yiduobo的每日leetcode 822.翻转卡片游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344113862"
zhihu_id: "344113862"
zhihu_title: "yiduobo的每日leetcode 822.翻转卡片游戏"
question_id: "822"
question: "翻转卡片游戏"
problem_url: "https://leetcode.cn/problems/card-flipping-game/"
difficulty: "Medium"
created: "2021-01-18T22:27:44+08:00"
updated: "2021-01-18T22:27:44+08:00"
upvotes: 0
comments: 0
---

# 822. 翻转卡片游戏

> **[yiduobo的每日leetcode 822.翻转卡片游戏](https://zhuanlan.zhihu.com/p/344113862) · 知乎 · 2021-01-18 · 赞同 0**
> 力扣：[822. 翻转卡片游戏](https://leetcode.cn/problems/card-flipping-game/) · Medium · 灵茶山艾府：[阅读理解题（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

822.翻转卡片游戏

[力扣](https://leetcode-cn.com/problems/card-flipping-game/)

首先，如果一张卡片的正反两面都是同一个数字的话，那么这个数字必然不能成为答案。而对于除开这类数字之外其他数字，由于其不会同时出现在同一张卡片的两边，因此只需要将该数字翻到卡片的背面就行了。

到了这里，就只需要找到没有同时出现在卡片两面的最小的数字即可。

最后附上python代码：

```python
class Solution(object):
    def flipgame(self, fronts, backs):
        """
        :type fronts: List[int]
        :type backs: List[int]
        :rtype: int
        """

        ban_set = set()
        for index in range(len(fronts)):
            if fronts[index] == backs[index]:
                ban_set.add(fronts[index])
        
        res = 0
        for num in fronts:
            if num not in ban_set and (res == 0 or res > num):
                res = num
        for num in backs:
            if num not in ban_set and (res == 0 or res > num):
                res = num
                
        return res
```
