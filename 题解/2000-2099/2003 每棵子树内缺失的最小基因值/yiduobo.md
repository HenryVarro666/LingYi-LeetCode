---
title: "2003. 每棵子树内缺失的最小基因值"
aliases: ["yiduobo的每日leetcode 2003.每棵子树内缺失的最小基因值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/502750805"
zhihu_id: "502750805"
zhihu_title: "yiduobo的每日leetcode 2003.每棵子树内缺失的最小基因值"
question_id: "2003"
question: "每棵子树内缺失的最小基因值"
problem_url: "https://leetcode.cn/problems/smallest-missing-genetic-value-in-each-subtree/"
difficulty: "Hard"
rating: 2415
created: "2022-04-21T22:47:47+08:00"
updated: "2022-04-21T22:47:47+08:00"
upvotes: 0
comments: 0
---

# 2003. 每棵子树内缺失的最小基因值

> **[yiduobo的每日leetcode 2003.每棵子树内缺失的最小基因值](https://zhuanlan.zhihu.com/p/502750805) · 知乎 · 2022-04-21 · 赞同 0**
> 力扣：[2003. 每棵子树内缺失的最小基因值](https://leetcode.cn/problems/smallest-missing-genetic-value-in-each-subtree/) · Hard · 灵茶山艾府：[【图解】一张图秒懂！多种写法！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2003.每棵子树内缺失的最小基因值

[力扣](https://leetcode-cn.com/problems/smallest-missing-genetic-value-in-each-subtree/)

没有想到特别好的常规做法，不过题目中各个节点的基因值都互不相同，那么有一种tricky的做法。

首先考虑特殊情况。如果基因值1没有出现在树中，那么所有节点的答案都是1。

接下来，由于基因值1只出现一次，那么从基因值为1的节点开始向上一路走到树的根节点，路过的这些节点的子树中是有基因值1的，而对于其他的节点而言，以这些节点为根节点的子树中则是不包含基因值1的，也就是说，对于这些节点，对应的答案就必然是1。

有了上面的结论，接下来就只需要考虑子树中含有基因值1的这些节点了。

依然是从基因值为1的节点开始向上一路走到数的根节点，在这个过程中，对于当前处理的节点p，则可以通过bfs找出以p为根节点的子树中有哪些基因值，并使用一个集合num_set将其记录下来。在这里由于是有一个p到parent[p]的行走过程，那么在bfs求解parent[p]时，就无须再将p加入到bfs队列中，而是可以在以p的num_set的基础上，将parent[p]其他子树的基因值添加进来即可。

这个过程看上去是O(n^2)的，但是实际上每个节点只会被遍历到一次，因此这一步的时间复杂度为O(n)。

另一方面，对于p而言，有了其子树中的基因值集合还需要找出其中缺失的最小基因值。那么可以从1开始向上枚举，直到枚举的基因值没有出现在num_set中。由于以parent[p]为根节点的子树中缺失的最小基因值必然大于等于以p为根节点的子树中缺失的最小基因值，因此在求解parent[p]对应的答案时，就可以在p对应答案的基础上往上枚举，而不用再次从1开始枚举。这样一来，枚举答案的复杂度也同样是O(n)的。

综合起来，整体的时间复杂度就是O(n)，虽然是比较tricky的做法，但是效率是非常好的。

最后附上python代码：

```python
class Solution(object):
    def smallestMissingValueSubtree(self, parents, nums):
        """
        :type parents: List[int]
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(parents)
        g = {x : set() for x in range(n)}
        for index, fa in enumerate(parents):
            if fa != -1:
                g[fa].add(index)
        
        res = [1] * n
        p = None
        for index, num in enumerate(nums):
            if num == 1:
                p = index
                break
        
        if p is None:
            return res

        num_set = set()
        num_set.add(1)
        q = [p]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                num_set.add(nums[next])
                q.append(next)
                r += 1
        
        miss = 2
        while miss in num_set:
            miss += 1
        res[p] = miss

        while parents[p] != -1:
            q = [parents[p]]
            num_set.add(nums[parents[p]])
            l = 0
            r = 1
            while l < r:
                now = q[l]
                l += 1
                for next in g[now]:
                    if next == p:
                        continue
                    num_set.add(nums[next])
                    q.append(next)
                    r += 1
            
            while miss in num_set:
                miss += 1

            res[parents[p]] = miss
            p = parents[p]
        
        return res
```
