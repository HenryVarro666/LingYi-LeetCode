---
title: "755. 倒水"
aliases: ["yiduobo的每日leetcode 755.倒水"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605784018"
zhihu_id: "605784018"
zhihu_title: "yiduobo的每日leetcode 755.倒水"
question_id: "755"
question: "倒水"
problem_url: "https://leetcode.cn/problems/pour-water/"
created: "2023-02-13T00:48:32+08:00"
updated: "2023-02-13T00:48:32+08:00"
upvotes: 0
comments: 0
---

# 755. 倒水

> **[yiduobo的每日leetcode 755.倒水](https://zhuanlan.zhihu.com/p/605784018) · 知乎 · 2023-02-13 · 赞同 0**
> 力扣：[755. 倒水](https://leetcode.cn/problems/pour-water/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

755.倒水

[力扣](https://leetcode.cn/problems/pour-water/)

题目中倒水的规则使用文字描述起来反而不如想象生活中往参差不齐的网格中倒水时水的流动规则来得方便。不过有一点不同的是，生活中倒水时水最后会平摊到相同高度的连续格子当中，而对于本题，如果确定的最终位置与其他高度相同的位置相邻，水也只会停留在离落点k最近的这个位置上，通过样例1中的第一滴水可以很清楚地看到这个区别。

使用单调性分析配合数据结构应该可以得到一种时间复杂度非常高效的算法，但是细节处理起来应该比较麻烦。由于本题的操作次数v不超过2000，而整个网格的长度不超过100，因此直接暴力计算就行了。

对于每次操作：

1、首先从k开始向左遍历，到首个非单调不增的位置停止，在遍历过程中记录最后一次落差出现的位置。若存在这个落差出现的位置，那么水最终就会留在这个落差的下方

2、否则就从k开始向右遍历，同样是到首个非单调不增的位置停止，也同样是记录最后一次落差出现的位置。若存在，那么水最终就会留在落差的下方

3、若1和2都不符合，那么水最终就会留在k

最后附上python代码：

```python
class Solution(object):
    def pourWater(self, heights, volume, k):
        """
        :type heights: List[int]
        :type volume: int
        :type k: int
        :rtype: List[int]
        """

        for _ in range(volume):
            p = k
            choose = k
            while p - 1 >= 0 and heights[p - 1] <= heights[p]:
                if heights[p - 1] < heights[p]:
                    choose = p - 1
                p -= 1

            if choose != k:
                heights[choose] += 1
                continue
            
            p = k
            choose = k
            while p + 1 < len(heights) and heights[p + 1] <= heights[p]:
                if heights[p + 1] < heights[p]:
                    choose = p + 1
                p += 1

            if choose != k:
                heights[choose] += 1
                continue
            
            heights[k] += 1
        
        return heights
```
