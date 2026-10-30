---
title: "3279. 活塞占据的最大总面积"
aliases: ["yiduobo的每日leetcode 3279.活塞占据的最大总面积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/794364262"
zhihu_id: "794364262"
zhihu_title: "yiduobo的每日leetcode 3279.活塞占据的最大总面积"
question_id: "3279"
question: "活塞占据的最大总面积"
problem_url: "https://leetcode.cn/problems/maximum-total-area-occupied-by-pistons/"
created: "2024-10-04T01:36:38+08:00"
updated: "2024-10-04T01:36:38+08:00"
upvotes: 1
comments: 0
---

# 3279. 活塞占据的最大总面积

> **[yiduobo的每日leetcode 3279.活塞占据的最大总面积](https://zhuanlan.zhihu.com/p/794364262) · 知乎 · 2024-10-04 · 赞同 1**
> 力扣：[3279. 活塞占据的最大总面积](https://leetcode.cn/problems/maximum-total-area-occupied-by-pistons/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3279.活塞占据的最大总面积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-area-occupied-by-pistons/description/)

题目给出一辆旧车，这辆旧车的引擎中有若干活塞。这些活塞将在高度0到高度height之间来回上下运动，运动的速度为每秒一个单位。当某个活塞高度下降到0时，其下一秒将改为向上运动，反之当某个活塞高度上升到height时，其下一秒将改为向下运动。

现在给出两个数组positions和directions，分别表示每个活塞目前所处的高度，以及这个活塞接下来的运动方向，问在整个运动过程中，所有活塞下方的面积之和的最大值是多少。

题设虽然是要求计算的面积，但是从样例上来看应该是问的所有活塞高度之和的最大值是多少。由于题目中height和活塞数量的规模都不小，因此需要尽量想高效的处理方法。

首先可以明确的是，每经过height \* 2秒，每个活塞都将会恢复到positions和directions中描述的初始状态，也就是说只需要考察初始状态0到第height \* 2 - 1秒时间所有活塞的高度之和就行了。

注意到由于活塞的运动速度为1，这也就意味着所有的活塞在下一秒的取值相对上一秒只会变化1或者-1，而这里是1还是-1，在0都height \* 2 - 1这个过程中也最多产生两次变化，也就是说这里高度的变化情况将形成最多三段全部由1或者-1的区间。基于这一点，就可以在每一秒都先通过差分数组f来计算所有活塞在每一秒的变化值之和，然后通过上一秒的高度之和与变化值之和计算这一秒的高度之和。

具体来说，初始化差分数组f为全0，接下来遍历所有活塞。对于一个初始高度为p，方向为d的活塞：

1、若d为'U'且p不等于height，或者p等于0：

对于这种情况，活塞在下一秒将向上运动持续到第height - p秒，因此在1到height - p秒变化值都是1。

接下来从第height - p + 1开始，活塞将一直下降height秒，即在height - p + 1到height \* 2 - p秒变化值都是-1。

若此时的h非0，那么从第height \* 2 - p + 1开始，活塞将重新开始向上运动，因此在height \* 2 - p + 1到height \* 2秒变化值都是1。

上面三段对应到差分数组分别为(f[1] +\= 1, f[height - p + 1] -\= 1)、(f[height - p + 1] -\= 1, f[height \* 2 - p + 1] +\= 1)、(f[height \* 2 - p + 1] +\= 1, f[height \* 2] -\= 1)。

由于大于等于height \* 2的高度都无需计算，因此在这里需要设置的是

f[1] +\= 1

f[height - p + 1] -\= 2

同时在p !\= 0时设置f[height \* 2 - p + 1] +\= 2

2、反之，若不属于第一种情况：

与上面的处理方法类似，对于这种情况，先分析活塞按同一方向运动的时间段：活塞在下一秒将向下运动持续到第p秒，在第p + 1秒到第height + p秒向上运动，当p不等于height时在第height + p + 1秒到第heigth \* 2秒向下运动，因此需要设置的是

f[1] -\= 1

f[p + 1] +\= 2

同时在p !\= height时设置f[height + p + 1] +\= 2

得到完整的f数组后，初始化当前高度now为初始高度之和sum(positions)，同时初始化高度变化值delta为0。接下来从第1秒遍历到第heigth \* 2 - 1秒，对于当前遍历到的第t秒，先利用f[t]数组来更新高度的变化delta，然后利用delta来更新now，并通过now来更新最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxArea(self, height, positions, directions):
        """
        :type height: int
        :type positions: List[int]
        :type directions: str
        :rtype: int
        """

        f = [0] * (height * 2 + 1)
        for p, d in zip(positions, directions):
            if p == 0 or (d == 'U' and p != height):
                f[1] += 1
                f[height - p + 1] -= 2
                if p != 0:
                    f[height * 2 - p + 1] += 2
            else:
                f[1] -= 1
                f[p + 1] += 2
                if p != height:
                    f[height + p + 1] -= 2
        
        now = sum(positions)
        res = now
        delta = 0
        for t in range(1, height * 2):
            delta += f[t]
            now += delta
            res = max(res, now)
        
        return res
```
