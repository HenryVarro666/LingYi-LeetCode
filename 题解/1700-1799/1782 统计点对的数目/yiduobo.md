---
title: "1782. 统计点对的数目"
aliases: ["yiduobo的每日leetcode 1782.统计点对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/图论算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/462847493"
zhihu_id: "462847493"
zhihu_title: "yiduobo的每日leetcode 1782.统计点对的数目"
question_id: "1782"
question: "统计点对的数目"
problem_url: "https://leetcode.cn/problems/count-pairs-of-nodes/"
difficulty: "Hard"
rating: 2457
created: "2022-01-28T23:30:23+08:00"
updated: "2022-01-28T23:30:23+08:00"
upvotes: 0
comments: 0
---

# 1782. 统计点对的数目

> **[yiduobo的每日leetcode 1782.统计点对的数目](https://zhuanlan.zhihu.com/p/462847493) · 知乎 · 2022-01-28 · 赞同 0**
> 力扣：[1782. 统计点对的数目](https://leetcode.cn/problems/count-pairs-of-nodes/) · Hard · 灵茶山艾府：[击败 100%！从双指针到终极优化，十万个查询都不怕！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1782.统计点对的数目

[力扣](https://leetcode-cn.com/problems/count-pairs-of-nodes/)

对于题目中给出的点对(x, y)，与x或y相连的边数就是d[x] + d[y] - g[x][y]，其中d[x]表示与x相连的边数，而g[x][y]表示x与y之间边的数目。这里减去g[x][y]的原因是这部分边在计算d[x]和d[y]时都被计算了，也就是多计算了一次，因此在这里需要减去g[x][y]。

注意到题目中点的规模非常大，那么直接枚举x和y求解显然是行不通的。相对的，题目中边的数目是相对较小的，而减去g[x][y]中的边必然都是出自于题目中给出的边，那么在这里可以将题目分成两个部分来计算。

首先是抛开去重问题，只考虑求解所有满足d[x] + d[y] > query的点对。对于这个问题，由于题目中一共有n个点，那么可以组成n \* (n - 1) / 2组点对，只需求出其中不满足条件的点对数目，就能反过来求得满足条件的点对数目。

到了这里，题目就转化成了求解所有满足d[x] + d[y] \<\= query的点对数目。在这里可以按照第一题两数之和类似的做法，将d从小到大进行排序后，使用双指针来求解。对于每个左指针l，找到最右侧的满足d[l] + d[r] \<\= query的位置r，那么这里就有(l, l + 1)、(l, l + 2)、……、(l, r)这一共r - l组不符合条件的点对，将其从答案中删去，然后将l向后移动。随着l的向右移动，d[l]是越来越大的，因此r必然是越来越小的，因此每次在移动l之和可以在上一轮r的基础上将r向左移动，这样一来就可以在O(n)的时间复杂度内求出所有满足d[x] + d[y] > query的点对数目了。

接下来再单独考虑去重问题。对于一组(x, y)，根据上面的做法其可以为所有小于d[x] + d[y]的query提供一组答案，即在query在1到d[x] + d[y] - 1之间时，(x, y)将提供一组答案。但是实际上，由于g[x][y]的存在，点对(x, y)时不应该对处于d[x] + d[y] - g[x][y]到d[x] + d[y] - 1之间的query提供合法答案的，也就是说在query位于d[x] + d[y] - g[x][y]到d[x] + d[y] - 1之间时，应该将上面计算出来的答案减去1。

这是一个静态区间加减操作问题，对于这类问题，使用差分数组是比较合适的做法。

到了这里，就可以枚举每条边并对每一组有边相连的(x, y)计算出一个需要执行减一的区间，并将这些区间加入到差分数组当中。由于这里的边数为m，因此差分数组的大小也是m。此时还需要从小到大枚举差分数组，并更新数组的前缀和。这样做的理由是对于一个query而言，需要统计到所有小于等于query的差分区间起点。

接下来就只需要枚举每个query，通过双指针计算出未去重前符合条件的点对数目，然后使用差分数组的前缀数组去掉去重后不符合条件的点对数目。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, n, edges, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type queries: List[int]
        :rtype: List[int]
        """

        g = {}
        d = [0] * n
        for x, y in edges:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[x].get(y, 0) + 1
            g[y][x] = g[y].get(x, 0) + 1
            d[x] += 1
            d[y] += 1
        
        m = len(edges)
        delta = [0] * (m + 1)
        for x in g:
            for y in g[x]:
                if x < y:
                    delta[d[x] + d[y] - g[x][y]] -= 1
                    if d[x] + d[y] <= m:
                        delta[d[x] + d[y]] += 1
        
        f = [delta[0]]
        for index in range(1, m + 1):
            f.append(f[-1] + delta[index])

        d = sorted(d)
        res = []
        for q in queries:
            res.append(n * (n - 1) /2 + f[q])
            l = 0
            r = n - 1
            while l < r:
                if d[l] + d[r] <= q:
                    res[-1] -= r - l
                    l += 1
                else:
                    r -= 1
        
        return res
```
