---
title: "2078. 两栋颜色不同且距离最远的房子"
aliases: ["yiduobo的每日leetcode 2078.两栋颜色不同且距离最远的房子"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/brainteaser", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/零-常用枚举技巧", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/517489037"
zhihu_id: "517489037"
zhihu_title: "yiduobo的每日leetcode 2078.两栋颜色不同且距离最远的房子"
question_id: "2078"
question: "两栋颜色不同且距离最远的房子"
problem_url: "https://leetcode.cn/problems/two-furthest-houses-with-different-colors/"
difficulty: "Easy"
created: "2022-05-20T16:35:27+08:00"
updated: "2022-05-20T16:35:27+08:00"
upvotes: 0
comments: 0
---

# 2078. 两栋颜色不同且距离最远的房子

> **[yiduobo的每日leetcode 2078.两栋颜色不同且距离最远的房子](https://zhuanlan.zhihu.com/p/517489037) · 知乎 · 2022-05-20 · 赞同 0**
> 力扣：[2078. 两栋颜色不同且距离最远的房子](https://leetcode.cn/problems/two-furthest-houses-with-different-colors/) · Easy · 灵茶山艾府：[O(n) 做法，脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2078.两栋颜色不同且距离最远的房子

[力扣](https://leetcode.cn/problems/two-furthest-houses-with-different-colors/)

最直观的想法自然是逐对枚举这两栋房子的位置，然后判断当前枚举的位置上的房子颜色是否不同，并更新答案。这个做法的时间复杂度为O(n^2)，对于本题是足够的。

另一个想法是枚举其中一栋房子位置，然后想办法找出另一栋离得最远的房子的位置。

我在这里采用的是枚举右边这一栋房子的位置，然后找离这栋房子最远且颜色不同的左边的房子的位置。很明显，要找的这栋房子就是下标最小且颜色与当前房子不同的房子，那么可以记录最左侧，且颜色与下标为0的房子颜色不同的房子的下标second。

得到second后，对于second右侧的所有房子，其颜色要么与下标为0的房子不同，要么与下标为second的房子不同，换言之，要么是用index来更新答案，要么是用index - second来更新答案。这样一来，总的时间复杂度就优化到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, colors):
        """
        :type colors: List[int]
        :rtype: int
        """

        for index in range(1, len(colors)):
            if colors[index] != colors[0]:
                res = index
                second = index
                break

        for index in range(second + 1, len(colors)):
            if colors[index] == colors[0]:
                res = max(res, index - second)
            else:
                res = max(res, index)
        
        return res
```
