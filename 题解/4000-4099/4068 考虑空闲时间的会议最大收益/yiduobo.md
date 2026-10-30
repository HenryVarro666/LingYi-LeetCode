---
title: "4068. 考虑空闲时间的会议最大收益"
aliases: ["yiduobo的每日leetcode 4068.考虑空闲时间的会议最大收益"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2089040941944403537"
zhihu_id: "2089040941944403537"
zhihu_title: "yiduobo的每日leetcode 4068.考虑空闲时间的会议最大收益"
question_id: "4068"
question: "考虑空闲时间的会议最大收益"
problem_url: "https://leetcode.cn/problems/maximize-meeting-earnings-with-idle-gaps/"
difficulty: "Hard"
created: "2026-10-01T17:32:36+08:00"
updated: "2026-10-01T17:32:39+08:00"
upvotes: 2
comments: 0
---

# 4068. 考虑空闲时间的会议最大收益

> **[yiduobo的每日leetcode 4068.考虑空闲时间的会议最大收益](https://zhuanlan.zhihu.com/p/2089040941944403537) · 知乎 · 2026-10-01 · 赞同 2**
> 力扣：[4068. 考虑空闲时间的会议最大收益](https://leetcode.cn/problems/maximize-meeting-earnings-with-idle-gaps/) · Hard · 灵茶山艾府：[动态规划 + 式子变形（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4068.考虑空闲时间的会议最大收益

<https://leetcode.cn/problems/maximize-meeting-earnings-with-idle-gaps/description/>

题目给出一个二维整数数组meetings，其中meetings\[index\] \= \[start\[index\], end\[index\], revenue\[index\]\]，表示一场会议从start\[index\]开始，到end\[index\]结束，可以获得revenue\[index\]的收益。

所有会议都是左闭右开区间，这也就意味着即使前一场会议的结束时间与后一场会议的起始时间相同，这两场会议也不会被视为重叠。

现在要求找出一个会议的非空子集，其中的会议互不重叠。所获得的收益除了这些会议的固有收益之外，还可以空闲时间的额外收益。空闲时间收益的计算方式为将这些会议按开始时间递增进行排序，对于每一组相邻的会议，期间间隔的时间即为空闲时间，每单位的空闲时间可以获得1单位的收益。

需要注意，第一场会议之前的时间，以及最后一场会议之后的时间均不算做空闲时间，若只选择了一场会议，则不会获得任何空闲时间的收益。

问最大的总收益是多少。

如果不考虑空闲时间收益，本题就是经典的动态规划问题，可以使用排序加二分或者离散化加树状数组进行处理。而有了空闲时间收益之后，直观感觉上使用排序加二分是更好的选择。

具体来说，在不考虑空闲时间的版本中，可以先将所有会议按照结束时间从小到大进行排序。接下来，令f[index]表示前index场会议可以获得的最大收益。那么对于f[index]，如果不召开index这场会议，就有f[index] \= f[index - 1]。反之如果选择召开，则需要找到其在谁的后面召开。由于f是单调递增的，因此就需要找到最大的p，满足end[p] \<\= start[index]，那么在这里就可以用start[index]到end[0]和end[index - 1]直接进行二分，找出这个p，然后就有f[index] \= max(f[index], f[p] + revenue[index])。

接下来，如果需要考虑空闲时间，那么对于f[index]而言，如果从f[index - 1]直接过来不会有任何变化，但是从f[p]过来的话，就需要直到f[p]中真正召开的最后一场会议q是哪一场，然后这里就应该使用f[p] + revenue[index] + start[index] - end[q]来更新f[index]。然而按照上面的计算方法，此时已经丢失了q的信息了，不过还有另一种处理方法就是在更新f[index]时直接将end[q]的信息带上去，即将次数的f[index]改写为f[p] + revenue[index] + start[index] - end[index]，这样一来就不需要考虑这个q到底是哪一场会议了。

不过需要注意的是，此时f的定义产生了变化，而在计算答案时是不应该减去这个end[index]的，需要特别注意。另外对于第一场会议，计算收益时不应该考虑start，但是更新f时还是需要减去end。

最后附上python代码：

```python
class Solution(object):
    def maxEarnings(self, meetings):
        """
        :type meetings: List[List[int]]
        :rtype: int
        """
        
        meetings.sort(key=lambda d:d[1])

        f = []
        res = 0

        for index, (start, end, rev) in enumerate(meetings):
            if start < meetings[0][1]:
                res = max(res, rev)
                if not f:
                    f.append(rev - end)
                else:
                    f.append(max(f[-1], rev - end))
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right + 1) // 2
                    if meetings[mid][1] <= start:
                        left = mid
                    else:
                        right = mid - 1
                
                v = f[left] + rev + start
                res = max(res, v)
                f.append(max(f[-1], v - end))
        
        return res
```
