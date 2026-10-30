---
title: "1024. 视频拼接"
aliases: ["yiduobo的每日leetcode 1024.视频拼接"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369172151"
zhihu_id: "369172151"
zhihu_title: "yiduobo的每日leetcode 1024.视频拼接"
question_id: "1024"
question: "视频拼接"
problem_url: "https://leetcode.cn/problems/video-stitching/"
created: "2021-04-30T23:39:20+08:00"
updated: "2021-04-30T23:39:20+08:00"
upvotes: 0
comments: 0
---

# 1024. 视频拼接

> **[yiduobo的每日leetcode 1024.视频拼接](https://zhuanlan.zhihu.com/p/369172151) · 知乎 · 2021-04-30 · 赞同 0**
> 力扣：[1024. 视频拼接](https://leetcode.cn/problems/video-stitching/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1024.视频拼接

[力扣](https://leetcode-cn.com/problems/video-stitching/)

题目要求选出若干区间，这些区间可以覆盖住0到T这个大区间。

首先，我们显然需要一个左边界为0的区间，即我们需要从所有左边界为0的区间中挑选一个。由于这里选择每个区间的代价一样，因此我们应该选择一个右边界最大的区间。不妨设这个右边界为p，若p小于T，那么我们需要继续选择新的区间。此时可选的区间就是左边界小于等于p的所有区间。同样地，我们也应当选择其中右边界最大的区间。于是我们可以每次都选择当前可选区间中右边界最大的，然后根据这个右边界更新当前可选区间的集合，重复此过程直到某一时刻右边界大于等于T，或者可选区间的集合为空。

为了方便这个选取过程，我们可以将区间按左边界从小到大进行排序，然后使用一个变量pos维护当前可选区间的最大下标。

最后附上python代码：

```python
class Solution(object):
    def videoStitching(self, clips, T):
        """
        :type clips: List[List[int]]
        :type T: int
        :rtype: int
        """

        if T == 0:
            return 0

        now = 0
        res = 0
        pos = 0
        sorted_clips = sorted(clips, key=lambda d:(d[0], d[1]))
        n = len(sorted_clips)
        while pos < n:
            next = 0
            while pos < n and sorted_clips[pos][0] <= now:
                next = max(next, sorted_clips[pos][1])
                pos += 1
            
            if next == 0:
                return -1

            now = next
            res += 1
            if now >= T:
                return res

        return -1
```
