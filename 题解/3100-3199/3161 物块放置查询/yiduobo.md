---
title: "3161. 物块放置查询"
aliases: ["yiduobo的每日leetcode 3161.物块放置查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/binary-indexed-tree", "leetcode/segment-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704569122"
zhihu_id: "704569122"
zhihu_title: "yiduobo的每日leetcode 3161.物块放置查询"
question_id: "3161"
question: "物块放置查询"
problem_url: "https://leetcode.cn/problems/block-placement-queries/"
difficulty: "Hard"
rating: 2513
created: "2024-06-21T00:19:41+08:00"
updated: "2024-06-21T00:19:41+08:00"
upvotes: 0
comments: 0
---

# 3161. 物块放置查询

> **[yiduobo的每日leetcode 3161.物块放置查询](https://zhuanlan.zhihu.com/p/704569122) · 知乎 · 2024-06-21 · 赞同 0**
> 力扣：[3161. 物块放置查询](https://leetcode.cn/problems/block-placement-queries/) · Hard · 灵茶山艾府：[三种方法：线段树/树状数组/并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3161.物块放置查询

[. - 力扣（LeetCode）](https://leetcode.cn/problems/block-placement-queries/description/)

题目给出一条无限长的数轴，原点在0处，沿x轴正方向延伸。

接下来给出一个二维数组queries，其中包含两种操作。

第一种操作是给出一个x，要求在数轴的x处放置一个障碍物，题目保证不会将障碍物放置在同一个位置。

第二种操作是给出一组[x, sz]，要求判断在数轴[0, x]中是否存在一段没有障碍物的区间可以用来放置长度为sz的物品，在这里只需要进行判断，不需要真的执行放置操作。

题目给出的操作数目可以达到15 \* 10^4，而x和sz的取值范围则可以到5 \* 10^4，使用暴力法显然是不行，需要想办法高效求解。题目中的操作一是用来为难操作二的，那么在这里主要是考虑对于操作二中的询问应该如何高效求解。

对于[0, x]这个区间，其中可能包含若干个终点小于x的区间，以及一个包含x这个点的区间。对于前面的这些区间，若其中最长的区间长度大于等于sz，那么就可以放置；对于后面这个包含x点的区间，若这个区间的起点到x这一段的长度大于等于sz，那么也可以放置。

简单总结一下，就是：

1、需要高效计算前缀中独立区间长度的最大值

2、需要记录数轴上的每个点所属区间的起点

对于需求1，需要动态维护这些区间的序，而对于其中的最大长度则可以利用树状数组来处理。对于需求2,，同样是需要动态维护区间的序，然后通过二分法来查找x处于哪个区间中。

动态维护区间序这个问题并不简单，需要使用平衡二叉树，我在这里使用的是另一种处理方法。

注意到本题中只有设置障碍的操作，没有移除障碍的操作，这也就意味着只有区间分割操作，没有区间合并操作。对于这类问题，一种经典的处理方法就是倒推：先将分割点在整个大区间上标记出来，然后就可以得到最终的区间分割情况。接下来倒序遍历分割操作，对于每个分割操作，将其视为区间合并操作，这样一来就变成了若干个小区间逐渐合并成大区间的问题，而区间合并问题则可以利用并查集高效解决。

具体来说，在合并被x分隔的两个区间，首先可以通过并查集找到x左侧区间的起点left以及x右侧区间的终点right，接下来只需将x右侧区间的起点置为left，x左侧区间的终点置为right即可。在实现上，由于分割点同时属于两个区间，例如样例2的区间[0, 2]以及[2, 7]，2这个位置同时处于两个区间中会出现冲突，那么在这里就可以将分割点两侧的值分别乘以2以及乘以2再加1，默认障碍物放置在右侧区间的起点处，例如上面的[0, 2], [2, 7]可以修改为[0, 4], [5, 14]，这样一来就可以避免冲突了。

而对于前缀中最大区间长度这个问题，则只需在区间合并后使用新区间的长度来更新树状数组即可，老的被合并的区间也无需删去，因为老区间的长度一定小于新区间，不可能再被用来更新答案。

最后附上python代码：

```python
class Solution(object):
    def getResults(self, queries):
        """
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        ma = 100000
        f = [0] * (ma + 1)
        left = []
        right = []

        cut_pos = []
        for q in queries:
            if q[0] == 1:
                cut_pos.append(q[1] * 2 + 1)
        cut_pos.sort()
        

        def update(x, v):
            while x <= ma:
                f[x] = max(f[x], v)
                x += x & -x

        pre = 0
        for p in cut_pos:
            for index in range(pre, p):
                left.append(pre)
                right.append(p - 1)
            update(p - 1, p - pre)
            pre = p
        
        for index in range(pre, ma + 1):
            left.append(pre)
            right.append(ma)
        update(ma, ma - pre + 1)

        def get(x):
            v = 0
            while x:
                v = max(v, f[x])
                x -= x & -x
            return v
        
        def find(g, x):
            if g[x] != x:
                g[x] = find(g, g[x])
            return g[x]

        res = []
        for q in queries[::-1]:
            if q[0] == 1:
                q[1] = q[1] * 2 + 1
                if q[1] > ma:
                    continue
                new_l = find(left, q[1] - 1)
                new_r = find(right, q[1])
                
                left[q[1]] = new_l
                right[q[1] - 1] = new_r

                update(new_r, new_r - new_l + 1)
            
            else:
                q[1] *= 2
                q[2] *= 2
                res.append(get(q[1]) >= q[2] or q[1] - find(left, q[1]) + 1 >= q[2])

        res.reverse()
        return res
```
