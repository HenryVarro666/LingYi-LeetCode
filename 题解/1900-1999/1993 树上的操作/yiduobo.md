---
title: "1993. 树上的操作"
aliases: ["yiduobo的每日leetcode 1993.树上的操作"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/500177848"
zhihu_id: "500177848"
zhihu_title: "yiduobo的每日leetcode 1993.树上的操作"
question_id: "1993"
question: "树上的操作"
problem_url: "https://leetcode.cn/problems/operations-on-tree/"
created: "2022-04-17T21:56:06+08:00"
updated: "2022-04-17T21:56:07+08:00"
upvotes: 0
comments: 0
---

# 1993. 树上的操作

> **[yiduobo的每日leetcode 1993.树上的操作](https://zhuanlan.zhihu.com/p/500177848) · 知乎 · 2022-04-17 · 赞同 0**
> 力扣：[1993. 树上的操作](https://leetcode.cn/problems/operations-on-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1993.树上的操作

[力扣](https://leetcode-cn.com/problems/operations-on-tree/)

由于题目的数据规模并不大，因此使用O(n^2)的做法完全是可行的，不过在这里也有更好的做法。对于树和父节点相关的问题，一种常见的做法是对树进行dfs，并保留dfs序。由于dfs是按照根节点-孩子节点-回到根节点这种顺序来进行的，也就意味着第一次遇到某个节点，以及遍历完该节点直接的其他节点都是该节点的子孙节点。

以样例来说，树的dfs序为

0->1->3->3(完成)->4->4(完成)->1(完成)->2->5->5(完成)->6->6(完成)->2(完成)->0(完成)

例如以1为根节点的子树，在dfs序中1和1完成之间有3和4，而1和1(完成)在dfs序中对应的位置为1和6，这就说明dfs序中区间[1, 6]描述的是以1为根节点的子树。

类似的，对于以2位根节点的子树，其对应的区间位置就是[7, 12]。

这样做的好处就是题目从一个树中的问题转化成了一个数组上的区间操作问题，从而可以使用各类区间操作的数据结构来优化效率。

题目中的lock和unlock都是常规的单点操作。

对于lock操作，只需先检测num在dfs序中对应位置的值是否为0，若为0，说明可以操作lock，那么此时应该将num对应位置的值赋为user，将num(完成)对应位置的值赋为-user。使用user和-user的目的后面会讲到。

对于unlock操作，与lock相反，需要先检测num在dfs序中对应位置的值是否为user，若为user，说明可以操作lock，那么此时只需将num和num(完成)对应的位置都赋值为0即可。

接下来考虑upgrade操作。对于upgrade所需的三个条件，：

1、num没有上锁。这个可以通过num在dfs序中对应的位置的是否等于0来判断。

2、num至少有一个上锁的子孙节点。num的所有子孙节点对应的就是num以及num(完成)这两个位置之间的区间，至少有一个上锁的子孙节点也就意味着这个区间的数不全为0

3、num没有任何上锁的祖先节点。对于num而言，其所有的祖先节点必然是num在dfs序中位置左侧，且还未完成的节点。而在num左侧，且已完成的节点，其并不是num的祖先节点。这样一来就可以计算0到num在dfs序中对应位置的前一位的区间之和是否等于0就行了。

由于lock操作中对上锁节点会进行正负两次赋值，那么对于所有不是num祖先节点的点而言，即使其dfs序处于num的左侧，其完成位置的dfs也会处于num的左侧，这样一来正负就抵消掉了。

在这里可以发现，1和3可以合并到一起，就变成了计算0到num在dfs序中对应位置的区间之和是否等于0。

到了这里就有了几种操作需求：

1、单点赋值

2、计算区间和

3、检测区间是否全为0

4、将区间赋值为0

综合起来可以发现，线段树是非常适合这个场景的，那么直接在dfs序上套用线段树即可。

另外，需要注意在这里有区间赋值操作，因此需要使用延迟更新的技巧，否则时间复杂度承受不住。

最后附上python代码：

```python
class Node(object):

    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.left = self.right = None
        self.all_zero = True
        self.set_zero = False
        self.v = 0

class LockingTree(object):

    def __init__(self, parent):
        """
        :type parent: List[int]
        """

        n = len(parent)
        g = {x : set() for x in range(n)}
        for index in range(1, n):
            g[parent[index]].add(index)
        

        self.left_order = [0] * n
        self.right_order = [0] * n
        self.order_list = []

        def dfs(now):
            self.left_order[now] = len(self.order_list)
            self.order_list.append(now)
            for next in g[now]:
                dfs(next)

            self.right_order[now] = len(self.order_list)
            self.order_list.append(now)

        dfs(0)
        self.root = Node(0, len(self.order_list) - 1)
        self.build(self.root)

    def build(self, now):
        if now.l == now.r:
            return
        
        mid = (now.l + now.r) >> 1
        now.left = Node(now.l, mid)
        self.build(now.left)
        now.right = Node(mid + 1, now.r)
        self.build(now.right)

    def set_v(self, now, l, r, v):
        if l == now.l and r == now.r:
            if l == r:
                now.v = v
                if v == 0:
                    now.all_zero = True
                else:
                    now.all_zero = False
                now.set_zero = False
            else:
                now.v = 0
                now.all_zero = now.set_zero = True
            return

        if now.set_zero:
            now.set_zero = False
            now.left.set_zero = now.left.all_zero = True
            now.left.v = 0
            now.right.set_zero = now.right.all_zero = True
            now.right.v = 0

        mid = (now.l + now.r) >> 1
        if r <= mid:
            self.set_v(now.left, l, r, v)
        elif l > mid:
            self.set_v(now.right, l, r, v)
        else:
            self.set_v(now.left, l, mid, v)
            self.set_v(now.right, mid + 1, r, v)

        now.v = now.left.v + now.right.v

        if now.left.all_zero and now.right.all_zero:
            now.all_zero = True
        else:
            now.all_zero = False

    def get_v(self, now, l, r):
        if l == now.l and r == now.r:
            return now.v

        if now.set_zero:
            now.set_zero = False
            now.left.set_zero = now.left.all_zero = True
            now.left.v = 0
            now.right.set_zero = now.right.all_zero = True
            now.right.v = 0
            return 0

        mid = (now.l + now.r) >> 1
        if r <= mid:
            return self.get_v(now.left, l, r)
        elif l > mid:
            return self.get_v(now.right, l, r)
        else:
            return self.get_v(now.left, l, mid) + self.get_v(now.right, mid + 1, r)

    def check_zero(self, now, l, r):
        if now.l == now.r:
            if now.v == 0:
                now.all_zero = True
            else:
                now.all_zero = False
            return now.all_zero
        
        if now.set_zero:
            now.set_zero = False
            now.left.set_zero = now.left.all_zero = True
            now.left.v = 0
            now.right.set_zero = now.right.all_zero = True
            now.right.v = 0
            return True
        
        if l == now.l and r == now.r:
            return now.all_zero
        
        mid = (now.l + now.r) >> 1
        if r <= mid:
            return self.check_zero(now.left, l, r)
        elif l > mid:
            return self.check_zero(now.right, l, r)
        else:
            return self.check_zero(now.left, l, mid) and self.check_zero(now.right, mid + 1, r)

    def lock(self, num, user):
        """
        :type num: int
        :type user: int
        :rtype: bool
        """
        if self.get_v(self.root, self.left_order[num], self.left_order[num]) == 0:
            self.set_v(self.root, self.left_order[num], self.left_order[num], user)
            self.set_v(self.root, self.right_order[num], self.right_order[num], -user)
            return True
        else:
            return False

    def unlock(self, num, user):
        """
        :type num: int
        :type user: int
        :rtype: bool
        """
        if self.get_v(self.root, self.left_order[num], self.left_order[num]) == user:
            self.set_v(self.root, self.left_order[num], self.left_order[num], 0)
            self.set_v(self.root, self.right_order[num], self.right_order[num], 0)
            return True
        else:
            return False

    def upgrade(self, num, user):
        """
        :type num: int
        :type user: int
        :rtype: bool
        """
        if self.get_v(self.root, 0, self.left_order[num]) != 0:
            return False
        if self.check_zero(self.root, self.left_order[num], self.right_order[num]):
            return False

        self.set_v(self.root, self.left_order[num] + 1, self.right_order[num] - 1, 0)
        self.set_v(self.root, self.left_order[num], self.left_order[num], user)
        self.set_v(self.root, self.right_order[num], self.right_order[num], -user)
        return True

# Your LockingTree object will be instantiated and called as such:
# obj = LockingTree(parent)
# param_1 = obj.lock(num,user)
# param_2 = obj.unlock(num,user)
# param_3 = obj.upgrade(num,user)
```
