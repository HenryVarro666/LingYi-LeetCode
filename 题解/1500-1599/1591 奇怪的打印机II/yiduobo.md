---
title: "1591. 奇怪的打印机II"
aliases: ["yiduobo的每日leetcode 1591.奇怪的打印机II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/431860563"
zhihu_id: "431860563"
zhihu_title: "yiduobo的每日leetcode 1591.奇怪的打印机II"
question_id: "1591"
question: "奇怪的打印机II"
problem_url: "https://leetcode.cn/problems/strange-printer-ii/"
created: "2021-11-10T23:28:47+08:00"
updated: "2021-11-10T23:28:47+08:00"
upvotes: 0
comments: 0
---

# 1591. 奇怪的打印机II

> **[yiduobo的每日leetcode 1591.奇怪的打印机II](https://zhuanlan.zhihu.com/p/431860563) · 知乎 · 2021-11-10 · 赞同 0**
> 力扣：[1591. 奇怪的打印机II](https://leetcode.cn/problems/strange-printer-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1591.奇怪的打印机II

[力扣](https://leetcode-cn.com/problems/strange-printer-ii/)

做法跟一维的版本类似，但是由于数字不会重复使用，实际上要简单得多。

同样是先找出一块完全未被覆盖过的数字，将其替换成万用数字。重复此过程直到所有数字都被替换过，或者出现无法替换的情况。由于数字不能重复使用，那么在具体操作时，没有必要执行具体的替换，而是只需要通过每一块数字的范围得到数字之间的先后关系，判断是否可行就好了。

确定数字范围指的是找出某个数字其最左、最右、最上、最下的出现的位置，那么在打印这个数字至少需要覆盖这整块区域，而这块区域内的其他数字就必然是在打印该数字之后才被覆盖上去的，这样一来就得到了一个先后关系，也就是有向图中的一条边。

遍历每个数字，求出所有的先后关系，建图后执行拓扑排序即可。

最后附上python代码：

```python
class Solution(object):
    def isPrintable(self, targetGrid):
        """
        :type targetGrid: List[List[int]]
        :rtype: bool
        """

        m = len(targetGrid)
        n = len(targetGrid[0])

        left = {}
        right = {}
        top = {}
        bottom = {}
        for i in range(m):
            for j in range(n):
                now = targetGrid[i][j]
                if left.get(now, n) > j:
                    left[now] = j
                if right.get(now, -1) < j:
                    right[now] = j
                if top.get(now, m) > i:
                    top[now] = i
                if bottom.get(now, -1) < i:
                    bottom[now] = i
        
        g = {}
        ind = {}
        for color in left:
            ind[color] = 0
            for i in range(top[color], bottom[color] + 1):
                for j in range(left[color], right[color] + 1):
                    if targetGrid[i][j] != color:
                        if targetGrid[i][j] not in g:
                            g[targetGrid[i][j]] = set()
                        g[targetGrid[i][j]].add(color)
        
        for color in g:
            for next in g[color]:
                ind[next] = ind.get(next, 0) + 1

        q = []
        for color in ind:
            if ind[color] == 0:
                q.append(color)
        
        l, r = 0, len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
        
        return len(q) == len(ind)
```
