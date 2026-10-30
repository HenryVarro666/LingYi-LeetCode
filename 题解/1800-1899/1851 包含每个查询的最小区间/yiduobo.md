---
title: "1851. 包含每个查询的最小区间"
aliases: ["yiduobo的每日leetcode 1851.包含每个查询的最小区间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/binary-search", "leetcode/sorting", "leetcode/chi-xian-suan-fa", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/七-并查集", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/471565662"
zhihu_id: "471565662"
zhihu_title: "yiduobo的每日leetcode 1851.包含每个查询的最小区间"
question_id: "1851"
question: "包含每个查询的最小区间"
problem_url: "https://leetcode.cn/problems/minimum-interval-to-include-each-query/"
difficulty: "Hard"
rating: 2286
created: "2022-02-24T00:54:54+08:00"
updated: "2022-02-24T00:54:54+08:00"
upvotes: 0
comments: 0
---

# 1851. 包含每个查询的最小区间

> **[yiduobo的每日leetcode 1851.包含每个查询的最小区间](https://zhuanlan.zhihu.com/p/471565662) · 知乎 · 2022-02-24 · 赞同 0**
> 力扣：[1851. 包含每个查询的最小区间](https://leetcode.cn/problems/minimum-interval-to-include-each-query/) · Hard · 灵茶山艾府：[按区间长度排序+离线询问+并查集](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1851.包含每个查询的最小区间

[力扣](https://leetcode-cn.com/problems/minimum-interval-to-include-each-query/)

题目要求对于每个询问，都找出覆盖这个询问的位置，且长度最短的区间是多长。对于这个问题，朴素的做法自然是遍历每个区间，使用区间的长度更新区间内每一个位置的最小值。不过在这里区间数目众多，跨度也很大，朴素做法时间复杂度必然是不行的。

对于区间操作类问题，王道做法自然是线段树了。不过在这里使用线段树有两个需要注意的地方。第一个是由于区间的长度极大，因此需要先对区间的端点做一个离散化映射，从而确保在空间复杂度上满足使用线段树的条件。第二个是常规线段树都是点更新，区间查询的模式。在这里变成了区间更新，点查询的模式。对于点查询而言是没有任何问题的，但是对于区间更新而言，如果每次更新都直接下发到每个对应的位置，这样时间复杂度甚至高于朴素算法。在这里就需要用到延迟更新这种技巧。

扯了这么多，一想到上面这些乱七八糟的就不想写线段树了。正好前两天做1847题的时候写过treap，那么在这里可以看看能否复用一下。

首先自然还是将问题变为离线问题，先将区间和查询都进行排序。在这里我选择的是对区间的起点以及查询都从小到大进行排序，那么对于当前的查询q[index]而言，设p为满足起点小于等于q[index]的左右区间中最后那一个，那么在这里由于q[index]是单调不减的，因此p同样是单调不减的。这样一来随着index的向后遍历，p也可以跟着向后移动，这样一来就可以在均摊O(1)的时间内选出备选的区间。

接下来对于备选区间而言，所有区间的起点都是满足条件的，那么此时区间还剩下终点以及长度两个信息。因此在treap中除了随机数作为堆的key，还需要加入区间终点right_bound以及区间长度length这两个变量。此时对于q而言，需要查询的就是备选区间中终点大于等于q的区间的最小长度，因此在这里自然是用right_bound作为树的key，而length则是需要查询的信息。

在这里先考虑查询操作。对于当前节点now和询问q：

1、若now.right_bound >\= q，此时now，以及now右子树中所有节点的right_bound都大于等于q，也就是说这些节点对应的区间都包含了q，此时应该从中选出最小的长度来更新答案。在这里逐个节点遍历显然是不行的，那么在这里除了length之外，每个节点还需要额外维护一个min_length，表示以当前节点为根节点的子树中的最小length。这样一来，对于当前这种情况，now以及now右子树中length的最小值就是min(now.length, now.right.min_length)。

当然，除了now以及now的右子树之外，now的左子树中可能还存在部分节点满足right_bound大于等于q，因此此时应该将now更新为now.left，然后继续向下求解。

2、若now.right_bound \< q，此时now，以及now左子树中所有节点的right_bound都小于q，也就是说这些节点对应的区间都不包含q，因此可以直接排除掉。而now的右子树中所有节点的right_bound都大于now.right_bound，依然可能包含q，因此此时需要将now更新为now.right，然后继续向下求解。

接下来是插入操作。在这里新增了right_bound以及length，另外还有上面查询操作需要用到的min_length。由于right_bound是作为树的key，因此在插入时需要根据当前节点的right_bound大小来判断当前新加入的节点应该放在左子树还是右子树。

在这里有一种特殊情况，就是now.right_bound等于插入的right_bound，此时由于区间的起始位置已经不重要了，那么就只需要使用插入的length更新now.length以及now.min_length即可。

对于其他情况而言，则按照常规的插入操作执行即可。不过由于有min_length的存在，因此在从根节点向下迭代的过程中，需要使用加入节点的length来更新迭代路径上每一个节点对应的min_length。

找到插入位置并新建节点后，此时需要根据新建节点的随机值与该节点父亲节点的随机值来进行堆相关的操作。这里的旋转操作大致与普通版本一样，不过需要注意的是每次旋转都将改变当前节点now以及其父亲节点now.fa的树中包含的节点，因此需要在旋转时同步更新now.min_length以及now.fa.min_length。

值得一提的是，上面查询用的是实际上当前节点以及该节点右子树中所有length的最小值，那么在这里为什么还需要维护整颗子树的最小值min_length呢？答案是维护起来比较方便。因为右侧最小值不具有良好的传递性质，例如now的右侧最小值，应该是now.length以及now.right这颗子树中length的最小值，也包含了now.right.left这颗子树中length的最小值。但是反过来，对于now.right而言，其右侧最小值不包含now.right.left中length的最小值，也就是说不能简单通过now.right的右侧最小值来更新得到now的右侧最小值。而为了得到正确的右侧最小值需要向下迭代两层，这在旋转操作中会极大提高处理的复杂程度，新增若干判断。

相对的，如果维护的是min_length，那么now.min_length就可以通过now.left.min_length、now.right.min_length，以及now.length得到，只需向下迭代一层，相对更方便简洁。

最后附上python代码：

```python
class Node(object):
    def __init__(self, right_bound, length, key, fa):
        self.left = self.right = None
        self.right_bound = right_bound
        self.length = length
        self.min_length = length
        self.key = key
        self.fa = fa

class Treap(object):
    def __init__(self):
        self.root = Node(-1, 0, -1, None) #设置假根节点，方便后续的旋转操作
    
    def insert(self, right_bound, length):
        now = self.root
        while True: #从根节点向下迭代，找到right_bound应该放置的位置
            now.min_length = min(now.min_length, length) #更新迭代路径上的min_length
            if right_bound == now.right_bound: #如果终点一样，更新length后可以直接返回
                now.length = min(now.length, length)
                return
            elif right_bound < now.right_bound:
                if now.left is None:
                    node = Node(right_bound, length, random.randint(0, 2147483647), now)
                    now.left = node
                    break
                else:
                    now = now.left
            else:
                if now.right is None:
                    node = Node(right_bound, length, random.randint(0, 2147483647), now)
                    now.right = node
                    break
                else:
                    now = now.right
        
        now = node
        while now.key < now.fa.key: #按照key的大小进行树结构的调整
            grand_fa = now.fa.fa
            if now == now.fa.left: #右旋操作
                #在这里三行fa.min_length相关的语句，分别对应了旋转后fa自身的length,fa右子树的min_length以及fa左子树的min_length
                now.fa.min_length = now.fa.length
                if now.fa.right:
                    now.fa.min_length = min(now.fa.min_length, now.fa.right.min_length)
                if now.right:
                    now.right.fa = now.fa
                    now.fa.min_length = min(now.fa.min_length, now.right.min_length)
                now.fa.left = now.right

                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.right = now.fa
                now.min_length = min(now.min_length, now.fa.min_length)
                now.fa = grand_fa
            else: #左旋操作
                #与上面类似，不过结构是反过来的
                now.fa.min_length = now.fa.length
                if now.fa.left:
                    now.fa.min_length = min(now.fa.min_length, now.fa.left.min_length)
                if now.left:
                    now.left.fa = now.fa
                    now.fa.min_length = min(now.fa.min_length, now.left.min_length)
                now.fa.right = now.left

                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.left = now.fa
                now.min_length = min(now.min_length, now.fa.min_length)
                now.fa = grand_fa
        
    def query(self, q):
        if self.root.right is None:
            return -1
        now = self.root.right
        res = 10000001
        while now:
            if q <= now.right_bound:
                #使用now的length以及now右侧子树的min_length更新答案
                res = min(res, now.length)
                if now.right:
                    res = min(res, now.right.min_length)
                now = now.left
            else:
                now = now.right
        
        if res == 10000001:
            return -1
        
        return res

class Solution(object):
    def minInterval(self, intervals, queries):
        """
        :type intervals: List[List[int]]
        :type queries: List[int]
        :rtype: List[int]
        """

        treap = Treap()
        sorted_intevals = sorted(intervals, key=lambda d:d[0])
        sorted_queries = sorted([[q, index] for index, q in enumerate(queries)], key=lambda d:d[0])
        p = 0
        res = [-1] * len(queries)
        for q, index in sorted_queries:
            while p < len(sorted_intevals) and sorted_intevals[p][0] <= q:
                treap.insert(sorted_intevals[p][1], sorted_intevals[p][1] - sorted_intevals[p][0] + 1)
                p += 1
            
            res[index] = treap.query(q)

        return res
```
