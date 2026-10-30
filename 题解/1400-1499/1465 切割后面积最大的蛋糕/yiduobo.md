---
title: "1465. 切割后面积最大的蛋糕"
aliases: ["yiduobo的每日leetcode 1465.切割后面积最大的蛋糕"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/413702548"
zhihu_id: "413702548"
zhihu_title: "yiduobo的每日leetcode 1465.切割后面积最大的蛋糕"
question_id: "1465"
question: "切割后面积最大的蛋糕"
problem_url: "https://leetcode.cn/problems/maximum-area-of-a-piece-of-cake-after-horizontal-and-vertical-cuts/"
difficulty: "Medium"
created: "2021-09-24T23:41:27+08:00"
updated: "2021-09-24T23:41:27+08:00"
upvotes: 0
comments: 0
---

# 1465. 切割后面积最大的蛋糕

> **[yiduobo的每日leetcode 1465.切割后面积最大的蛋糕](https://zhuanlan.zhihu.com/p/413702548) · 知乎 · 2021-09-24 · 赞同 0**
> 力扣：[1465. 切割后面积最大的蛋糕](https://leetcode.cn/problems/maximum-area-of-a-piece-of-cake-after-horizontal-and-vertical-cuts/) · Medium · 灵茶山艾府：[横切和竖切是互相独立的（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1465.切割后面积最大的蛋糕

[力扣](https://leetcode-cn.com/problems/maximum-area-of-a-piece-of-cake-after-horizontal-and-vertical-cuts/)

由于这里的切割只有横切和纵切两种，这也就以为着最后答案必然是一个矩形。为了使得这个矩形面积最大，自然是要求矩形的长和宽都最大。

注意到矩形的长和宽是互相独立的，于是可以将横切位置和纵切位置分别排序，然后一趟扫描，找出两条横切以及两条纵切之间的最大间隔，二者相乘即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxArea(self, h, w, horizontalCuts, verticalCuts):
        """
        :type h: int
        :type w: int
        :type horizontalCuts: List[int]
        :type verticalCuts: List[int]
        :rtype: int
        """

        last = 0
        max_h = 0
        for now in sorted(horizontalCuts):
            max_h = max(max_h, now - last)
            last = now
        
        max_h = max(max_h, h - now)

        last = 0
        max_v = 0
        for now in sorted(verticalCuts):
            max_v = max(max_v, now - last)
            last = now
        
        max_v = max(max_v, w - now)

        return max_h * max_v % (10 ** 9 + 7)
```
