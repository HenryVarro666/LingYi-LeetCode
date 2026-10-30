---
title: "2682. 找出转圈游戏输家"
aliases: ["yiduobo的每日leetcode 2682.找出转圈游戏输家"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649680384"
zhihu_id: "649680384"
zhihu_title: "yiduobo的每日leetcode 2682.找出转圈游戏输家"
question_id: "2682"
question: "找出转圈游戏输家"
problem_url: "https://leetcode.cn/problems/find-the-losers-of-the-circular-game/"
difficulty: "Easy"
created: "2023-08-13T00:05:58+08:00"
updated: "2023-08-13T00:05:58+08:00"
upvotes: 0
comments: 0
---

# 2682. 找出转圈游戏输家

> **[yiduobo的每日leetcode 2682.找出转圈游戏输家](https://zhuanlan.zhihu.com/p/649680384) · 知乎 · 2023-08-13 · 赞同 0**
> 力扣：[2682. 找出转圈游戏输家](https://leetcode.cn/problems/find-the-losers-of-the-circular-game/) · Easy · 灵茶山艾府：[模拟（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2682.找出转圈游戏输家

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-losers-of-the-circular-game/description/)

约瑟夫问题的某种变种，应该存在数学方法或者动态规划方法进行求解，不过本题的数据规模很小，因此在这里直接使用暴力法求解就行了。

最后附上python代码：

```python
class Solution(object):
    def circularGameLosers(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[int]
        """

        res = []
        vis = [False] * (n + 1)
        now = 1
        vis[1] = True
        step = k
        while True:
            now += step
            if now > n:
                now -= n
            if vis[now]:
                break
            vis[now] = True

            step += k
            if step >= n:
                step -= n
        
        for index in range(1, n + 1):
            if not vis[index]:
                res.append(index)
        
        return res
```
