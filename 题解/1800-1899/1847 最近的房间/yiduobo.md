---
title: "1847. 最近的房间"
aliases: ["yiduobo的每日leetcode 1847.最近的房间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/ordered-set", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/470513652"
zhihu_id: "470513652"
zhihu_title: "yiduobo的每日leetcode 1847.最近的房间"
question_id: "1847"
question: "最近的房间"
problem_url: "https://leetcode.cn/problems/closest-room/"
difficulty: "Hard"
rating: 2082
created: "2022-02-22T00:42:03+08:00"
updated: "2022-02-22T00:42:04+08:00"
upvotes: 0
comments: 0
---

# 1847. 最近的房间

> **[yiduobo的每日leetcode 1847.最近的房间](https://zhuanlan.zhihu.com/p/470513652) · 知乎 · 2022-02-22 · 赞同 0**
> 力扣：[1847. 最近的房间](https://leetcode.cn/problems/closest-room/) · Hard · 灵茶山艾府：[离线+有序集合+双指针（Python/Java/C++/Go/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1847.最近的房间

[力扣](https://leetcode-cn.com/problems/closest-room/)

首先，拿到这种在线询问式，但又给出了全部询问的问题，第一反应就是能否通过离线算法来简化问题。

对于本题，题目要求在面积大于等于minSize的所有房间中，与preferred最接近的房间，那么在这里就可以先将所有房间以及询问分别按面积从大到小进行排序。

接下来遍历所有的询问，对于当前询问对应的preferred[index]以及minSize[index]而言，其必然满足minSize[index] >\= minSize[index + 1]。而对于能成为当前询问候选答案的房间而言，必然满足size >\= minSize[index]，因此也必然满足size >\= minSize[index + 1]。换言之，能成为当前房间备选答案的房间，必然也能成为后续任意房间的备选答案。

那么在这里，就可以使用一个指针指向当前面积最小的备选房间，配合着询问的遍历向后移动，动态扩充备选房间。这样一来就可以将选择备选答案的过程优化到均摊O(1)。

接下来的问题就是如何在当前备选房间的id中找到距离preferred[index]最近的。由于在这里备选房间的id是动态变化的，那么在这里就只能祭出对付这类问题的王道做法，平衡二叉树。不过在这里由于只有插入和查询操作，没有删除操作，因此在实现上也简单了许多。

我在这里实现的是treap。treap是一种并不严谨但相对好些的平衡二叉树，其维护树平衡的方式是对树中的每个节点随机生成一个key值，然后根据这个key值的大小，依照堆的性质调整树中节点，这也是这种数据结构叫做treap的原因。由于是随机数构成的堆，因此大致上可以认为treap的高度是logn级别的。

对于插入操作，首先从根节点向下，根据当前插入房间id的大小与当前节点的id大小决定如何向下迭代，直到走到某个叶子节点位置。接下来创建一个新节点，其id为当前房间的id，其key为随机整数。接下来从这个新节点开始，运用堆的更新方式对比当前节点的key与其父亲节点的key的大小，若需要调整，那么根据当前节点是其父亲节点的左孩子还是右孩子选择执行右旋或者左旋操作，直到树中的key满足堆的构造为止。其中，左旋和右旋操作是平衡树中调整结构的经典操作，在这里就不展开了。

对于查询操作，同样是从根节点向下，此时有三种情况：

1、若当前节点的id等于preferred，那么答案就是id

2、若当前节点的id小于preferred，那么应该向当前节点的右孩子迭代，并更新较小那一侧的备选答案

3、若当前节点的id大于preferred，那么应该向当前节点的左孩子迭代，并更新较大那一侧的备选答案

当迭代到某个叶子节点时结束迭代，并根据当前的备选答案确定最终的答案即可。

最后附上python代码：

```python
class Node(object):
    def __init__(self, v, key, fa):
        self.left = self.right = None
        self.v = v
        self.key = key
        self.fa = fa

class Treap(object):
    def __init__(self):
        self.root = Node(-1, -1, None) #设置假根节点，方便后续的旋转操作
    
    def insert(self, v):
        now = self.root
        while True: #从根节点向下迭代，找到v应该放置的位置
            if v < now.v:
                if now.left is None:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.left = node
                    break
                else:
                    now = now.left
            elif v > now.v:
                if now.right is None:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.right = node
                    break
                else:
                    now = now.right
        
        now = node
        while now.key < now.fa.key: #按照key的大小进行树结构的调整
            grand_fa = now.fa.fa
            if now == now.fa.left: #右旋操作
                if now.right:
                    now.right.fa = now.fa
                now.fa.left = now.right
                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.right = now.fa
                now.fa = grand_fa
            else: #左旋操作
                if now.left:
                    now.left.fa = now.fa
                now.fa.right = now.left
                if now.fa == grand_fa.left:
                    grand_fa.left = now
                else:
                    grand_fa.right = now
                now.fa.fa = now
                now.left = now.fa
                now.fa = grand_fa

    def query(self, v):
        if self.root.right is None:
            return -1
        now = self.root.right
        l_max = r_min = None
        while now:
            if now.v == v: #恰好相等时直接返回
                return now.v
            elif now.v < v: #更新左侧备选答案
                l_max = now.v
                now = now.right
            else:
                r_min = now.v #更新右侧备选答案
                now = now.left
        
        if l_max is None:
            return r_min
        elif r_min is None:
            return l_max
        elif v - l_max <= r_min - v:
            return l_max
        else:
            return r_min

class Solution(object):
    def closestRoom(self, rooms, queries):
        """
        :type rooms: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        treap = Treap()
        n = len(rooms)
        sorted_rooms = sorted(rooms, key=lambda d:d[1], reverse=True)
        m = len(queries)
        sorted_queries = sorted([[preferred, minSize, index] for index, [preferred, minSize] in enumerate(queries)], key=lambda d:d[1], reverse=True)
        res = [-1] * m

        p = 0 #p指向当前面积最小的备选房间
        for preferred, minSize, index in sorted_queries:
            while p < n and sorted_rooms[p][1] >= minSize:
                treap.insert(sorted_rooms[p][0])
                p += 1
            
            res[index] = treap.query(preferred)
        
        return res
```
