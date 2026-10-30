---
title: "2739. 总行驶距离"
aliases: ["yiduobo的每日leetcode 2739.总行驶距离"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653175496"
zhihu_id: "653175496"
zhihu_title: "yiduobo的每日leetcode 2739.总行驶距离"
question_id: "2739"
question: "总行驶距离"
problem_url: "https://leetcode.cn/problems/total-distance-traveled/"
difficulty: "Easy"
created: "2023-08-30T02:22:28+08:00"
updated: "2023-08-30T02:22:28+08:00"
upvotes: 0
comments: 0
---

# 2739. 总行驶距离

> **[yiduobo的每日leetcode 2739.总行驶距离](https://zhuanlan.zhihu.com/p/653175496) · 知乎 · 2023-08-30 · 赞同 0**
> 力扣：[2739. 总行驶距离](https://leetcode.cn/problems/total-distance-traveled/) · Easy · 灵茶山艾府：[模拟 / 数学（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2739.总行驶距离

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/total-distance-traveled/)

不断将主油箱的油量除以5来计算可能获得的补给油量t，若当前的t大于0，那么就尝试从副油箱抽调t的油补到主油箱并更新行驶距离，然后重复此过程，直到某一时刻t等于0为止。当t等于0时，则只需将剩余油量可行驶的距离累加到答案中就行了。

最后附上python代码：

```python
class Solution(object):
    def distanceTraveled(self, mainTank, additionalTank):
        """
        :type mainTank: int
        :type additionalTank: int
        :rtype: int
        """

        res = 0
        while mainTank:
            r = mainTank % 5
            t = mainTank / 5
            if t > 0:
                res += t * 50
                t = min(t, additionalTank)
                additionalTank -= t
                mainTank = r + t
            else:
                res += r * 10
                break

        return res
```
