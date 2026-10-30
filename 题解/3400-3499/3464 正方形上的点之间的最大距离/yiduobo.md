---
title: "3464. 正方形上的点之间的最大距离"
aliases: ["yiduobo的每日leetcode 3464.正方形上的点之间的最大距离"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/backtracking", "题单/滑动窗口与双指针", "题单/二分算法", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/数学算法", "题单/滑动窗口与双指针/五-三指针", "题单/二分算法/二-二分答案", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/七-其他线性-DP", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1895583618363008286"
zhihu_id: "1895583618363008286"
zhihu_title: "yiduobo的每日leetcode 3464.正方形上的点之间的最大距离"
question_id: "3464"
question: "正方形上的点之间的最大距离"
problem_url: "https://leetcode.cn/problems/maximize-the-distance-between-points-on-a-square/"
difficulty: "Hard"
rating: 2806
created: "2025-04-15T21:53:02+08:00"
updated: "2025-04-15T21:53:02+08:00"
upvotes: 0
comments: 0
---

# 3464. 正方形上的点之间的最大距离

> **[yiduobo的每日leetcode 3464.正方形上的点之间的最大距离](https://zhuanlan.zhihu.com/p/1895583618363008286) · 知乎 · 2025-04-15 · 赞同 0**
> 力扣：[3464. 正方形上的点之间的最大距离](https://leetcode.cn/problems/maximize-the-distance-between-points-on-a-square/) · Hard · 灵茶山艾府：[五种方法：二分套二分 / k 指针 / 倍增 / DFS / 动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3464.正方形上的点之间的最大距离

[3464. 正方形上的点之间的最大距离 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-the-distance-between-points-on-a-square/)

题目给出一个整数side，表示有一个边长为side的正方形，正方形的四个角分别位于笛卡尔平面的(0, 0)，(0, side)，(side, 0)，(side, side)。

同时给出一个正整数k以及一个二维整数数组points，其中points\[index\] \= \[x\[index\], y\[index\]\]，表示一个在正方形边界上的点。题目保证points中的所有点都位于正方形边界上，且互不相同。

现在要求从中找出k个点，使得任意两个点之间的最小曼哈顿距离最大，问这个最大的距离可能是多少。

由于points中的所有点都位于正方形的边上，那么如果将这些点从左下角开始按照顺时针排序，选出来的点之间的最小曼哈顿距离必然出现在相邻的点之间，可以使用反证法给出简单的证明。设最小的曼哈顿距离出现在不相邻的两点a和b之间，另外按顺时针排布时a在b的前面，那么：

1、这a和b位于同一条边上：

这种情况最直观。由于这a和b不相邻，那么a和b之间必然存在某个点c，而c到a的距离加上c到b的距离刚好等于a到b的距离，因此a到b的距离显然不是最小的。

2、这a和b位于相邻的边上：

这种情况下，a到b的距离就是从a先走到正方形的某个顶点，然后从这个顶点走到b的距离之和，而a和b之间的某个顶点c必然位于a所在的边或者b所在的边上，其距离a或者b的距离显然小于a到b的距离。

3、这两点位于相对的边上：

这种情况下比较麻烦。由于水平和竖直的方向对称，在这里不妨设这a和b分别位于上边和下边，那么二者的距离相当于竖直距离side，再加上这两点在水平方向上坐标之差的绝对值。

接下来，若二者之间的某个点c位于上边或者下边，那么这个c距离a或b的距离必然小于等于side，显然是更小的，因此只需要考虑中间点位于左边或者右边的情况。

由于a和b不相邻，因此左边至少存在一个点c，右边上至少存在一个点d，如果原题设成立，那么这里就需要证明a到b的距离小于a到c、a到d、b到c、b到d中的最小距离。在极限情况下，这四段距离之和恰好为整个正方形的周长，也就是side \* 4，因此这四个距离中的最小距离必然小于等于side，同样也小于等于a和b的距离。实际上，可以想象a、b、c、d这四个点分别为正方形上边、下边、左边、右边的中点，只有在这种情况下a到b的距离才刚刚好等于a到c、a到d、b到c、b到d的距离。

根据以上的结论，就可以将这些点从正方形左下角开始，按顺时针顺序拉直成一直线，问题就变成了给出一个循环的下标数组，需要从中选出k个点，使得任意两个点之间的距离的最小值最大。

具体的拉直方案为：

1、对于位于左边的点(0, y)，其在直线上的下标为y

2、对于位于上边的点(x, side)，其在直线上的下标为side + x，即先通过完整的左边长度为side，再往右走x

3、对于位于右边的点(side, y)，其在直线上的下标为side \* 2 + side - y，即先通过完整的左边和上边，长度之和为side \* 2，再从右上角开始向下走到y，行走的距离为side - y

4、对于位于下边的点(x, 0)，其在直线上的下标为side \* 3 + side - x，即先通过完整的左边、上边和右边，长度之和为side \* 3，再从右下角开始向左走到x，行走的距离为side - x

转化完成后，对于这类最小值最大的问题，依然是使用二分法来进行处理。对于当前二分到的mid，现在的问题变成了如何检测能否在直线上找出k个点，使得相邻点之间的距离，包括第一个点和最后一个点之间的距离都大于等于mid，而对于这个问题可以使用动态规划来进行处理。令f[index]表示以直线上第index个点结尾时可以选取的最多点数，初始情况下f[0] \= 1，表示选择直线上最左侧的点。接下来对于index > 0的情况，由于f是单调不减的，因此对于f[index]，就应该选择最靠后的点pre，pre在这里需要满足index到pre的距离大于等于mid。此时就有f[index] \= f[pre] + 1，若不存在这样的pre，那么f[index] \= 1。另外，为了方便对比第一个点和最后一个点之间的距离，在这里还需要额外使用一个数组start记录以index为结尾时对应的第一个点是哪个，那么当f[index]通过f[pre]更新时，就有start[index] \= start[pre]，否则start[index]就是index自身。

当某一时刻f[index]大于等于k，且index与start[index]之间的距离大于等于mid，那么就说明可以找到最小距离大于等于mid的一组点，此时应该调整二分的下界为mid。若找不到，则应该调整二分的上界为mid - 1。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, side, points, k):
        """
        :type side: int
        :type points: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        dis = []
        for x, y in points:
            if x == 0:
                dis.append(y)
            elif y == side:
                dis.append(side + x)
            elif x == side:
                dis.append(side * 2 + side - y)
            else:
                dis.append(side * 3 + side - x)
        
        dis.sort()

        left = 1
        right = side
        while left < right:
            mid = (left + right + 1) // 2
            f = [1]
            start = [0]
            pre = 0
            flag = False
            for index in range(1, len(points)):
                while dis[index] - dis[pre] >= mid:
                    pre += 1
                
                if pre > 0:
                    f.append(f[pre - 1] + 1)
                    start.append(start[pre - 1])
                    if f[-1] >= k and side * 4 - dis[index] + dis[start[index]] >= mid:
                        flag = True
                        break
                else:
                    f.append(1)
                    start.append(index)

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
```
