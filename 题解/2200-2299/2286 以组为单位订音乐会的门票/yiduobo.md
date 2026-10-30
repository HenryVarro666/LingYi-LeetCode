---
title: "2286. 以组为单位订音乐会的门票"
aliases: ["yiduobo的每日leetcode 2286.以组为单位订音乐会的门票"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/binary-search", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/552057499"
zhihu_id: "552057499"
zhihu_title: "yiduobo的每日leetcode 2286.以组为单位订音乐会的门票"
question_id: "2286"
question: "以组为单位订音乐会的门票"
problem_url: "https://leetcode.cn/problems/booking-concert-tickets-in-groups/"
difficulty: "Hard"
rating: 2470
created: "2022-08-10T13:36:37+08:00"
updated: "2022-08-10T13:36:37+08:00"
upvotes: 0
comments: 0
---

# 2286. 以组为单位订音乐会的门票

> **[yiduobo的每日leetcode 2286.以组为单位订音乐会的门票](https://zhuanlan.zhihu.com/p/552057499) · 知乎 · 2022-08-10 · 赞同 0**
> 力扣：[2286. 以组为单位订音乐会的门票](https://leetcode.cn/problems/booking-concert-tickets-in-groups/) · Hard · 灵茶山艾府：[线段树二分（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2286.以组为单位订音乐会的门票

[力扣](https://leetcode.cn/problems/booking-concert-tickets-in-groups/)

由于题目中的座位安排总是从左到右进行安排的，因此实际上并不需要关心每个座位的安排情况，而是使用每一行剩余的座位来表示每一行的状态。

这样一来，问题就变成了给出一个数组rest，表示每一行剩下的座位，然后需要实现下面两个操作：

1、找出最小的p，满足0 \<\= p \<\= maxRow，且rest[p] >\= k。若存在合法的p，那么将rest[p]减去k。这里的减法操作表示将这k个人连续地安排在第p行，因此第p行剩余的座位数应该减去k。

2、找出最小的p，满足0 \<\= p \<\= maxRow，且rest[0] + rest[1] + ... + rest[p] >\= k。若存在合法的p，那么将rest[p]减去(k - rest[0] - rest[1] - ... - rest[p - 1])，表示将这k个人先安排在第0到第p - 1行剩余的座位上，此时会将这些行剩余的座位全部消耗完，而剩余没有安排的人则安排在第p行的座位中。

可以发现，在这里使用线段树是很合适的。在建树时除了常规的树结构之外，还额外维护两个值max_v和sum_v，分别表示当前子树管辖的区间中的数组最大值以及数组总和。接下来对于上面的两种操作：

1、可以先转化成找出数组中最小的满足rest[p] >\= k的下标p，然后判断p是否小于等于maxRow。寻找p则可以通过从树的根节点开始递归向下求解。

对于当前节点now，若now.max_v \< k，那么说明当前子树对应的数组区间中没有数大于等于k，因此无法进行安排，此时直接返回空数组就行了。否则说明数组中必然存在某个数大于等于k，接下来的任务就是找出最小的p的位置。

在这里可以考虑now.left.max_v与k的大小。若now.left.max_v >\= k，说明now.left管辖区间中存在某个数大于等于k，此时就应该递归求解now.left，否则就递归求解now.right。若某一时刻递归到了某个叶子节点，那么这个节点对应的数组下标就是要找的p。

找到p之后，首先判断p是否小于等于maxRow。若p大于maxRow，那么直接返回空数组就行了，否则还需要将p对应节点的max_v和sum_v都将去k，并更新所有包含这个数的树中节点的max_v和sum_v。

2、在这里可以运用上面同样的方法递归找到p，不过在这里使用的是节点的sum_v而不是max_v。若找不到p或者p > maxRow，则同样是返回空数组，否则就先将区间0到p - 1的max_v和sum_v都置为0，并在过程中记录区间0到p - 1原来的sum_v之和，记为cnt。最后再将p对应的节点的max_v和sum_v减去cnt，并更新所有包含这个数的树中节点的max_v和sum_v。

关于上面的操作，单点查询，单点修改都是线段树的常规操作。而操作2中的区间操作也是一次性的，因为当某个区间的max_v和sum_v被置为0之后，在后续的操作中并不会再修改这个区间的值。

最后附上python代码：

```python
class BookMyShow(object):

    def __init__(self, n, m):
        """
        :type n: int
        :type m: int
        """
        self.n = n
        self.m = m
        self.left = [-1] * (4 * n)
        self.right = [-1] * (4 * n)
        self.max_v = [-1] * (4 * n)
        self.sum_v = [-1] * (4 * n)
        self.build(0, 0, n - 1, m)

    def build(self, now, l, r, v):
        if l == r:
            self.max_v[now] = self.sum_v[now] = v
        else:
            mid = (l + r) >> 1
            self.left[now] = now + now + 1
            self.right[now] = now + now + 2
            self.build(self.left[now], l, mid, v)
            self.build(self.right[now], mid + 1, r, v)
            self.max_v[now] = max(self.max_v[self.left[now]], self.max_v[self.right[now]])
            self.sum_v[now] = self.sum_v[self.left[now]] + self.sum_v[self.right[now]]

    def find_max(self, now, l, r, v):
        if self.max_v[now] < v:
            return -1, -1
        if l == r:
            return l, now
        else:
            mid = (l + r) >> 1
            if self.max_v[self.left[now]] >= v:
                return self.find_max(self.left[now], l, mid, v)
            else:
                return self.find_max(self.right[now], mid +1, r, v)

    def update_single(self, now, l, r, p, v):
        if l == r:
            self.max_v[now] -= v
            self.sum_v[now] -= v
        else:
            mid = (l + r) >> 1
            if p <= mid:
                self.update_single(self.left[now], l, mid, p, v)
            else:
                self.update_single(self.right[now], mid + 1, r, p, v)
            
            self.max_v[now] = max(self.max_v[self.left[now]], self.max_v[self.right[now]])
            self.sum_v[now] = self.sum_v[self.left[now]] + self.sum_v[self.right[now]]

    def gather(self, k, maxRow):
        """
        :type k: int
        :type maxRow: int
        :rtype: List[int]
        """
        p, node = self.find_max(0, 0, self.n - 1, k)
        if p == -1 or p > maxRow:
            return []
        
        res = [p, self.m - self.max_v[node]]

        self.update_single(0, 0, self.n - 1, p, k)

        return res

    def find_sum(self, now, l, r, v):
        if self.sum_v[now] < v:
            return -1
        if l == r:
            return l
        else:
            mid = (l + r) >> 1
            if self.sum_v[self.left[now]] >= v:
                return self.find_sum(self.left[now], l, mid, v)
            else:
                return self.find_sum(self.right[now], mid + 1, r, v - self.sum_v[self.left[now]])

    def set_seg_zero(self, now, l, r, p):
        if l == r:
            cnt = self.max_v[now]
            self.max_v[now] = self.sum_v[now] = 0
        else:
            mid = (l + r) >> 1
            if p <= mid:
                cnt = self.set_seg_zero(self.left[now], l, mid, p)
            else:
                cnt = self.sum_v[self.left[now]]
                self.max_v[self.left[now]] = self.sum_v[self.left[now]] = 0
                
                cnt += self.set_seg_zero(self.right[now], mid + 1, r, p)
            
            self.max_v[now] = max(self.max_v[self.left[now]], self.max_v[self.right[now]])
            self.sum_v[now] = self.sum_v[self.left[now]] + self.sum_v[self.right[now]]
        
        return cnt

    def scatter(self, k, maxRow):
        """
        :type k: int
        :type maxRow: int
        :rtype: bool
        """
        p = self.find_sum(0, 0, self.n - 1, k)
        if p == -1 or p > maxRow:
            return False
        
        cnt = self.set_seg_zero(0, 0, self.n - 1, p - 1)
        self.update_single(0, 0, self.n - 1, p, k - cnt)

        return True

# Your BookMyShow object will be instantiated and called as such:
# obj = BookMyShow(n, m)
# param_1 = obj.gather(k,maxRow)
# param_2 = obj.scatter(k,maxRow)
```
