---
title: "1889. 装包裹的最小浪费空间"
aliases: ["yiduobo的每日leetcode 1889.装包裹的最小浪费空间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/prefix-sum", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/478451822"
zhihu_id: "478451822"
zhihu_title: "yiduobo的每日leetcode 1889.装包裹的最小浪费空间"
question_id: "1889"
question: "装包裹的最小浪费空间"
problem_url: "https://leetcode.cn/problems/minimum-space-wasted-from-packaging/"
difficulty: "Hard"
rating: 2214
created: "2022-03-09T23:49:00+08:00"
updated: "2022-03-09T23:49:00+08:00"
upvotes: 1
comments: 0
---

# 1889. 装包裹的最小浪费空间

> **[yiduobo的每日leetcode 1889.装包裹的最小浪费空间](https://zhuanlan.zhihu.com/p/478451822) · 知乎 · 2022-03-09 · 赞同 1**
> 力扣：[1889. 装包裹的最小浪费空间](https://leetcode.cn/problems/minimum-space-wasted-from-packaging/) · Hard · 灵茶山艾府：[贪心+二分：使箱子的尺寸之和尽可能地小](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1889.装包裹的最小浪费空间

[力扣](https://leetcode-cn.com/problems/minimum-space-wasted-from-packaging/)

由于题目中每个箱子只能装一个包裹，那么为了使浪费的空间最小，很明显就应该选择容量最小的，但大于等于包裹大小的箱子。

对于箱子的选择，可以通过排序后二分，或者排序后的单调性来求解。我在这里采用的是排序后利用单调性，需要注意的是，由于题目中的箱子是分组的，因此需要一些特别的处理。

将所有箱子标记好其所属的组之后按容积从小到大排序，同时将所有包裹按大小从小到大排序。另外，还需要使用一个数组deal，其中deal[index]表示使用index这一组的箱子当目前位置可以处理哪些包裹。接下里对遍历每个箱子，并使用一个变量p表示当前箱子可以装下的最大包裹的下标。随着遍历的进行，p必然是逐渐增大的，因此可以在均摊O(1)的时间内求出每个箱子可以装下的最大包裹的下标。

对于当前箱子，不妨设其是属于index这个组的，容积为v。那么如果最终选择的是index这个组的箱子，那么下标小于等于deal[index]的所有包裹可以由当前箱子之前的箱子来满足，而对于deal[index] + 1到p之间的包裹，则需要选择当前箱子。

从deal[index] + 1到p之间一共有p - deal[index]个箱子，那么浪费的空间就是(p - deal[index]) \* v - (boxes[deal[index] + 1] + boxes[deal[index] + 2] + ... + boxes[p])，后面这个连加很自然想到使用前缀和来优化。将这个浪费的值累加到index这一组箱子浪费空间的总和当中，然后更新deal[index]到p即可。

全部计算完成后，若某组箱子对应的deal等于n - 1，说明该组箱子可以装下所有的包裹，那么使用该组箱子浪费的空间来更新答案，否则说明该组箱子不够大，无法装下所有的包裹，直接忽略掉就好。

最后附上python代码：

```
class Solution(object):
    def minWastedSpace(self, packages, boxes):
        """
        :type packages: List[int]
        :type boxes: List[List[int]]
        :rtype: int
        """

        box_info = []
        m = len(boxes)
        for index in range(m):
            for v in boxes[index]:
                box_info.append([v, index])
        
        box_info = sorted(box_info, key=lambda d:d[0])
        
        n = len(packages)
        sorted_packages = sorted(packages)
        s = [sorted_packages[0]]
        for package in sorted_packages[1:]:
            s.append(s[-1] + package)
        
        dealed = [-1] * m
        cost = [0] * m
        p = -1
        mod = 10 ** 9 + 7
        for v, index in box_info:
            while p + 1 < n and sorted_packages[p + 1] <= v:
                p += 1
            
            if p > dealed[index]:
                cnt = p - dealed[index]
                cost[index] += cnt * v - s[p]
                if dealed[index] >= 0:
                    cost[index] += s[dealed[index]]
                dealed[index] = p

        res = -1
        for index in range(m):
            if dealed[index] == n - 1 and (res == -1 or res > cost[index]):
                res = cost[index]
        
        if res != -1:
            res %= mod

        return res
```
