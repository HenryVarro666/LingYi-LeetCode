---
title: "3656. 判断是否存在简单图"
aliases: ["yiduobo的每日leetcode 3656.判断是否存在简单图"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1949238872174232630"
zhihu_id: "1949238872174232630"
zhihu_title: "yiduobo的每日leetcode 3656.判断是否存在简单图"
question_id: "3656"
question: "判断是否存在简单图"
problem_url: "https://leetcode.cn/problems/determine-if-a-simple-graph-exists/"
created: "2025-09-13T14:31:48+08:00"
updated: "2025-09-13T14:31:50+08:00"
upvotes: 0
comments: 0
---

# 3656. 判断是否存在简单图

> **[yiduobo的每日leetcode 3656.判断是否存在简单图](https://zhuanlan.zhihu.com/p/1949238872174232630) · 知乎 · 2025-09-13 · 赞同 0**
> 力扣：[3656. 判断是否存在简单图](https://leetcode.cn/problems/determine-if-a-simple-graph-exists/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3656.判断是否存在简单图

[3656. 判断是否存在简单图 - 力扣（LeetCode）](https://leetcode.cn/problems/determine-if-a-simple-graph-exists/description/)

题目给出一个整数数组degrees，其中degrees[index]表示第index个顶点的期望度数。

现在要求判断是否存在一个恰好具有这些顶点度数的无向简单图。简单图指的是没有自环和重边的图。

题目保证所有的degrees[index]在0到n - 1之间，其中n为degrees的长度，也就是图中的节点数。

首先，题目保证了degrees中的所有元素都小于n，因此不会出现为了避免重边而无法连边的情况。也就是说，在这里只需要考虑各个节点的度数是否足够就行了。

另外，由于每条边将产生两个度，因此度的总和必然为偶数，在这里可以先检测degress的总和是否为偶数，若不是，则可以直接返回false。

接下来，则需要考虑如何分配这些边。由于度越大的节点需要连接的边越多，因此这些边就应该优先分配给度同样比较大的节点，那么一个自然的想法就是将所有节点中度最大的节点取出来，然后将这些边分配给剩下节点中度最大的若干个，若无法分配，则返回false，否则将这些节点的度减一，然后继续从剩下的节点中取出度最大的并修正度数，直到处理完所有节点为止。

不过本题中的数据规模不小，直接模拟显然是不行。可以发现，只需要好好调整分配的具体节点，就可以保证取节点是按照所有节点原始的度从大到小进行的。更具体的说，就是将所有节点按照度从大到小进行排序，然后在每次分配时，分配到的节点一定是由一段度单调不增的节点，再加上最后一段度相同的节点。例如[4, 3, 2, 2, 2, 2, 1]，在分配第一个4时，将分配到[3]和[2, 2, 2, 2]，此时就应该优先将边分配给单调不增的这一段中的所有节点，然后将剩下的边，按从后向前的顺序分配到度相同的节点中，这样一来，剩下的度就变成了[2, 2, 1, 1, 1, 1]，依然保持单调不增。

基于上面的结论，问题就可以转化为计算剩下节点可用的度是否足够，而不需要考虑具体的分配方式。不妨设当前分配的是度第k大的节点，那么此前分配过的所有节点，加上当前节点的度数之和就是degrees[0] + degrees[1] + ... + degress[k - 1]，也就是到目前为止需要分配出去这么多度数。接下来，如果这k个节点内部两两连边，可以产生的度数为k \* (k - 1)，而对于剩下的节点，若这些节点的度数小于k，则全都要，否则最多取k个度用来连边，将这三部分的值累加起来就是可能产生的最大度数。若这个值小于需要的度数，则返回false，否则继续考虑下一个节点，直到全部考察完毕为止。

最后附上python代码：

```python
class Solution(object):
    def simpleGraphExists(self, degrees):
        """
        :type degrees: List[int]
        :rtype: bool
        """
        
        if sum(degrees) % 2 == 1:
            return False

        degrees.sort(reverse=True)
        s = [0]
        for v in degrees:
            s.append(s[-1] + v)
        
        need = 0
        p = len(degrees)
        for k in range(1, len(degrees) + 1):
            need += degrees[k - 1]
            inner = k * (k - 1)
            while p > k and degrees[p - 1] < k:
                p -= 1
            
            outer = (p - k) * k + s[-1] - s[p]
            if inner + outer < need:
                return False

        return True
```
