---
title: "1825. 求出MK平均值"
aliases: ["yiduobo的每日leetcode 1825.求出MK平均值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/466958006"
zhihu_id: "466958006"
zhihu_title: "yiduobo的每日leetcode 1825.求出MK平均值"
question_id: "1825"
question: "求出MK平均值"
problem_url: "https://leetcode.cn/problems/finding-mk-average/"
created: "2022-02-13T19:14:14+08:00"
updated: "2022-02-13T19:14:14+08:00"
upvotes: 0
comments: 0
---

# 1825. 求出MK平均值

> **[yiduobo的每日leetcode 1825.求出MK平均值](https://zhuanlan.zhihu.com/p/466958006) · 知乎 · 2022-02-13 · 赞同 0**
> 力扣：[1825. 求出MK平均值](https://leetcode.cn/problems/finding-mk-average/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1825.求出MK平均值

[力扣](https://leetcode-cn.com/problems/finding-mk-average/)

题目的数据规模比较大，直接使用暴力算法肯定是行不通的，需要使用数据结构来进行优化。

对于最后m个数字，使用一个长度为m循环队列，每次新来数字时插入到队尾，若此时队列中数字个数大于m，那么将队首弹出即可。

题目中涉及到了这个队列中第k大的数max_k以及第k小的数min_k，还需要求出最大的数到max_k以及最小的数到min_k这两部分的和。如果使用额外的数据结构，那么还有插入队尾新来的数，以及删去队首弹出的数这两个操作。对于这类问题，王道做法自然是平衡二叉树。在这里树中节点需要额外维护当前子树中数的个数以及这些数的和。虽然号称是王道做法，但是不到万不得已的时候我是不愿意手写的，应该实在是太麻烦了。

除此之外，这里也可以用四个堆来进行维护。对于最小的k个数使用一个大顶堆来维护，对于最大的k个数则使用一个小顶堆来维护，而对于中间的部分则需要同时维护一个大顶堆和一个小顶堆。当数字发生变化时，根据数字与这些堆顶的大小关系来进行调整。这里只需要用到堆，但是具体的调整细节也是非常复杂的。

注意到这里数字的范围在1到100000之间，所以我才用了一种取巧的做法，使用线段树来维护当前最后m个数。线段树中的每个节点都管辖了一个范围[l, r]，若l \= r，那么该节点是一个叶子节点，否则该节点有两个孩子，分别为[l, mid]以及[mid + 1, r]，这里的mid \= (l + r) / 2。

除此之外，每个节点同样需要保存以给节点为根节点的子树中数字的个数w以及这些数字之后s。

由于题目中的数字最大为100000，那么整棵树根节点的管辖范围就是[1, 100000]。对于题目中的几种操作：

1、插入数字v：

从根节点开始向下，找到v对应的叶子节点。具体寻找过程如下：

不妨设当前处于now这个节点，管辖范围为[l, r]。若l \= r，说明now就是要找的叶子节点，否则令mid \= (l + r) / 2。若v \<\= mid，说明v落在now的左子树中，那么将now迭代为now.left，now.left的管辖范围为[l, mid]，否则说明v落在now的右子树中，将now迭代为now.right，now.right的管辖范围为[mid + 1, r]。

在寻找v对应叶子节点的过程中，以路过的节点为根节点的子树中都新增了数字v，因此需要将这些节点的w加上1，s加上v。

2、删除数字v：

与插入数字类似，同样是从根节点向下找到v对应的叶子节点，并将路过节点的w减去1，s减去v

3、找到最小k个数的和：

同样是从根节点往下找，不过这里需要找的与w有关。具体寻找过程何下，设最终答案为res：

不妨设当前处于now这个节点，管辖范围为[l, r]。若l \= r，说明第k小的叶子节点对应的数值就是l，此时k个l将提供k \* l的和，此时应该返回res + k \* l。否则还需要向下继续迭代。令mid \= (l + r) / 2。

若now左子树left的w小于k，说明第k小的数落在了now的右子树中，而这个数应该是now右子树right的第k - left.w小的数，于是此时将k更新为k - left.w，将res加上left.s，同时将now迭代为now.right。

若now左子树left的w大于等于k，说明第k小的数落在了now的左子树中，其同样也是now左子树left的第k的数，因此无需操作k和res，只需要将now迭代为now.left即可。

4、找到最大k个数的和：

与找到最小k个数的和类似，此时应该是判断now的右子树right中数字的个数与k的大小关系，然后决定如何向下迭代。

5、计算mk平均值：

此时队列中最后m个数的和就是整棵树的根节点root中维护的root.s，需要减去最小的k个数的和以及最大的k个数的和，在这里使用操作3和操作4可以求出来。最后除以m - k \* 2就是mk平均值。

具体实现上，可以使用node节点来构造这棵树，也可以使用数组下标法。

对于一个数组，令下标0表示整棵线段树的根节点，管辖[1, 100000]。对于某个下标index，若其管辖的区间[l, r]满足l \= r，说明其对应的是一个叶子节点，否则令index \* 2 + 1表示index的左孩子，管辖[l, mid]，令index \* 2 + 2表示index的右孩子，管辖[mid + 1, r]。其中mid \= (l + r) / 2。

对于本题，则只需要两个数组w和s，遵照上面下标法的定义进行各种操作即可。

最后附上python代码：

```python
class SegementTree(object):

    def __init__(self, maxn):
        self.maxn = maxn
        self.w = [0] * (maxn * 4)
        self.s = [0] * (maxn * 4)
    
    def insert(self, v):
        now = 0
        l, r = 1, self.maxn
        while l <= r:
            self.w[now] += 1
            self.s[now] += v
            if l == r:
                break
            mid = (l + r) >> 1
            if v <= mid:
                now = now + now + 1
                r = mid
            else:
                now = now + now + 2
                l = mid + 1
    
    def remove(self, v):
        now = 0
        l, r = 1, self.maxn
        while l <= r:
            self.w[now] -= 1
            self.s[now] -= v
            if l == r:
                break
            mid = (l + r) >> 1
            if v <= mid:
                now = now + now + 1
                r = mid
            else:
                now = now + now + 2
                l = mid + 1
        
    def weight(self):
        return self.w[0]
    
    def sum(self):
        return self.s[0]

    def min_k(self, k):
        now = 0
        l, r = 1, self.maxn
        res = 0
        while l <= r:
            if l == r:
                return res + l * k
            mid = (l + r) >> 1
            if self.w[now + now + 1] < k:
                res += self.s[now + now + 1]
                k -= self.w[now + now + 1]
                now = now + now + 2
                l = mid + 1
            else:
                now = now + now + 1
                r = mid

    def max_k(self, k):
        now = 0
        l, r = 1, self.maxn
        res = 0
        while l <= r:
            if l == r:
                return res + r * k
            mid = (l + r) >> 1
            if self.w[now + now + 2] < k:
                res += self.s[now + now + 2]
                k -= self.w[now + now + 2]
                now = now + now + 1
                r = mid
            else:
                now = now + now + 2
                l = mid + 1

class MKAverage(object):

    def __init__(self, m, k):
        """
        :type m: int
        :type k: int
        """
        self.m = m
        self.num_list = [None] * m
        self.p = 0
        self.k = k
        self.tree = SegementTree(100000)

    def addElement(self, num):
        """
        :type num: int
        :rtype: None
        """
        self.tree.insert(num)
        if self.tree.weight() > self.m:
            self.tree.remove(self.num_list[self.p])
        self.num_list[self.p] = num
        self.p = (self.p + 1) % self.m

    def calculateMKAverage(self):
        """
        :rtype: int
        """
        if self.tree.weight() < self.m:
            return -1
        return (self.tree.sum() - self.tree.max_k(self.k) - self.tree.min_k(self.k)) / (self.m - self.k - self.k)

# Your MKAverage object will be instantiated and called as such:
# obj = MKAverage(m, k)
# obj.addElement(num)
# param_2 = obj.calculateMKAverage()
```
