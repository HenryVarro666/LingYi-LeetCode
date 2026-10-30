---
title: "1906. 查询差绝对值的最小值"
aliases: ["yiduobo的每日leetcode 1906.查询差绝对值的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/482227636"
zhihu_id: "482227636"
zhihu_title: "yiduobo的每日leetcode 1906.查询差绝对值的最小值"
question_id: "1906"
question: "查询差绝对值的最小值"
problem_url: "https://leetcode.cn/problems/minimum-absolute-difference-queries/"
difficulty: "Medium"
created: "2022-03-17T00:21:44+08:00"
updated: "2022-03-17T00:21:44+08:00"
upvotes: 0
comments: 0
---

# 1906. 查询差绝对值的最小值

> **[yiduobo的每日leetcode 1906.查询差绝对值的最小值](https://zhuanlan.zhihu.com/p/482227636) · 知乎 · 2022-03-17 · 赞同 0**
> 力扣：[1906. 查询差绝对值的最小值](https://leetcode.cn/problems/minimum-absolute-difference-queries/) · Medium · 灵茶山艾府：[前缀和，或者二分位置](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1906.查询差绝对值的最小值

[力扣](https://leetcode-cn.com/problems/minimum-absolute-difference-queries/)

题目要问区间内最接近的两个数。虽然是区间问题，但是这里不太适合用线段树之类的结构，因为在这里两个子段之间合并时答案可能出自子段中的任意位置，也就没法抽象成某几个具体的值来进行储存了。

不过注意到题目这里nums的数值规模很小，那么可以从这一点入手。

由于题目要找的是绝对值差的最小值，因此可以从1到100枚举当前值，若其存在于区间l到r直接，那么就计算当前值与上一个存在于区间中的值的绝对值差，并更新答案。这样做的理由是每个数只可能跟存在于区间中且最近的数形成答案，例如3,5,6都存在于区间中，那么只需要考虑3和5以及5和6，3是没有理由越过5去和6组队的。

这样一来，只需要可以高效确定区间l到r之间是否存在某个数就行了。对于这个问题，还有占了数值规模小的便宜，可以对每个数都弄一个前缀数组，通过区间问题转化为前缀问题的做法来求解。

最后附上python代码：

```python
class Solution(object):
    def minDifference(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        pos_dict = {}
        for num in range(1, 101):
            pos_dict[num] = [0]
        pos_dict[nums[0]][0] = 1
        for index in range(1, len(nums)):
            for num in range(1, 101):
                pos_dict[num].append(pos_dict[num][-1])
            pos_dict[nums[index]][-1] += 1

        res = []        
        for x, y in queries:
            last = None
            now = None
            for num in range(1, 101):
                cnt = pos_dict[num][y]
                if x > 0:
                    cnt -= pos_dict[num][x - 1]
                if cnt > 0:
                    if last is not None and ((now is None) or (now > num - last)):
                        now = num - last
                    last = num
        
            if now is None:
                res.append(-1)
            else:
                res.append(now)
        
        return res
```
