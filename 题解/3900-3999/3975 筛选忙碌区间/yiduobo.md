---
title: "3975. 筛选忙碌区间"
aliases: ["yiduobo的每题leetcode 3975.筛选忙碌区间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2054646397996110897"
zhihu_id: "2054646397996110897"
zhihu_title: "yiduobo的每题leetcode 3975.筛选忙碌区间"
question_id: "3975"
question: "筛选忙碌区间"
problem_url: "https://leetcode.cn/problems/filter-occupied-intervals/"
difficulty: "Medium"
rating: 1533
created: "2026-06-28T19:34:17+08:00"
updated: "2026-06-28T19:34:30+08:00"
upvotes: 1
comments: 0
---

# 3975. 筛选忙碌区间

> **[yiduobo的每题leetcode 3975.筛选忙碌区间](https://zhuanlan.zhihu.com/p/2054646397996110897) · 知乎 · 2026-06-28 · 赞同 1**
> 力扣：[3975. 筛选忙碌区间](https://leetcode.cn/problems/filter-occupied-intervals/) · Medium · 灵茶山艾府：[两种合并区间写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3975.筛选忙碌区间

<https://leetcode.cn/problems/filter-occupied-intervals/description/>

题目给出一个二维整数数组occupiedIntervals，其中occupiedIntervals\[index\] \= \[start\[index\], end\[index\]\]，表示在start\[index\]到end\[index\]这一段时间是忙碌的，包含两个端点。

另外给出两个整数freeStart和freeEnd，表示一个空闲的事件区间，同样包含两个端点。

现在要求将所有重叠或者相连的忙碌区间合并，然后从中移除掉空闲区间内的整数点。

要求按升序返回最终留下的合并后忙碌区间，若没有剩余区间，则返回空列表。

首先，按照题目要求对忙碌区间进行合并。具体来说，按区间起点从小到大进行排序，然后一趟遍历，使用now_x和now_y记录当前合并中的区间端点，然后遍历所有区间，对于当前区间[x, y]，若x小于等于now_y + 1，说明区间是重叠或者相连的，此时应该使用y来更新now_y，否则说明[now_x, now_y]已经定型，此时将其加入到合并后的区间数组中，然后将now_x和now_y更新为x、y即可。

合并完成后，还需要从中剔除掉与空闲区间重叠的部分。

遍历所有合并后的区间，对于当前遍历到的区间[x, y]，可以先判断其是否与空闲区间重叠。若y \< freeStart，或者x > freeEnd，说明区间不重叠，此时直接将[x, y]加入到答案中。

反之，则可以找出[x, y]与空闲区间重叠的区间部分[overlap_x, overlap_y]，其中overlap_x为两个区间起点的较大值，overlap_y为两个区间中点的较小值。接下来，若x与overlap_x之间，以及overap_y与y之间都可能存在空隙：若x \< overlap_x，那么[x, overlap_x - 1]是忙碌区间，需要加入到答案中；若overlap_y \< y，那么[overlap_y + 1, y]是忙碌区间，也需要加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def filterOccupiedIntervals(self, occupiedIntervals, freeStart, freeEnd):
        """
        :type occupiedIntervals: List[List[int]]
        :type freeStart: int
        :type freeEnd: int
        :rtype: List[List[int]]
        """
        
        occupiedIntervals.sort()

        now_x, now_y = occupiedIntervals[0]
        merged = []
        for x, y in occupiedIntervals:
            if now_y + 1 >= x:
                now_y = max(now_y, y)
            else:
                merged.append([now_x, now_y])
                now_x, now_y = x, y
        
        merged.append([now_x, now_y])

        res = []
        for x, y in merged:
            if freeStart > y or freeEnd < x:
                res.append([x, y])
            else:
                overlap_x = max(x, freeStart)
                overlap_y = min(y, freeEnd)
                if x < overlap_x:
                    res.append([x, overlap_x - 1])
                if overlap_y < y:
                    res.append([overlap_y + 1, y])

        return res
```
