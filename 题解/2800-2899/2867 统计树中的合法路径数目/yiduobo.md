---
title: "2867. 统计树中的合法路径数目"
aliases: ["yiduobo的每日leetcode 2867.统计树中的合法路径数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/常用数据结构/零-常用枚举技巧", "题单/常用数据结构/七-并查集", "题单/链表-二叉树与回溯/三-一般树", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662114015"
zhihu_id: "662114015"
zhihu_title: "yiduobo的每日leetcode 2867.统计树中的合法路径数目"
question_id: "2867"
question: "统计树中的合法路径数目"
problem_url: "https://leetcode.cn/problems/count-valid-paths-in-a-tree/"
difficulty: "Hard"
rating: 2428
created: "2023-10-19T02:09:05+08:00"
updated: "2023-10-19T02:09:05+08:00"
upvotes: 0
comments: 0
---

# 2867. 统计树中的合法路径数目

> **[yiduobo的每日leetcode 2867.统计树中的合法路径数目](https://zhuanlan.zhihu.com/p/662114015) · 知乎 · 2023-10-19 · 赞同 0**
> 力扣：[2867. 统计树中的合法路径数目](https://leetcode.cn/problems/count-valid-paths-in-a-tree/) · Hard · 灵茶山艾府：[【图解】O(n) 线性做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2867.统计树中的合法路径数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-valid-paths-in-a-tree/description/)

首先，题目设计到了节点值是否为质数的判定，因此在这类可以先通过一次筛法找出1到n中的所有质数方便后续使用。

接下来，题目中的合法路径只有两种形态，分别是：

1、从某个合数出发，经过0个或若干个合数，然后再经过一个质数，再经过0个或若干个合数，最终停在一个合数

2、从某个合数出发，经过0个或若干个合数，最终停在一个质数

如果转换成质数的视角，那么上面两种形态就可以认为是对于一个质数，其存在若干条到达某个合数的路径，且这些路径只经过合数。那么从中任选一条或者两条进行组合，就都将得到一条合法路径。

由于之前以及预处理好了质数，在这里枚举质数是很容易的，但是要找出到到达合数且路径上也是合数的路径则不那么简单。

在这里不妨定义一下合数连通块。

合数连通块指的是树中由若干个合数节点组成的连通分量，其中不能包含质数节点，那么合数连通块就可以通过类似floodfill的方式进行求解。

对于某个合数连通块，如果其与某个质数节点相邻，那么从这个质数节点出发，就可以只经过合数节点到达这个连通块中的所有合数节点。不妨设与质数节点相邻的所有合数连通块中，节点的总数为tot，那么对于一个大小为k的相邻合数连通块，首先存在k条从质数节点出发到达连通块中每个节点的路径，另外从这个连通块出发到达另一个相邻合数连通块中的节点的路径数则为k \* (tot - k)。

于是在这里只需要枚举每个质数节点，将其相邻合数节点所在连通块的大小收集起来并计算得到tot，然后逐个遍历这些大小计算可以形成的合法路径数量就行了。不过需要注意的是，上面的计算方法会对每条合数出发合数结尾的路径计算两次，因此最终需要将这部分的结果除以2。

另外，在这里也可以换一种计算方法。类比于枚举数组中的下标对，既可以两重循环每次都遍历所有下标，计算结果之后除以2，也可以第二重循环仅枚举比第一重循环更小的下标达成去重的效果。对于本题，则可以在遍历质数节点的相邻合数节点时，只计算其与当前已经计算过的合数连通块的大小之和cnt与当前遍历到的连通块大小k的乘积，然后再将k累加到cnt中供后续遍历的连通块使用。为了不漏掉从质数节点出发的路径，在这里可以设置cnt的初始值为1。

最后附上python代码：

```python
class Solution(object):
    def countPaths(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        g = {x : set() for x in range(1, n + 1)}
        for x, y in  edges:
            g[x].add(y)
            g[y].add(x)

        prime = [True] * (n + 1)
        prime[1] = False
        p = 2
        while p * p <= n:
            if prime[p]:
                for x in range(p + p, n + 1, p):
                    prime[x] = False
            p += 1
        
        belong = {}
        part_len = {}
        tot_part = 0
        for x in range(1, n + 1):
            if not prime[x] and x not in belong:
                q = [x]
                belong[x] = tot_part
                part_len[tot_part] = 1
                head, tail = 0, 1
                while head < tail:
                    for x in q[head : tail]:
                        for y in g[x]:
                            if not prime[y] and y not in belong:
                                q.append(y)
                                belong[y] = tot_part
                                part_len[tot_part] += 1
                    
                    head, tail = tail, len(q)
                
                tot_part += 1
        
        res = 0
        for x in range(1, n + 1):
            if prime[x]:
                cnt = 1
                for y in g[x]:
                    if y in belong:
                        res += part_len[belong[y]] * cnt
                        cnt += part_len[belong[y]]
        
        return res
```
