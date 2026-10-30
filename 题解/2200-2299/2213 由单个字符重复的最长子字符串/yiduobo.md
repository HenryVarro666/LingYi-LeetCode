---
title: "2213. 由单个字符重复的最长子字符串"
aliases: ["yiduobo的每日leetcode 2213.由单个字符重复的最长子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/540851980"
zhihu_id: "540851980"
zhihu_title: "yiduobo的每日leetcode 2213.由单个字符重复的最长子字符串"
question_id: "2213"
question: "由单个字符重复的最长子字符串"
problem_url: "https://leetcode.cn/problems/longest-substring-of-one-repeating-character/"
difficulty: "Hard"
rating: 2629
created: "2022-07-12T22:58:08+08:00"
updated: "2022-07-12T23:03:30+08:00"
upvotes: 0
comments: 1
---

# 2213. 由单个字符重复的最长子字符串

> **[yiduobo的每日leetcode 2213.由单个字符重复的最长子字符串](https://zhuanlan.zhihu.com/p/540851980) · 知乎 · 2022-07-12 · 赞同 0**
> 力扣：[2213. 由单个字符重复的最长子字符串](https://leetcode.cn/problems/longest-substring-of-one-repeating-character/) · Hard · 灵茶山艾府：[从分治出发思考，附相似题目（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2213.由单个字符重复的最长子字符串

[力扣](https://leetcode.cn/problems/longest-substring-of-one-repeating-character/)

题目修改单个点位，询问整个区间，所以我直接采用了线段树来进行处理。可能存在字符串相关的更优美的方法，不过我没有继续往下想了。

常规的线段树无法处理本题要求的单个字符重复的最长子串，需要进行特殊处理。

考虑线段树中的区间[l, r]。对于该区间而言，最终答案的分布可能有三种情况：

1、出现在左半边[l, mid]中

2、横跨左右半边

3、出现在右半边[mid + 1， r]中

假设我们现在已经有一种算法可以递归计算出[l, mid]和[mid + 1, r]中单个字符重复的最长子串长度，那么现在只需考虑如何处理情况2。因为当处理了情况2之后，根据递归计算出来的情况1和情况3的结果，就能得到[l, r]对应的答案，也就是得到了完整的递归算法。

对于情况2的横跨左右半边，由于现在是使用的线段树，那么同样也是将这个横跨分成两端，也就是左半边[l, mid]中从右边界开始的单个字符重复的最大子串，以及左半边[mid+ 1, r]中从左边界开始的单个字符重复的最大子串。这两个值也是通过递归计算得到。方便起见，记这两个值分别为rs和ls，那么对于区间[l, r]：

a）首先递归求解左半边区间[l, mid]的ls、rs和右半边区间[mid + 1, r]的ls、rs

b）若[l, mid]的ls等于mid - l + 1，且[l, mid]最右侧的字符恰好等于[mid + 1, r]最左侧的字符，那么[l, r]的ls就是[l, mid]的ls再加上[mid + 1, r]的ls，否则[l, r]的ls就是[l, mid]的ls。

这里简单解释一下。当[l, mid]的ls等于区间长度mid - l + 1时，说明整个左半边区间中都是同一种字符。若这个字符恰好与[mid + 1, r]最左边的的字符，那么说明这个ls延伸到了右半边区间，因此[l, r]的ls等于[l, mid]的ls再加上[mid + 1, r]的ls。

c）与情况2对称，若[mid + 1, r]的rs等于r - mid，且[mid + 1, r]最左侧的字符恰好等于[l, mid]最右侧的字符，那么[l, r]的rs就是[mid + 1, r]的rs再加上[l, mid]的rs，否则[l, r]的rs就是[mid + 1, r]的rs。

在这里又新引入了区间最左侧和最右侧的字符，这个同样是可以递归得到，不过无需什么特殊处理。

到了这里，就得到了[l, mid]的rs以及[mid + 1, r]的ls，那么同样地，若[l, mid]最右侧的字符恰好等于[mid + 1, r]最左侧的字符，那么说明有一个子字符串是横跨两侧的，其长度为[l, mid]的rs加上[mid + 1, r]的ls，也就是情况2对应的结果。

到了这里，就得到了一种算法。总结一下上面各个步骤，得到具体的处理方法 ：

1、首先按常规方法建立线段树。除常规的左右边界l和r、左右孩子left和right之外，还需要记录

1-1）lc和rc，表示区间最左侧和最右侧的字符

1-2）ls和rs，分别表示区间左右两侧单个字符重复的最长字符串长度

1-3）maxs，表示区间中单个字符重复的最长字符串长度

2、对于当前节点now，设其代表的区间为[l, r]。当l \= r时，说明now是一个叶子节点，那么此时lc和rc都等于字符串中l这个位置对应的字符，ls、rs和maxs则都等于1，当l \< r时，设mid \= (l + r) / 2，那么首先递归求解[l, mid]以及[mid + 1, r]。接下来：

2-1）区间[l, r]最左侧的字符就是区间[l, mid]最左侧的字符，因此now.lc \= now.left.lc

区间[l, r]最右侧的字符就是区间[mid + 1, r]最右侧的字符，因此now.rc \= now.right.rc

2-2）先不考虑横跨左右的子字符，那么可以初始化

now.ls \= now.left.ls

now.rs \= now.right.rs

now.maxs \= max(now.left.maxs, now.right.maxs)

2-3）然后再考虑横跨的情况。此时需要满足左半边最右侧的字符等于右半边最左侧的字符，即now.left.rc \= now.right.lc

当now.left.ls \= mid - l + 1，那么就有now.ls +\= now.right.ls

当now.right.rs \= r - mid，那么就有now.rs +\= now.left.rs

另外还有now.maxs \= max(now.maxs, now.left.rs + now.right.ls)

至此，就完成了建树的流程。

对于后续的每个询问，修改对应位置的字符后，需要重新计算受影响节点的各项数值，计算方式与上面的方式完全相同，而每一轮的最终答案就是线段树根节点对应的maxs。

最后附上python代码：

```python
class Node(object):

    def __init__(self, l, r, lc, rc):
        self.l = l
        self.r = r
        self.lc = lc
        self.rc = rc
        self.left = self.right = None
        self.ls = self.rs = 1
        self.maxs = 1

class SegementTree(object):

    def __init__(self, arr):
        self.root = self.build(0, len(arr) - 1, arr)
    
    def build(self, l, r, arr):
        now = Node(l, r, arr[l], arr[r])
        if l < r:
            mid = (l + r) >> 1
            now.left = self.build(l, mid, arr)
            now.right = self.build(mid + 1, r, arr)
            
            now.ls = now.left.ls
            now.rs = now.right.rs
            now.maxs = max(now.left.maxs, now.right.maxs)

            if now.left.rc == now.right.lc:
                if now.ls == mid - l + 1:
                    now.ls += now.right.ls
                if now.rs == r - mid:
                    now.rs += now.left.rs
                now.maxs = max(now.maxs, now.left.rs + now.right.ls)

        return now

    def insert(self, now, p, v):
        if now.l == now.r:
            now.lc = now.rc = v
        else:
            mid = (now.l + now.r) >> 1
            if p <= mid:
                self.insert(now.left, p, v)
            else:
                self.insert(now.right, p, v)
            
            now.lc = now.left.lc
            now.ls = now.left.ls

            now.rc = now.right.rc
            now.rs = now.right.rs

            now.maxs = max(now.left.maxs, now.right.maxs)

            if now.left.rc == now.right.lc:
                if now.ls == mid - now.l + 1:
                    now.ls += now.right.ls
                if now.rs == now.r - mid:
                    now.rs += now.left.rs
                now.maxs = max(now.maxs, now.left.rs + now.right.ls)

    def query(self, p, v):
        self.insert(self.root, p, v)
        return self.root.maxs

class Solution(object):
    def longestRepeating(self, s, queryCharacters, queryIndices):
        """
        :type s: str
        :type queryCharacters: str
        :type queryIndices: List[int]
        :rtype: List[int]
        """

        tree = SegementTree(s)
        res = []
        for index in range(len(queryCharacters)):
            res.append(tree.query(queryIndices[index], queryCharacters[index]))
        
        return res
```
