---
title: "LCP 42. 玩具套圈"
aliases: ["yiduobo的每日leetcode LCP42.玩具套圈"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/enumeration", "leetcode/binary-search", "leetcode/bao-li", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576073414"
zhihu_id: "576073414"
zhihu_title: "yiduobo的每日leetcode LCP42.玩具套圈"
question_id: "LCP 42"
question: "玩具套圈"
problem_url: "https://leetcode.cn/problems/vFjcfV/"
difficulty: "Hard"
created: "2022-10-22T03:05:01+08:00"
updated: "2022-10-22T03:05:01+08:00"
upvotes: 0
comments: 0
---

# LCP 42. 玩具套圈

> **[yiduobo的每日leetcode LCP42.玩具套圈](https://zhuanlan.zhihu.com/p/576073414) · 知乎 · 2022-10-22 · 赞同 0**
> 力扣：[LCP 42. 玩具套圈](https://leetcode.cn/problems/vFjcfV/) · Hard · 灵茶山艾府：[排序二分+暴力枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP42.玩具套圈

[力扣](https://leetcode.cn/problems/vFjcfV/)

涉及到圆的几何问题通常都不太好处理，不过本题出题人给的数据范围非常仁慈，每个圆的半径都不超过10，同时所有圆的圆心都处在整数点上，那么在这里就可以将所有圈的圆心先加入到哈希表，然后对于每个玩具，枚举所有可以套到这个玩具的整数圆心，若这个圆心出现在了哈希表中，说明这个玩具可以被套走。

具体来说，如果一个圆(x1, y1, r1)可以完全覆盖另一个圆(x2, y2, r2)，那么就需要满足

sqrt((x1 - x2)^2 + (y1 - y2)^2) \<\= r1 - r2

当然，为了避免开根操作，这个式子通常都会写成

(x1 - x2)^2 + (y1 - y2)^2 \<\= (r1 - r2)^2

回到本题，如果一个玩具(xt, yt, rt)会被一个圈(xc, yc, r)给套住，那么就需要满足r >\= rt，且

(xc - xt)^2 + (yc - yt)^2 \<\= (rt - r)^2

在这里需要枚举所有满足条件的(xc, yc)，实际上就相当于枚举所有处于圆(xt, yt, r - rt)中的点(xc, yc)，然后检测(xc, yc)是否出现在由所有圈的圆心组成哈希表中。方便起见，在这里可以将枚举(xc, yc)的范围放大到正方形，即从xt - (r - rt)到xt + (r - rt)枚举xc，从yt - (r - rt)到yt + (r - rt)枚举yc，然后检测(xc, yc)是否既处于圆(xt, yt, r - rt)内，也处于哈希表中。如果是，说明当前玩具可以被套走，此时更新答案然后考虑下一个玩具即可。

最后附上python代码：

```python
class Solution(object):
    def circleGame(self, toys, circles, r):
        """
        :type toys: List[List[int]]
        :type circles: List[List[int]]
        :type r: int
        :rtype: int
        """

        res = 0
        circle_set = set()
        for cx, cy in circles:
            circle_set.add((cx, cy))
        
        for tx, ty, tr in toys:
            if tr > r:
                continue
            
            l = r - tr
            flag = False
            for x in range(tx - l, tx + l + 1):
                if flag:
                    break
                for y in range(ty - l, ty + l + 1):
                    if (x - tx) ** 2 + (y - ty) ** 2 <= l ** 2 and (x, y) in circle_set:
                        flag = True
                        break
            
            if flag:
                res += 1
        
        return res
```
