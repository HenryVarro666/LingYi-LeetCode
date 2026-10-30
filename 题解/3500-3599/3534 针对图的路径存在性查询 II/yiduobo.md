---
title: "3534. 针对图的路径存在性查询II"
aliases: ["yiduobo的每日leetcode 3534.针对图的路径存在性查询II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/two-pointers", "leetcode/dynamic-programming", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1905058857262219480"
zhihu_id: "1905058857262219480"
zhihu_title: "yiduobo的每日leetcode 3534.针对图的路径存在性查询II"
question_id: "3534"
question: "针对图的路径存在性查询 II"
problem_url: "https://leetcode.cn/problems/path-existence-queries-in-a-graph-ii/"
difficulty: "Hard"
rating: 2507
created: "2025-05-15T23:19:38+08:00"
updated: "2025-05-15T23:19:38+08:00"
upvotes: 0
comments: 0
---

# 3534. 针对图的路径存在性查询II

> **[yiduobo的每日leetcode 3534.针对图的路径存在性查询II](https://zhuanlan.zhihu.com/p/1905058857262219480) · 知乎 · 2025-05-15 · 赞同 0**
> 力扣：[3534. 针对图的路径存在性查询 II](https://leetcode.cn/problems/path-existence-queries-in-a-graph-ii/) · Hard · 灵茶山艾府：[排序+双指针+倍增（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3534.针对图的路径存在性查询II

[3534. 针对图的路径存在性查询 II - 力扣（LeetCode）](https://leetcode.cn/problems/path-existence-queries-in-a-graph-ii/description/)

题目给出一个整数n，表示图中的节点数量，这些节点从0到n - 1编号。同时给出一个长度为n的整数数组nums，以及一个整数maxDiff。

对于一组节点对(i, j)，若|nums[i] - nums[j]| \<\= maxDiff，那么这两个节点间存在一条无向边。

另外给出一个二维数组queries，对于其中的每个查询queries\[index\] \= \[u\[index\], v\[index\]\]，需要计算u\[index\]与v\[index\]到之间的最短距离，若不存在，则返回-1。

需要注意，节点间的边是无权的，上面所说的最短距离指的就是u[index]可以通过至少几条边走到v[index]。

之前3532题的加强版，本题中nums不再有序，同时需要处理的查询也不再是连通性查询，而是计算最短距离。

由于nums无序，那么在这里还是应该使其有序，才好判断点之间的连通性。但是需要注意的是，最后询问的是原始数组中的下标，因此需要建立起原始数组下标到排序后数组下标的映射。为了方便描述，在这里记ori_nums为原始的nums，sorted_nums为排序后的nums，那么现在就是需要计算一个数组rank，其中rank[index]表示ori_nums[index]在sorted_nums中的下标。直接计算rank不太方便，可以先计算一个对称的映射数组order，然后通过order来计算rank。其中order[index]表示的就是sorted_nums[index]在ori_nums中的下标。

很凑巧的是，题目的样例1和样例2中，order和rank数组是完全相同的，在这里以样例3来对这两个数组进行说明：

nums \= [3, 6, 1]，也就是说ori_nums \= [3, 6, 1]，排序后则为sorted_nums \= [1, 3, 6]

接下来：

order[0]表示的是sorted_nums[0] \= 1在ori_nums中的下标，也就是2

order[1]表示的是sorted_nums[1] \= 3在ori_nums中的下标，也就是0

order[2]表示的是sorted_nums[2] \= 6在ori_nums中的下标，也就是1

因此order \= [2, 0, 1]

接下来，对order进行一趟遍历，将index赋值给rank\[order\[index\]\]就可以得到rank了，也就是将0赋值给rank\[order\[0\]\]，也就是rank\[2\]，将1赋值给rank\[order\[1\]\]，也就是rank\[0\]，将2赋值给rank\[order\[2\]\]，也就是rank\[1\]，因此得到的rank \= \[1, 2, 0\]。

对于order的计算就相对简单了。首先初始化order \= \[0, 1, 2, ..., n - 1\]，接下来对order进行排序，对于一对(order\[i\], order\[j\])，排序的依据是nums\[order\[i\]\]以及nums\[order\[j\]\]的大小。得到order数组后，对其进行一趟遍历，对于当前遍历到的order\[r\]，将r赋值给rank\[order\[r\]\]就可以得到rank数组了。

得到order和rank之后，就可以按照之前3532题的处理方法，对sorted_nums进行一趟遍历，根据maxDiff进行划分。需要注意划分是在sorted_nums上进行的，在具体实现上可以通过排序获取一个sorted_nums数组，也可以直接通过order数组来进行划分。

接下来对于每组查询(x, y)，可以先通过x \= rank[x]和y \= rank[y]将x和y转化到sorted_nums中的下标。若x和y不属于用一个区间，那么直接返回-1，否则就需要想办法高效计算x和y的最短距离。方便起见，在这里默认x \< y，若x >y，只需交换二者就行了。为了使得x能尽快到达y，从x出发的每一步都应该尽量远的向后走，也就是说从x尽量往后走到p1，然后从p1尽量往后走到p2，以此类推，直到走到某个下标大于等于y的节点。可以发现，这个行走的过程是O(n)的，需要想办法进行优化。

对于这类问题，一种常见的处理方法是使用倍增来折叠路径。令f\[x\]\[p\]表示从x出发，走2^p步可以到的最远节点，初始情况下f\[x\]\[0\]为x走一步可以到达的最远节点。由于已经排好序了，因此可以先预先进行一趟遍历，利用滑动窗口计算出所有的f\[x\]\[0\]。而对于p > 1的f\[x\]\[p\]，则有f\[x\]\[p\] \= f\[f\[x\]\[p - 1\]\]\[p - 1\]，也就是说从x出发走2^p步，相当于从x出发走2^(p - 1)步，走到f\[x\]\[p - 1\]，然后从f\[x\]\[p - 1\]出发，再走剩下的2^(p - 1)步，也就是f\[f\[x\]\[p - 1\]\]\[p - 1\]。

得到f数组后，对于一组查询(x, y)，则可以找到先从大到小遍历，找到最大的满足f[x][p] \< y的p，先花费(1 \<\< p)步从x走到f[x][p]，然后再考察从f[x][p]走到y需要的步数。由于f[x][p] \< y且p最大，因此从f[x][p]走到y所需的步数也必然小于等于(1 \<\< p)，也就是说这里的p在行走过程中是单调递减的。不断重复这个过程直到x走到大于等于y的节点处为止，这个过程中行走的次数取决于p的大小，而p是logn级的，因此每次查询就优化到了O(logn)。

值得一提的是，这个倍增法也常运用在经典的lca问题上，记录的则是从树中每个节点开始向上走2^p步到达的节点是什么。

最后附上python代码：

```python
class Solution(object):
    def pathExistenceQueries(self, n, nums, maxDiff, queries):
        """
        :type n: int
        :type nums: List[int]
        :type maxDiff: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        order = [index for index in range(n)]
        order.sort(key=lambda d:nums[d])
        rank = [None] * n
        for r, index in enumerate(order):
            rank[index] = r

        f = [[] for _ in range(n)]

        def update(start, end):
            p = start
            for index in range(start, end + 1):
                while p <= end and nums[order[p]] - nums[order[index]] <= maxDiff:
                    p += 1
                f[index].append(p - 1)

            while f[start][-1] != end:
                for index in range(start, end + 1):
                    mid = f[index][-1]
                    f[index].append(f[mid][-1])

        p = 0
        while p < n:
            q = p + 1
            while q < n and nums[order[q]] - nums[order[q - 1]] <= maxDiff:
                q += 1
            
            update(p, q - 1)
            p = q
        
        res = []
        for x, y in queries:
            x = rank[x]
            y = rank[y]
            if x > y:
                x, y = y, x

            if f[x][-1] < y:
                res.append(-1)
                continue

            res.append(0)
            p = len(f[x]) - 1
            while x < y:
                while p > 0 and f[x][p] >= y:
                    p -= 1
                res[-1] += (1 << p)
                x = f[x][p]
        
        return res
```
