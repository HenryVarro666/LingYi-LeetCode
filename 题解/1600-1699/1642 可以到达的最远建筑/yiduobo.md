---
title: "1642. 可以到达的最远建筑"
aliases: ["yiduobo的每日leetcode 1642.可以到达的最远建筑"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/439285933"
zhihu_id: "439285933"
zhihu_title: "yiduobo的每日leetcode 1642.可以到达的最远建筑"
question_id: "1642"
question: "可以到达的最远建筑"
problem_url: "https://leetcode.cn/problems/furthest-building-you-can-reach/"
created: "2021-11-30T00:30:16+08:00"
updated: "2021-11-30T00:30:16+08:00"
upvotes: 1
comments: 0
---

# 1642. 可以到达的最远建筑

> **[yiduobo的每日leetcode 1642.可以到达的最远建筑](https://zhuanlan.zhihu.com/p/439285933) · 知乎 · 2021-11-30 · 赞同 1**
> 力扣：[1642. 可以到达的最远建筑](https://leetcode.cn/problems/furthest-building-you-can-reach/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1642.可以到达的最远建筑

[力扣](https://leetcode-cn.com/problems/furthest-building-you-can-reach/)

首先向高度更低的建筑走是没有任何代价的，因此在这里只需要考虑向高度更高的建筑走应该如何规划砖块和梯子的使用。

由于题目中的梯子是任意梯可以使用任何高度差，那么很明显应该将梯子用在落差最大的建筑之间。但是对于这些落差很大的建筑，一开始是无法确定能否到达的。如果一味保留梯子的话可能根本就走不到这些高度落差很大的建筑。于是一个自然的想法是尽量保留梯子，只有当不得已的时候拿出来用，同时也必须满足用在当前最划算的位置上。换言之，就是对于可以通过砌砖到达的建筑，一律使用砌砖，并将这些操作花费的砖块数量记录下来。当某一时刻砖块不够时，则考虑使用梯子。设此时需要砌砖的数量为diff，那么有下面几种情况：

1、剩余梯子的数量为0：

此时说明梯子已经填到了之前所需砖块最多的位置上，因此无论怎么调整梯子的位置，所剩的砖块都只会只少不多，无论如何都是不够的diff的，因此只能到此为止了，答案就是这一栋建筑的位置减一。

2、剩余梯子的数量大于0：

此时一定要用掉一架梯子，但是用的位置有讲究。理想的情况是这架梯子用在了花费砖块最多的位置，那么这个位置必然就是之前砌砖花费砖块最多的位置，与当前位置这二者中花费砖块较多的一个。为了高效得到之前砌砖花费砖块最多是多少，可以使用一个堆来维护之前所有砌砖操作花费的砖块量，那么这里最多的花费量就是堆顶heap[0]。

比较heap[0]与diff，若heap[0] > diff，说明此时应该用梯子填补heap[0]这个位置，从而解放出heap[0]的砖块数目。使用其中的diff块搭建当前位置的梯子后，还剩下heap[0] - diff的砖块，将其累积到剩余砖块中，同时将diff加入到堆中。若heap[0] \<\= diff，那么此时直接在当前位置使用梯子是最划算的，因此无需操作堆和剩余砖块数。无论是哪种情况，最后都要将梯子的数量减一。

如果没有中途退出，那么说明可以到达最后一栋建筑，此时的答案就应该是len(heights) - 1了。

最后附上python代码：

```python
class Solution(object):
    def furthestBuilding(self, heights, bricks, ladders):
        """
        :type heights: List[int]
        :type bricks: int
        :type ladders: int
        :rtype: int
        """

        heap = []
        for index in range(1, len(heights)):
            if heights[index] > heights[index - 1]:
                diff = heights[index] - heights[index - 1]
                if diff <= bricks:
                    bricks -= diff
                    heapq.heappush(heap, -diff)
                elif ladders > 0:
                    if heap and -heap[0] > diff:
                        bricks += -heapq.heappop(heap) - diff
                        heapq.heappush(heap, -diff)
                    ladders -= 1
                else:
                    return index - 1

        return len(heights) - 1
```
