---
title: "4001. 聚合两个时间序列"
aliases: ["yiduobo的每日leetcode 4001.聚合两个时间序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/simulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2065237525082419673"
zhihu_id: "2065237525082419673"
zhihu_title: "yiduobo的每日leetcode 4001.聚合两个时间序列"
question_id: "4001"
question: "聚合两个时间序列"
problem_url: "https://leetcode.cn/problems/aggregate-two-time-series/"
difficulty: "Medium"
rating: 1506
created: "2026-07-28T01:03:45+08:00"
updated: "2026-07-28T01:03:46+08:00"
upvotes: 2
comments: 0
---

# 4001. 聚合两个时间序列

> **[yiduobo的每日leetcode 4001.聚合两个时间序列](https://zhuanlan.zhihu.com/p/2065237525082419673) · 知乎 · 2026-07-28 · 赞同 2**
> 力扣：[4001. 聚合两个时间序列](https://leetcode.cn/problems/aggregate-two-time-series/) · Medium · 灵茶山艾府：[双指针，合并两个有序列表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4001.聚合两个时间序列

<https://leetcode.cn/problems/aggregate-two-time-series/description/>

题目给出两个二维整数数组series1和series2。

两个序列中的每个元素都表示为[timestamp, value]，其中timestamp是表示时间的整数，value则是表示这个时间点对应值的整数。

这两个数组都按照timestamp严格递增排列。

若某个序列中某个时间戳缺失，且该序列中存在更晚的时间戳，同时另一个序列中存在这个缺失的时间戳，就将该序列中缺失的时间戳的值设置为下一个更晚时间戳对应的值，否则该时间点的值为0。

例如\[\[1, 3\], \[4,1\]\]以及\[2, 2\]这两个序列。

第一个序列在时间戳为2时缺失，但是其存在后续时间戳等于4的时间点，同时另一个序列中存在2这个时间戳，因此第一个序列在时间点2的值就是其下一个更晚时间戳，也就是4对应的值1。

反过来，第二个序列中在时间戳为4时缺失，其后续不存在更大的时间戳，因此即使第一个序列中存在4这个时间戳，第二个序列中时间点4的值由于不存在下一个更晚的时间戳，因此值为0。

现在要求将这两个时间序列聚合。对于这两个序列中出现过的每个时间戳，将这两个序列在该时间点对应的值相加。要求返回合并后的时间序列，依然按照timestamp递增排列。

从题目描述上来看，有序列表的合并要求还是有序列表，很容易想到二路归并。再进一步考察合并的规则，可以发现，在二路归并的过程中：

1、若只有一方存在，另一方不存在：

此时可以直接使用存在这一方的值。

理由是按照题目的描述，另一方已经不存在了，因此后续也必然不具备更大的时间戳，在当前时间点的值将被认为是0，累加后就等于存在的这一方对应的值。

更进一步的，归并的条件就可以限点为两方都存在，否则直接将剩余的一方拼接到答案的末尾就行了。

2、若两方都存在且时间戳相同：

此时将当前的时间戳，以及双方对应的值之和添加到答案中即可。

需要注意，这种情况下双方的索引都应该向后移动。

3、若两方都存在且时间戳不同：

此时应该先合并时间戳较小的那一方。根据题目的描述，时间戳较大的那一方，显然是没有较小的时间戳这一项的，否则就会命中情况2。因此，此时时间戳较大的的那一方的值，就应该取比较小时间戳的下一个时间戳对应的值，这个值恰好就是当前较大时间戳那一方对应的值。换言之，合并后的值恰好也是两方的值累加起来。

因此在这种情况下，将较小的时间戳以及双方对应的值之和添加到答案中即可。

需要注意，此时只应该移动时间戳较小的那一方的索引。

最后附上python代码：

```python
class Solution(object):
    def aggregateTimeSeries(self, series1, series2):
        """
        :type series1: List[List[int]]
        :type series2: List[List[int]]
        :rtype: List[List[int]]
        """
        
        i, j = 0, 0
        res = []
        while i < len(series1) and j < len(series2):
            res.append([min(series1[i][0], series2[j][0]), series1[i][1] + series2[j][1]])
            if res[-1][0] == series1[i][0]:
                i += 1
            if res[-1][0] == series2[j][0]:
                j += 1
        
        res.extend(series1[i:])
        res.extend(series2[j:])
        return res
```
