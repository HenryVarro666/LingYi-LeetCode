---
title: "716. 最大栈"
aliases: ["yiduobo的每日leetcode 716.最大栈"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604694303"
zhihu_id: "604694303"
zhihu_title: "yiduobo的每日leetcode 716.最大栈"
question_id: "716"
question: "最大栈"
problem_url: "https://leetcode.cn/problems/max-stack/"
created: "2023-02-09T03:35:48+08:00"
updated: "2023-02-09T03:35:48+08:00"
upvotes: 0
comments: 0
---

# 716. 最大栈

> **[yiduobo的每日leetcode 716.最大栈](https://zhuanlan.zhihu.com/p/604694303) · 知乎 · 2023-02-09 · 赞同 0**
> 力扣：[716. 最大栈](https://leetcode.cn/problems/max-stack/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

716.最大栈

[力扣](https://leetcode.cn/problems/max-stack/)

题目给出一系列的插入和删除操作，其中插入操作的目标点会附带时间和数值这两个属性，而删除则需要删除时间属性最大或者数值属性最大的节点，要求这两种操作的时间复杂度都为O(nlogn)。

由于时间复杂度给出了严格的要求，因此在这里只能使用平衡二叉树来求解。

设置两颗平衡二叉树order和value，接下来，对于插入操作，在order中插入值为（timestamp， x）的节点，在value中插入值为（x, timestamp）的节点，同时在插入操作完成后从根节点出发一直向右侧行走，找出当前树中值最大的节点值ma。

而对于删除操作，如果要删除时间属性最大的节点，那么就通过order.ma拆解出要删除节点的timestamp和x，然后在order和value中找出对应的节点并执行删除。同样的，如果要删除数值属性最大的节点，则通过value.ma拆解出要删除节点的timestamp和x，然后找出对应节点并执行删除。需要注意的是，删除操作可能导致ma的变化，因此在删除节点后同样需要从根节点出发一直向右侧行走，找出当前树中最大的节点值。

在平衡二叉树的具体实现上，我才用的是经典的treap，具体的细节在这就不展开了。

另外提一句，python据我所知到现在都没有原生的平衡二叉数，虽然以及有了sortedList这种好用的三方库。当然也有可能是基于python运行的性能出发，认为python不适合处理这类任务所以就没有添加此类数据结构。

最后附上python代码：

```python
import random

class Node(object):

    def __init__(self, v=(-(10**7) - 1, -1), key=-1, fa=None):
        self.v = v
        self.key = key
        self.fa = fa
        self.left = None
        self.right = None

class Treap(object):

    def __init__(self):
        self.root = Node()
        self.ma = self.root.v

    def leftRotate(self, now):
        fa = now.fa
        fa.right = now.left
        if now.left:
            now.left.fa = fa
        now.left = fa
        
        g_fa = fa.fa
        if fa == g_fa.left:
            g_fa.left = now
        else:
            g_fa.right = now

        now.fa = g_fa
        fa.fa = now
    
    def rightRotate(self, now):
        fa = now.fa
        fa.left = now.right
        if now.right:
            now.right.fa = fa
        now.right = fa
        
        g_fa = fa.fa
        if fa == g_fa.left:
            g_fa.left = now
        else:
            g_fa.right = now

        now.fa = g_fa
        fa.fa = now

    def insert(self, v):
        now = self.root
        while True:
            if v < now.v:
                if now.left:
                    now = now.left
                else:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.left = node
                    now = node
                    break
            else:
                if now.right:
                    now = now.right
                else:
                    node = Node(v, random.randint(0, 2147483647), now)
                    now.right = node
                    now = node
                    break

        while now.fa.key > now.key:
            if now == now.fa.left:
                self.rightRotate(now)
            else:
                self.leftRotate(now)

        self.findMax()

    def delete(self, v):
        now = self.root
        while now.v != v:
            if v < now.v:
                now = now.left
            else:
                now = now.right

        while now.left and now.right:
            if now.left.key < now.right.key:
                self.rightRotate(now.left)
            else:
                self.leftRotate(now.right)

        fa = now.fa
        if now.left:
            if now == fa.left:
                fa.left = now.left
                now.left.fa = fa
            else:
                fa.right = now.left
                now.left.fa = fa

        elif now.right:
            if now == fa.left:
                fa.left = now.right
                now.right.fa = fa
            else:
                fa.right = now.right
                now.right.fa = fa

        else:
            if now == fa.left:
                fa.left = None
            else:
                fa.right = None

        del(now)
        self.findMax()

    def findMax(self):
        now = self.root
        while now.right:
            now = now.right
        self.ma = now.v

class MaxStack(object):

    def __init__(self):
        self.order = Treap()
        self.value = Treap()
        self.index = 0

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        self.order.insert((self.index, x))
        self.value.insert((x, self.index))
        self.index += 1

    def pop(self):
        """
        :rtype: int
        """
        max_index, v = self.order.ma
        self.order.delete((max_index, v))
        self.value.delete((v, max_index))
        return v

    def top(self):
        """
        :rtype: int
        """
        _, v = self.order.ma
        return v

    def peekMax(self):
        """
        :rtype: int
        """
        v, _ = self.value.ma
        return v

    def popMax(self):
        """
        :rtype: int
        """

        max_v, index = self.value.ma
        self.order.delete((index, max_v))
        self.value.delete((max_v, index))
        return max_v

# Your MaxStack object will be instantiated and called as such:
# obj = MaxStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.peekMax()
# param_5 = obj.popMax()
```
