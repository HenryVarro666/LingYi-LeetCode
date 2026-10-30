---
title: "1691. 堆叠长方体的最大高度"
aliases: ["yiduobo的每日leetcode 1691.堆叠长方体的最大高度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/446978467"
zhihu_id: "446978467"
zhihu_title: "yiduobo的每日leetcode 1691.堆叠长方体的最大高度"
question_id: "1691"
question: "堆叠长方体的最大高度"
problem_url: "https://leetcode.cn/problems/maximum-height-by-stacking-cuboids/"
difficulty: "Hard"
rating: 2172
created: "2021-12-18T15:00:30+08:00"
updated: "2021-12-18T15:00:30+08:00"
upvotes: 0
comments: 0
---

# 1691. 堆叠长方体的最大高度

> **[yiduobo的每日leetcode 1691.堆叠长方体的最大高度](https://zhuanlan.zhihu.com/p/446978467) · 知乎 · 2021-12-18 · 赞同 0**
> 力扣：[1691. 堆叠长方体的最大高度](https://leetcode.cn/problems/maximum-height-by-stacking-cuboids/) · Hard · 灵茶山艾府：[【图解】算法优化+详细证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1691.堆叠长方体的最大高度

[力扣](https://leetcode-cn.com/problems/maximum-height-by-stacking-cuboids/)

三维下的最长子序列，但是这里的三维给了比较强的限制条件。起码我是没见过哪里堆箱子要求上面箱子的高度也小于等于下面箱子的。。

由于题目要求上面箱子的三维都小于等于下面的箱子，因此判断两个箱子能否堆叠的时候只需要按箱子边长度从小到大的顺序一一对比就行了。

证明也很简单。不妨设两个箱子的三边分别为x1, y1, z1以及x2, y2, z2，且这里满足

x1 \<\= y1 \<\= z1

x2 \<\= y2 \<\= z2

此时尝试用下面箱子去覆盖上面箱子，那么就有

1、若z2 \< z1，那么也必然有x2 \< z1、y2 \< z1。也就是说如果下面箱子的长边比上面箱子的长边短，那么下面盒子的短边就更不可能覆盖住上面箱子的长边

2、若z2 >\= z1且y2 \< y1，那么此时对于y1，显然有x2 \<\= y2 \< y1，说明不能用x2去覆盖y1。另外，即使此时满足z2 >\= y1，但是由于x2 \<\= y2 \< y1 \<\= z1，因此如果挪用z2来覆盖y1，那么空出来的z1就无法覆盖了

也就是说如果x1 \<\= x2、y1 \<\= y2、z1 \<\= z2当中有任何一项不成立，那么即使调换x2、y2、z2之间的位置也不可能使得三个不等式同时成立，也就是说，题目这里判断一个箱子能否放在另一个箱子上面，只需要将两个箱子的边从小到大进行排序，然后一一对比即可。

除此之外，还有另一个隐藏条件就是最高高度必然是选择箱子的最长边作为高堆叠出来的。

根据上面的理论，按长度的顺序一一对应是最有可能堆叠起来的，因此若存在某个箱子不是将最长边作为高来进行堆叠时，设其下面的箱子、该箱子自身以及上面的箱子分别为(x1, y1, z1)， (x2, y2, z2)以及(x3, y3, z3)，且这里的x、y、z是按从小到大的顺序排列的，那么此时有两种情况：

1、这个箱子使用最短边x2作为高的，此时就有

x1 \<\= y2 \<\= x3

y1 \<\= z2 \<\= y3

z1 \<\= x2 \<\= z3

首先观察左侧：

由于z1 \<\= x2，那么就有x1 \<\= y1 \<\= z1 \<\= x2 \<\= y2 \<\= z2

此时显然满足x1 \<\= x2且y1 \<\= y2且z1 \<\= z2

而对于右侧：

由于y2 \<\= x3，那么就有x2 \<\= y2 \<\= x3 \<\= y3

即满足x2 \<\= x3且y2 \<\= y3

又由于z2 \<\= y3，那么就有z2 \<\= y3 \<\= z3，即z2 \<\= z3

综合左右两侧就有

x2 \<\= x3且y2 \<\= y3且z2 \<\= z3

因此此时完全可以将该箱子调整成为以z2作为高的状态，这样做的话对于最终结果显然是更优的

2、这个箱子使用中边y2作为高，此时就有

x1 \<\= x2 \<\= x3

y1 \<\= z2 \<\= y3

z1 \<\= y2 \<\= z3

同样先观察左侧：

由于z1 \<\= y2，那么就有y1 \<\= z1 \<\= y2 \<\= z2

此时满足y1 \<\= y2且z1 \<\= z2

再观察右侧：

由于z2 \<\= y3，那么就有y2 \<\= z2 \<\= y3 \<\= z3

此时满足y2 \<\= y3且z2 \<\= z3

再综合最开始的x1 \<\= x2 \<\= x3，那么说明此时同样可以调整该箱子使用z2作为高，这对于答案也是更优的

也就是说，如果存在某个箱子不是以最长边作为高的，那么将其调整为以最长边作为高之后同样满足堆叠的条件。这样一来问题就简化很多了。

将箱子按边的覆盖情况从小到到进行排序，然后执行最长上升子序列即可。这里的状态转移方程为

f[i] \= max(f[i], f[j] + z[i])，这里的i和j满足j \< i且x[j] \<\= x[i]、y[j] \<\= y[i]、z[j] \<\= z[i]

最后附上python代码：

```python
class Solution(object):
    def maxHeight(self, cuboids):
        """
        :type cuboids: List[List[int]]
        :rtype: int
        """

        cuboids = sorted([sorted(cuboid) for cuboid in cuboids], key=lambda d:(d[0], d[1], d[2]))
        n = len(cuboids)
        f = []
        res = 0
        for i in range(n):
            x, y, z = cuboids[i]
            f.append(z)
            for j in range(i):
                if x >= cuboids[j][0] and y >= cuboids[j][1] and z >= cuboids[j][2]:
                    f[-1] = max(f[-1], f[j] + z)
            res = max(f[-1], res)
        
        return res
```
