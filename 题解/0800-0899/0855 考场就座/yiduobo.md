---
title: "855. 考场就座"
aliases: ["yiduobo的每日leetcode 855.考场就座"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348909553"
zhihu_id: "348909553"
zhihu_title: "yiduobo的每日leetcode 855.考场就座"
question_id: "855"
question: "考场就座"
problem_url: "https://leetcode.cn/problems/exam-room/"
created: "2021-02-04T21:27:25+08:00"
updated: "2021-02-04T21:27:25+08:00"
upvotes: 1
comments: 0
---

# 855. 考场就座

> **[yiduobo的每日leetcode 855.考场就座](https://zhuanlan.zhihu.com/p/348909553) · 知乎 · 2021-02-04 · 赞同 1**
> 力扣：[855. 考场就座](https://leetcode.cn/problems/exam-room/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

855.考场就座

[力扣](https://leetcode-cn.com/problems/exam-room/)

如果我们将考场中剩余的一段连续作为看作区间的话，那么每新来一个学生，当前能提供最大间隔的区间[l ,r]就将被划分为[l, p]以及[p, r]两段，其中p为新来的学生就座的位置；每离开一个学生，那么以离开的位置p为首尾的两端区间[l, p]以及[p, r]则会被重新合并为区间[l, r]。

于是接下来只需要解决两个问题：

1、如何选出当前能提供最大间隔的区间

2、如何通过离开的p定位到区间[l, p]以及[p, r]

对于问题一，使用堆来维护这些区间是很自然的想法。由于当前座位的编号为0到n - 1，方便期间，我们假设初始区间为[-1, n]。那么对于一个区间[l, r]：

1-1）若l \= -1，那么学生必然坐在0这个位置上，因此该区间能提供的间隔就是r

1-2）若r \= n，那么学生必然坐在n - 1这个位置上，因此该区间能提供的间隔就是n - 1 - l

1-3）其他情况下，学生必然坐在区间的正中间，也就是mid \= (l + r) / 2，因此该区间能提供的间隔就是(r - l) / 2

有了上面这些比较准则，就可以根据区间能提供座位的间隔以及区间的左边界l的大小构造一个堆用来维护这些区间。

此时还需要解决问题2。对于问题2，一个自然的想法就是当一个学生就座之后，我们可以得到其座位p，以及其坐在哪个[l, r]当中。此时则可以使用head和tail这两个dict保存以[p, r]这个区间在堆中编号以及[l, p]这个区间在堆中的编号。当座位p上的同学离开时，我们可以将head[p]以及tail[p]这两个区间从堆当中弹出，同时在弹出时获取到原始的l和r是多少，然后再将[l, r]加入到堆中。

当然，python这里不能直接删去堆中节点，因此需要手动实现。

最后附上python代码：

```python
class ExamRoom(object):

    def __init__(self, N):
        """
        :type N: int
        """
        self.heap = []
        self.N = N
        self.head_dict = {}
        self.tail_dict = {}

    def compare(self, x, y):
        l1, r1 = self.heap[x]
        l2, r2 = self.heap[y]
        if l1 == -1:
            dis1 = r1
        elif r1 == self.N:
            dis1 = self.N - 1 - l1
        else:
            dis1 = (r1 - l1) / 2
        
        if l2 == -1:
            dis2 = r2
        elif r2 == self.N:
            dis2 = self.N - 1 - l2
        else:
            dis2 = (r2 - l2) / 2
        
        if dis1 > dis2 or (dis1 == dis2 and l1 < l2):
            return True

        return False

    def swap(self, x, y):
        l1, r1 = self.heap[x]
        l2, r2 = self.heap[y]

        self.heap[x] = [l2, r2]
        self.heap[y] = [l1, r1]

        self.head_dict[l1] = y
        self.tail_dict[r1] = y
        self.head_dict[l2] = x
        self.tail_dict[r2] = x

    def push(self, left, right):
        self.heap.append([left, right])
        now = len(self.heap) - 1
        self.head_dict[left] = now
        self.tail_dict[right] = now
        while now != 0:
            if self.compare(now, (now - 1) / 2):
                self.swap(now, (now - 1) / 2)
                now = (now - 1) / 2
            else:
                break

    def pop(self, now):
        l, r = self.heap[now]
        self.swap(now, -1)
        self.heap.pop()
        self.head_dict.pop(l)
        self.tail_dict.pop(r)
        while now < len(self.heap):
            flag_l = flag_r = False
            if now + now + 1 < len(self.heap) and self.compare(now + now + 1, now):
                flag_l = True
            if now + now + 2 < len(self.heap) and self.compare(now + now + 2, now):
                flag_r = True
            if flag_l:
                if flag_r:
                    if self.compare(now + now + 1, now + now + 2):
                        self.swap(now, now + now + 1)
                        now = now + now + 1
                    else:
                        self.swap(now, now + now + 2)
                        now = now + now + 2
                else:
                    self.swap(now, now + now + 1)
                    now = now + now + 1
            elif flag_r:
                self.swap(now, now + now + 2)
                now = now + now + 2
            else:
                break

        return l, r

    def seat(self):
        """
        :rtype: int
        """
        if not self.heap:
            self.push(0, self.N)
            self.push(-1, 0)
            return 0
        
        left, right = self.pop(0)
        if left == -1:
            self.push(0, right)
            self.push(-1, 0)
            return 0
        elif right == self.N:
            self.push(left, self.N - 1)
            self.push(self.N - 1, self.N)
            return self.N - 1
        else:
            mid = (left + right) / 2
            self.push(left, mid)
            self.push(mid, right)
            return mid

    def leave(self, p):
        """
        :type p: int
        :rtype: None
        """
        _, right = self.pop(self.head_dict[p])
        left, _ = self.pop(self.tail_dict[p])
        self.push(left, right)

# Your ExamRoom object will be instantiated and called as such:
# obj = ExamRoom(N)
# param_1 = obj.seat()
# obj.leave(p)
```
