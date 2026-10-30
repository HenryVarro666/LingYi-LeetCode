---
title: "1901. 找出顶峰元素II"
aliases: ["yiduobo的每日leetcode 1901.找出顶峰元素II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/matrix", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/480936361"
zhihu_id: "480936361"
zhihu_title: "yiduobo的每日leetcode 1901.找出顶峰元素II"
question_id: "1901"
question: "寻找峰值 II"
problem_url: "https://leetcode.cn/problems/find-a-peak-element-ii/"
difficulty: "Medium"
created: "2022-03-14T22:10:39+08:00"
updated: "2022-03-14T22:10:39+08:00"
upvotes: 0
comments: 0
---

# 1901. 找出顶峰元素II

> **[yiduobo的每日leetcode 1901.找出顶峰元素II](https://zhuanlan.zhihu.com/p/480936361) · 知乎 · 2022-03-14 · 赞同 0**
> 力扣：[1901. 寻找峰值 II](https://leetcode.cn/problems/find-a-peak-element-ii/) · Medium · 灵茶山艾府：[【图解】利用行最大值判断峰顶位置，附二分题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1901.找出顶峰元素II

[力扣](https://leetcode-cn.com/problems/find-a-peak-element-ii/)

经典的分治题，不妨先从一维的角度开始考虑。

对于一个长度为n的数组，数组中的元素各不相同，要如何在O(logn)的时间内找到其中的任意一个极大值。

对于log(n)这个复杂度，意味着每一轮必须直接舍弃掉当前剩余数组的一半，那么在这里就必须保证留下的这一半中存在极大值。不妨设这个数组为a，长度为n，那么左半边，即1到(n + 1) / 2这一段里面没有极大值的唯一一种可能就是a[1] \< a[2] \< ... \< a[(n + 1) / 2]，同时a[(n + 1) / 2]自身也不能是极大值，因此还需要满足a[(n + 1) / 2] \< a[(n + 1) / 2 + 1]。

也就是说，对于长度为n的数组，若满足a[(n + 1) / 2] \< a[(n + 1) / 2 + 1]，那么右侧必然存在极大值，否则左侧必然存在极大值。此时只需要根据这个结果递归求解相应的半边即可。

想清楚了一维的情况，那么对于二维的情况，则也同样是尝试将矩阵分为左右两个部分。不过这里稍微复杂一些的地方是，一维数组是两个数接壤，而二维矩阵则是整条中线接壤。另一方面，二维矩阵需要考察四个方向，因此可能出现接壤处的两个数满足左边大于右边，但是从这个数开始往左半边矩阵中存在一条路径满足每个数单调递增，然后通过另一处接壤的地方进入了右半边矩阵，也就是说单个接壤的数并不能保证其所在行中存在极大值。

为了避免上面说的这种情况，一个想法就是先办法把接壤的这条线堵死，让上面所说的单调递增路径只能在本侧内部延伸，从而保证极大值处于本侧。一个自然的想法就是从中线的最大值开始，即对于左右两条中线，分别存在一个最大值，那么对于这两个最大值中较大的那一个。由于左右是对称的，那么在这里不妨设左侧的大于右侧的，那么对于左侧的这个值，设其为x：

1、由于其是中线的最大值，因此x必然大于上下两侧的值

2、根据假设，x大于右侧的值

3、若x大于左侧的值，那么x本身就是一个极大值；若x小于左侧的值，那么从x左侧的值开始延展单调递增路径，可以保证这个路径不可能从其他位置越过中线，因为路径上的数都大于x，而中线上的其他值都小于x。这样一来，就保证了x所在的左半边存在一个极大值

根据上面的结论，就可以按类似一维的方式，每次将矩阵分为左右两半，然后遍历两条中线，对比中线上的最大值后选择一半的矩阵进行递归求解。

具体实现上，由于习惯了操作行，因此我在这里选择的是分成上下两个矩阵求解。

最后附上python代码：

```python
class Solution(object):
    def findPeakGrid(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: List[int]
        """

        m = len(mat)
        n = len(mat[0])
        l = 0
        r = m - 1
        while l < r:
            mid = (l + r) >> 1
            top_max = 0
            for num in mat[mid]:
                top_max = max(top_max, num)
            
            bottom_max = 0
            for num in mat[mid + 1]:
                bottom_max = max(bottom_max, num)
            
            if top_max > bottom_max:
                r = mid
            else:
                l = mid + 1
        
        ma = mat[l][0];
        res_y = 0
        for index in range(1, n):
            if mat[l][index] > ma:
                ma = mat[l][index];
                res_y = index
        
        return [l, res_y]
```
