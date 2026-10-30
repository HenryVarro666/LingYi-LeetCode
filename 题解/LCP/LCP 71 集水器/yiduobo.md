---
title: "LCP 71. 集水器"
aliases: ["yiduobo的每日leetcode LCP71.集水器"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/graph", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/580767135"
zhihu_id: "580767135"
zhihu_title: "yiduobo的每日leetcode LCP71.集水器"
question_id: "LCP 71"
question: "集水器"
problem_url: "https://leetcode.cn/problems/kskhHQ/"
difficulty: "Hard"
created: "2022-11-05T23:09:31+08:00"
updated: "2022-11-05T23:09:31+08:00"
upvotes: 0
comments: 0
---

# LCP 71. 集水器

> **[yiduobo的每日leetcode LCP71.集水器](https://zhuanlan.zhihu.com/p/580767135) · 知乎 · 2022-11-05 · 赞同 0**
> 力扣：[LCP 71. 集水器](https://leetcode.cn/problems/kskhHQ/) · Hard · 灵茶山艾府：[建图技巧 + 并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP71.集水器

[力扣](https://leetcode.cn/problems/kskhHQ/)

LCP系列终于写完了，最后这一题除了触及到盲区的物理知识以外，倒是比想象中要简单得多。

首先，对于被左右斜杠分割的正方形板子求连通块的问题，之前也遇到过一题，做法是将板子按对角线切分成4份，然后根据斜杠的情况使用并查集将这些切分后的部分再合并起来。具体可以参考之前的959题：

[yiduobo：yiduobo的每日leetcode 959.由斜杠划分区域](https://zhuanlan.zhihu.com/p/360526370)

---

在这里假设已经通过上面的算法将各个连通块划分了出来，那么接下来的问题就是判断这些连通块里面哪些部分最后会有水。

首先可以明确的是，一个连通块如果想要有水，那么就必须与shape的边界连通，这样的话水才有机会进到这个连通块里面去。

接下来，与shape的左、右、下三边连通的话，有些水可能会流失掉。具体的流失规则应该更压强有关？（物理知识以及还给老师了）

在这里可以观察题目给出的样例，总结规律。

通过前三个样例可以发现，对于一个块，如果在相同或者更低的水平线上与左右边界或者底边相连，那么这个块就没有办法蓄水，但是样例四立马就推翻了这个结论。可以发现，样例四中容器左侧依然有一部分是可以蓄水的，直观的看，这部分的水如果要被倒出去，那么就必须经过更高的位置，也就是说如果一个块可以仅经过较低的块到达左右边界或者底边，那么这个块就无法蓄水。

于是在这里可以调整一下并查集合并的顺序，可以从最下面开始向上按行进行合并。在合并完一行之后，再重新遍历这一行的所有块，并通过并查集检测这个块是否与左右边界或者底边相连，若不相连，那么这个块就有可能蓄水，那么将其统计起来。

具体实现上，除了常规的并查集父节点的数组，则还需要一个数组和一个哈希表，记录当前块中有多少个可能蓄水的块，以及与边界相连的连通块。

遍历完成后，对于每个连通的块，如果其与四个边界相连，那么就将这个块中统计得到的值累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def reservoir(self, shape):
        """
        :type shape: List[str]
        :rtype: int
        """

        m = len(shape)
        n = len(shape[0])

        fa = range(m * n * 4 + 1)
        linked_water = set()
        cnt = [0] * (m * n * 4 + 1)

        for i in range(m):
            linked_water.add(i * n * 4 + 4)
            linked_water.add((i * n + n - 1) * 4 + 2)
        
        for j in range(n):
            linked_water.add(((m - 1) * n + j) * 4 + 3)
        
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        def union(x, y):
            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                cnt[fa_y] += cnt[fa_x]
                if fa_x in linked_water:
                    linked_water.add(fa_y)

        for i in range(m - 1, -1, -1):
            for j in range(n):
                base = (i * n + j) * 4
                if shape[i][j] == '.':
                    union(base + 1, base + 2)
                    union(base + 1, base + 3)
                    union(base + 1, base + 4)
                elif shape[i][j] == 'r':
                    union(base + 1, base + 4)
                    union(base + 2, base + 3)
                else:
                    union(base + 1, base + 2)
                    union(base + 3, base + 4)

            for j in range(n - 1):
                right = (i * n + j) * 4 + 2
                left = (i * n + j + 1) * 4 + 4
                union(left, right)

            if i != m - 1:
                for j in range(n):
                    bottom = (i * n + j) * 4 + 3
                    top = ((i + 1) * n + j) * 4 + 1
                    union(top, bottom)
            
            for j in range(n):
                base = (i * n + j) * 4
                for offset in range(1, 5):
                    if find(base + offset) not in linked_water:
                        cnt[fa[base + offset]] += 1

        for j in range(n):
            linked_water.add(find(j * 4 + 1))

        res = 0
        for index in range(1, m * n * 4 + 1):
            if find(index) == index and index in linked_water:
                res += cnt[index]
        
        return res / 2
```
