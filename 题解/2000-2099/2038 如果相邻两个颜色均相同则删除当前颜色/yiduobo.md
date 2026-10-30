---
title: "2038. 如果相邻两个颜色均相同则删除当前颜色"
aliases: ["yiduobo的每日leetcode 2038.如果相邻两个颜色均相同则删除当前颜色"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/string", "leetcode/game-theory", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/六-分组循环", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/509205567"
zhihu_id: "509205567"
zhihu_title: "yiduobo的每日leetcode 2038.如果相邻两个颜色均相同则删除当前颜色"
question_id: "2038"
question: "如果相邻两个颜色均相同则删除当前颜色"
problem_url: "https://leetcode.cn/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/"
difficulty: "Medium"
rating: 1468
created: "2022-05-04T18:01:16+08:00"
updated: "2022-05-04T18:01:16+08:00"
upvotes: 1
comments: 0
---

# 2038. 如果相邻两个颜色均相同则删除当前颜色

> **[yiduobo的每日leetcode 2038.如果相邻两个颜色均相同则删除当前颜色](https://zhuanlan.zhihu.com/p/509205567) · 知乎 · 2022-05-04 · 赞同 1**
> 力扣：[2038. 如果相邻两个颜色均相同则删除当前颜色](https://leetcode.cn/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/) · Medium · 灵茶山艾府：[统计连续相同颜色的长度](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2038.如果相邻两个颜色均相同则删除当前颜色

[力扣](https://leetcode-cn.com/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/)

首先可以明确的是，删除某个位置上的颜色对其他任意位置是否可以被删除并不会产生任何影响。

设当前准备删除的位置为p，对于其他位置来说，只有删除位置左右两侧的这两个位置，即p - 1和p + 1会受到当前位置的影响。

接下来如果删去了p，那么p - 1的右侧变成了p + 1，而p + 1的左侧变成了p - 1。又因为p - 1、p、p + 1的颜色一直，因此当前p被删去后，p - 1的右侧和p + 1的左侧颜色并没有发生变化，因此删去p并不会给其他任何位置带来影响。

有了这个结论，alice和bob实际上就是各玩各的，最终比较的是可删除的A的数量与可删除的B的数量。若A的比较多，那么alice胜，否则bob胜。

最后附上python代码：

```python
class Solution(object):
    def winnerOfGame(self, colors):
        """
        :type colors: str
        :rtype: bool
        """

        cnt = 0
        for index in range(1, len(colors) - 1):
            if colors[index - 1] == colors[index] == colors[index + 1]:
                if colors[index] == 'A':
                    cnt += 1
                else:
                    cnt -= 1
        
        return cnt > 0
```
