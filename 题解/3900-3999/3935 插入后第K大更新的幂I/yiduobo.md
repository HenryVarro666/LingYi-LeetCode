---
title: "3930. 插入后第K大更新的幂II & 3935. 插入后第K大更新的幂I"
aliases: ["yiduobo的每日leetcode 3930.插入后第K大更新的幂II && 3935.插入后第K大更新的幂I", "3930. 插入后第K大更新的幂II", "3935. 插入后第K大更新的幂I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2042030950817723569"
zhihu_id: "2042030950817723569"
zhihu_title: "yiduobo的每日leetcode 3930.插入后第K大更新的幂II && 3935.插入后第K大更新的幂I"
question_id: ["3930", "3935"]
question: ["插入后第K大更新的幂II", "插入后第K大更新的幂I"]
problem_url: ["https://leetcode.cn/problems/power-update-after-k-th-largest-insertion-ii/", "https://leetcode.cn/problems/power-update-after-k-th-largest-insertion-i/"]
created: "2026-05-25T00:06:03+08:00"
updated: "2026-05-25T00:06:04+08:00"
upvotes: 1
comments: 0
---

# 3930. 插入后第K大更新的幂II & 3935. 插入后第K大更新的幂I

> **[yiduobo的每日leetcode 3930.插入后第K大更新的幂II && 3935.插入后第K大更新的幂I](https://zhuanlan.zhihu.com/p/2042030950817723569) · 知乎 · 2026-05-25 · 赞同 1**
> 力扣：[3930. 插入后第K大更新的幂II](https://leetcode.cn/problems/power-update-after-k-th-largest-insertion-ii/)
> 力扣：[3935. 插入后第K大更新的幂I](https://leetcode.cn/problems/power-update-after-k-th-largest-insertion-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3930.插入后第K大更新的幂II

<https://leetcode.cn/problems/power-update-after-k-th-largest-insertion-ii/description/>

3935.插入后第K大更新的幂I

<https://leetcode.cn/problems/power-update-after-k-th-largest-insertion-i/description/>

题目给出一个整数数组nums以及一个整数p。

另外给出一个二维整数数组queries，其中queries\[index\] \= \[val\[index\], k\[index\]\]。

对于每次查询：

- 将val[index]加入到nums中
- 令x为当前nums中第k[index]大的元素
- 将p更新为p^x % (10^9 + 7)

要求返回数组ans，其中ans[index]表示在第index查询后p的值。

两题的题设大致相同，3935题作为弱化的版本，其还具有一个条件是两次查询的k之差不超过10。另外3930题中所有数值的取值范围可达10^9，3935题则不超过10^6。

本题实际上可以理解成动态区间第k大值的问题，不过本题中只有插入没有删除，因此在这里可以使用离线技巧。

具体来说，先将所有的queires都过一遍，这样一来就可以得到nums中最终将出现哪些元素。

接下来，将这些元素，然后构造一颗高度完美的平衡树。相比于常规的树节点，这里的节点除了数值val以及左右孩子left和right之外，还需要额外维护一个weight，用来帮助后续查找树中第k大值。在一开始，所有节点的weight都为0。

接下来对于每一组询问，先从根节点开始向下逐步移动，找到当前的val对应的节点，并将路径上所有节点的weight都加上1。然后对于当前的k，先将第k大，改为查询第tot - k + 1小，然后从根节点向下，按照常规平衡树查询第k小的处理方法找到对应的节点，然后使用快速幂更新p的值即可。

最后附上python代码：

```python
class Node():
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.size = 0
        self.left = None
        self.right = None

class BST():
    def build(self, nums, start, end):
        mid = (start + end) // 2
        node = Node(nums[mid], None, None)
        if start < mid:
            node.left = self.build(nums, start, mid - 1)
        if mid < end:
            node.right = self.build(nums, mid + 1, end)
        return node

    def __init__(self, nums):
        self.root = self.build(nums, 0, len(nums) - 1)

    def update(self, v):
        curr = self.root
        curr.size += 1
        while curr.val != v:
            if v < curr.val:
                curr = curr.left
            else:
                curr = curr.right
            curr.size += 1
    
    def kth(self, k):
        curr = self.root
        while True:
            if curr.left and curr.left.size >= k:
                curr = curr.left
            elif curr.right and curr.size - curr.right.size < k:
                k -= curr.size - curr.right.size
                curr = curr.right
            else:
                return curr.val

class Solution(object):
    def powerUpdate(self, nums, p, queries):
        """
        :type nums: List[int]
        :type p: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        all_nums = sorted(list(set(nums + [v for v, _ in queries])))
        bst = BST(all_nums)
        for v in nums:
            bst.update(v)
        
        mod = 10 ** 9 + 7
        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p & 1:
                res = res * base % mod
            return res

        res = []
        tot = len(nums)
        for v, k in queries:
            bst.update(v)
            tot += 1
            x = bst.kth(tot - k + 1)
            p = quick_pow(p, x)
            res.append(p)
        
        return res
```
