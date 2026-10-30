---
title: "2817. 限制条件下元素之间的最小绝对差"
aliases: ["yiduobo的每日leetcode 2817.限制条件下元素之间的最小绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/ordered-set"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658602903"
zhihu_id: "658602903"
zhihu_title: "yiduobo的每日leetcode 2817.限制条件下元素之间的最小绝对差"
question_id: "2817"
question: "限制条件下元素之间的最小绝对差"
problem_url: "https://leetcode.cn/problems/minimum-absolute-difference-between-elements-with-constraint/"
difficulty: "Medium"
created: "2023-09-27T00:06:38+08:00"
updated: "2023-09-27T00:06:38+08:00"
upvotes: 0
comments: 0
---

# 2817. 限制条件下元素之间的最小绝对差

> **[yiduobo的每日leetcode 2817.限制条件下元素之间的最小绝对差](https://zhuanlan.zhihu.com/p/658602903) · 知乎 · 2023-09-27 · 赞同 0**
> 力扣：[2817. 限制条件下元素之间的最小绝对差](https://leetcode.cn/problems/minimum-absolute-difference-between-elements-with-constraint/) · Medium · 灵茶山艾府：[平衡树+双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2817.限制条件下元素之间的最小绝对差

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-absolute-difference-between-elements-with-constraint/description/)

题目中的元素对有下标差的要求，如果考虑向前配对，那么每个元素匹配的是nums的一个前缀，同时这个前缀长度是不断变长的。更具体来说就是nums[x]可以与nums[0]配对，nums[x + 1]可以与nums[0]和nums[1]配对，而nums[i]则可以与nums[0]到nums[i - x]这个前缀中的元素配对。于是在这里的基本做法就是从nums[x]开始向后遍历，对于当前遍历到的nums[i]，想将nums[i - x]加入到备选集中，然后从备选集中挑选与nums[x]最接近的数并更新答案。

题目的数据规模很大，同时数值范围也很大，又由于要计算的是数值差，也不存在离散化映射的条件，因此在这里就必须保证已有的元素有序，才能通过分治来高效找出与当前的nums[i]最优的配对元素，也就是说这是一个标准的动态维护有序性以及查找的问题，需要使用平衡二叉树来处理。

python没有原生的平衡二叉树，但是可以使用sorted_list来处理。由于本题只需要处理插入和查找这两种操作，所以我还是选择自己写treap来实现。

最后附上python代码：

```python
import random

class Node(object):

    def __init__(self, v):
        self.v = v
        self.left = self.right = None
        self.fa = None
        self.key = random.randint(0, 2147483647)

class Treap(object):

    def __init__(self):
        self.root = Node(0)
        self.root.key = -1
    
    def insert(self, v):
        fa = None
        now = self.root
        while now:
            fa = now
            if now.v == v:
                return
            elif now.v > v:
                now = now.left
            else:
                now = now.right
        
        node = Node(v)
        if fa.v > v:
            fa.left = node
            node.fa = fa
        else:
            fa.right = node
            node.fa = fa
        
        now = node
        while now.key < now.fa.key:
            fa = now.fa
            grand_fa = fa.fa
            if grand_fa.left == fa:
                grand_fa.left = now
            else:
                grand_fa.right = now
            now.fa = grand_fa

            if now == fa.left:
                fa.left = now.right
                if now.right:
                    now.right.fa = fa
                now.right = fa
                fa.fa = now
            else:
                fa.right = now.left
                if now.left:
                    now.left.fa = fa
                now.left = fa
                fa.fa = now

    def find(self, v):
        now = self.root.right
        mi = abs(now.v - v)
        while now:
            mi = min(mi, abs(now.v - v))
            if mi == 0:
                return 0
            if now.v > v:
                now = now.left
            else:
                now = now.right
        
        return mi
    
    def printTree(self):
        print('----------------')
        q = [self.root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            print now.v
            if now.left:
                print now.v, now.left.v
                q.append(now.left)
                tail += 1
            if now.right:
                print now.v, now.right.v
                q.append(now.right)
                tail += 1
        print('-------------END-------------')

class Solution(object):
    def minAbsoluteDifference(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """

        treap = Treap()
        res = None
        for index, v in enumerate(nums[x:]):
            treap.insert(nums[index])
            t = treap.find(v)
            if res is None or res > t:
                res = t
        
        return res
```
