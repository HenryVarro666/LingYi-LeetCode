---
title: "2736. 最大和查询"
aliases: ["yiduobo的每日leetcode 2736.最大和查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/sorting", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/单调栈", "题单/常用数据结构/八-树状数组和线段树", "题单/常用数据结构/专题-离线算法", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652938019"
zhihu_id: "652938019"
zhihu_title: "yiduobo的每日leetcode 2736.最大和查询"
question_id: "2736"
question: "最大和查询"
problem_url: "https://leetcode.cn/problems/maximum-sum-queries/"
difficulty: "Hard"
rating: 2533
created: "2023-08-29T02:48:00+08:00"
updated: "2023-08-29T02:48:00+08:00"
upvotes: 0
comments: 0
---

# 2736. 最大和查询

> **[yiduobo的每日leetcode 2736.最大和查询](https://zhuanlan.zhihu.com/p/652938019) · 知乎 · 2023-08-29 · 赞同 0**
> 力扣：[2736. 最大和查询](https://leetcode.cn/problems/maximum-sum-queries/) · Hard · 灵茶山艾府：[排序+单调栈上二分（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2736.最大和查询

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-sum-queries/)

对于题目中的数组，可以认为是在二维平面上的位置(nums1[i], nums2[i])存在一个值为nums1[i] \* nums2[i]的点，接下来的询问(xi, yi)则可以认为是问在(xi, yi)的右上方的所有点中值最大的是多少。

在x和y的规模比较小的情况下，如果是静态的询问可以使用二维差分数组，而动态的则可以使用二维树状数组。而本题的数据规模比较大，那么一种可行的处理方法就是坐标进行离散化，但是极限情况离散化后的坐标大小依然可以来到10^5，二维系列的东西还是不能用，不过在这里就可以采用对x排序然后用树状数组维护y的做法。

我在这里采用的方法略有不同，是针对一维提前排序，然后在另一维排序过程中进行计算。具体来说，就是首先将所有(nums1[i], nums2[i])的点以及所有询问的点(xi, yi)都收集起来，其中前一类点的值依然是nums1[i] \* nums2[i]，而后一类的点值则可以取-i，方便排序以及定位到最终答案。为了方便描述，后面称前一类点为数据点，后一类点为询问点。

不妨记收集所有点的数组为info，接下来则需要对info以x这一维为第一关键字，数值这一维为第二关键字，从大到小进行排序。这样一来，对于排序后info中的任何询问点，所有满足x坐标大于等于当前询问点x坐标的数据点，就都被排到了当前询问点的前面，也就是说x坐标现在已经满足条件了。在这里就可以说明之前为什么取-i作为询问点的数值，因为这样一来就可以保证在排序后可以将x坐标相同的数据点排到询问点的前面。

接下来则需要想办法处理y这一维。一种可行的做法是对排序后的info，以y坐标为关键字从大到小执行归并排序。

在归并排序执行的过程中，区间[left, right]将被分成[left, mid]到[mid + 1, right]这两个部分，由于info已经按x坐标排序过，因此[left, mid]区间中所有点的x坐标一定是小于等于[mid + 1, right]区间中所有点的x坐标，也就是说只要[left, mid]区间中某个数据点的y坐标大于等于[mid + 1,right]区间中某个询问点的y坐标，那么就可以使用前者的数值来更新后者对应的答案了。而对于这个大于等于，在左右区间执行二路归并的过程中则是天然满足的，也就是说在二轮归并执行到右侧区间某个询问点时，左侧区间中所有满足y坐标大于等于当前询问点的数据点都已经被遍历过了，那么只需使用一个变量记录当前已经遍历过的左侧区间中的数据点的数值中的最大值，就可以使用这个最大值更新后续右侧区间的询问点的结果了。

而对于单侧区间内部的数据点以及询问点的配对，则在递归求解左右区间的过程中就被处理掉了，也就是说上面这种处理方法不会遗漏任何合法的数对。

最后附上python代码：

```python
class Solution(object):
    def maximumSumQueries(self, nums1, nums2, queries):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        info = []
        for x, y in zip(nums1, nums2):
            info.append([x, y, x + y])
        
        for index, (x, y) in enumerate(queries):
            info.append([x, y, -index])
        
        info.sort(key=lambda d:(d[0], d[2]), reverse=True)
        
        res = [-1] * len(queries)

        def merge(info, left, right, res):
            if left == right:
                return
                
            mid = (left + right) / 2

            merge(info, left, mid, res)
            merge(info, mid + 1, right, res)

            i = left
            j = mid + 1
            ma = -1
            tmp = []
            while i <= mid and j <= right:
                if info[i][1] >= info[j][1]:
                    x, y, v = info[i]
                    if v > 0:
                        ma = max(ma, v)
                    i += 1
                    tmp.append([x, y, v])
                else:
                    x, y, v = info[j]
                    if v <= 0:
                        res[-v] = max(res[-v], ma)
                    j += 1
                    tmp.append([x, y, v])
            
            while i <= mid:
                x, y, v = info[i]
                i += 1
                tmp.append([x, y, v])
            
            while j <= right:
                x, y, v = info[j]
                if v <= 0:
                    res[-v] = max(res[-v], ma)
                j += 1
                tmp.append([x, y, v])

            for index in range(len(tmp)):
                info[index + left] = tmp[index][:]

        merge(info, 0, len(info) - 1, res)
        
        return res
```
