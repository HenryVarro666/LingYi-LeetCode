---
title: "3165. 不包含相邻元素的子序列的最大和"
aliases: ["yiduobo的每日leetcode 3165.不包含相邻元素的子序列的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/divide-and-conquer", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704897673"
zhihu_id: "704897673"
zhihu_title: "yiduobo的每日leetcode 3165.不包含相邻元素的子序列的最大和"
question_id: "3165"
question: "不包含相邻元素的子序列的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/"
difficulty: "Hard"
rating: 2697
created: "2024-06-23T01:06:12+08:00"
updated: "2024-06-23T01:06:12+08:00"
upvotes: 1
comments: 0
---

# 3165. 不包含相邻元素的子序列的最大和

> **[yiduobo的每日leetcode 3165.不包含相邻元素的子序列的最大和](https://zhuanlan.zhihu.com/p/704897673) · 知乎 · 2024-06-23 · 赞同 1**
> 力扣：[3165. 不包含相邻元素的子序列的最大和](https://leetcode.cn/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/) · Hard · 灵茶山艾府：[分治思想+线段树（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3165.不包含相邻元素的子序列的最大和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/description/)

题目给出一个整数数组nums以及一个二维数组queries，其中queries\[i\] \= \[pos\[i\], x\[i\]\]。对于每个查询i，要求先将nums\[pos\[i\]\]修改为x\[i\]，接下来计算当前nums数组中不包含相邻元素的子序列的最大和，然后将其累加起来，问最终的累加和是多少。

对于不包含相邻元素的子序列的最大和这个问题，常规做法是动态规划，令f[i]和g[i]分别表示前i个数，且最后一个数用了或者没用的情况下的最大和。每次计算的时间复杂度为O(n)，那么对于本题，如果直接暴力计算，最终的时间复杂度就是O(nq)。

不过本题的数据规模很大，nums和queries的规模都高达5 \* 10^4，用上面的方法显然是行不通的，需要想办法进行优化。

由于询问的次数是无法减少的，因此只能先办法提高查询的速度。注意到本题实际上可以看做是区间中单点修改，然后全局查询最值的问题，那么就可以尝试能否用线段树来解决。

线段树奏效的前提是全局的最值是可分治的，也就是对于一个区间[start, end]，其最值可以通过[start, mid]和[mid + 1, end]的最值来得到。幸运的是，本题需要计算的不包含相邻元素的子序列最大和恰好也可以用分治来处理。

对于区间[start, end]而言，从[start, end]这个层面需要关注的事情就是mid和mid + 1这两个元素只能选择其中一个，而[start, mid]以及[mid + 1, end]中保证子序列的元素不相邻则由子区间自行负责，因此对于[start, end]，其不包含相邻元素的最大和必然属于：

1、[start, mid]中不包含mid这个元素，且不包含相邻元素的子序列最大和，以及[mid + 1, end]中的不包含相邻元素的子序列最大和

2、[start, mid]中不包含相邻元素的子序列最大和，以及[mid + 1, end]中不包含mid + 1这个元素，且不包含相邻元素的子序列最大和

这两种情况之一

为了适配以上两种情况，线段树的每个节点中就还需要额外储存四个值head、tail、both、neither，分别表示当前区间[left，right]中：

1、head：包含nums[start]但是不包含nums[end]，且不包含相邻元素的子序列最大和

2、tail：包含nums[start]但是不包含nums[end]，且不包含相邻元素的子序列最大和

3、both：同时包含nums[start]以及nums[end]，且不包含相邻元素的子序列最大和

4、neither：既不包含nums[start]，也不包含nums[end]，且不包含相邻元素的子序列最大和

接下来对于这四个值，当start\= end时，只有both \= max(0, nums[start])，其他三个子序列都不存在。不过注意到题目中可以选取空的子序列，因此可以认为0是区间各种子序列和的下限，对于不存在的子序列可以直接将其值置为0。当start\< end时，记left为[start, mid]对应的节点，right为[mid + 1, end]对应的节点：

1、head：

由于需要包含nums[start]，因此对于left，其可选的只有left.head或者left.both。

当选择left.head时，right则可以包含nums[mid + 1]，但是right不能包含nums[end]，因此right这一侧只能选择right.head或者right.neither，当然，完全不要right这一侧也可以，即

left.head + max(0, right.head, right.neither)

当选择left.both时，right不能包含nums[mid + 1]，同时也不能包含nums[end]，因此只能选择right.neither，即

left.both + right.neither

综合起来就有

head \= max(0, left.head + max(0, right.head, right.neither), left.both + right.neither)

2、tail：

与情况1对称，由于需要包含nums[end]，因此对于right，其可选的只有right.tail或者right.both。

当选择right.tail时，left则可以包含nums[mid]，但是left不能包含nums[start]，因此left这一侧只能选择left.tail或者left.neither。用样的，left这一侧也可以完全不要，即

right.tail + max(0, left.tail, left.neither)

当选择right.both时，left不能包含nums[mid]，同时也不能包含nums[start]，因此只能选择left.neither，即

right.both + left.neither

综合起来就有

tail \= max(0, right.tail + max(0, left.tail, left.neither), right.both + left.neither)

3、both：

由于需要同时包含nums[start]以及nums[end]，因此对于left，其只能选择left.head或者left.both；对于right则需要选择right.tail和right.both之一。两两配对配对一共是四种选择，但是需要注意的是，left.both和right.both不能同时选择，因为nums[mid]与nums[mid + 1]是相邻的，不能同时选择，因此实际上可用的只有三种组合，再组合上0，即

both \= max(0, left.head + right.tail, left.head + right.both, left.both + right.tail)

4、neither：

由于nums[start]和nums[end]都不能选，因此对于left，其只能选择left.tail或者left.neither；对于right则需要选择right.head和right.neither之一。同样两两配对，但是left.tail和right.head不能同时选择，理由同上，因此也只有三种可用的组合，再组合上0，即

neither \= max(0, left.tail + right.neither, left.neither + right.head, left.neither + right.neither)

根据上面的算法以初始的nums建立线段树，接下来遍历queries，对于queries\[i\] \= \[pos\[i\], x\[i\]\]，只需将线段树中包含pos\[i\]的节点自底向上进行更新即可，当前查询对应的最大值就是根节点的head, tail, both, neither中的最大值。

最后附上python代码：

```python
class Node(object):
    def __init__(self, start, end):
        self.left = self.right = None
        self.start, self.end = start, end
        self.head = 0
        self.tail = 0
        self.both = 0
        self.neither = 0

    def update(self, v=0):
        if self.start == self.end:
            self.both = max(v, 0)
        else:
            self.head = max(0, self.left.head + max(0, self.right.head, self.right.neither), self.left.both + self.right.neither)
            self.tail = max(0, self.right.tail + max(0, self.left.tail, self.left.neither), self.left.neither + self.right.both)
            self.both = max(0, self.left.head + self.right.tail, self.left.both + self.right.tail, self.left.head + self.right.both)
            self.neither = max(0, self.left.tail + self.right.neither, self.left.neither + self.right.head, self.left.neither + self.right.neither)

class Tree(object):
    def __init__(self, nums):
        n = len(nums)
        self.root = self.build(0, n - 1, nums)

    def build(self, start, end, nums):
        if start == end:
            node = Node(start, end)
            node.update(nums[start])
        else:
            node = Node(start, end)
            mid = (start + end) // 2
            node.left = self.build(start, mid, nums)
            node.right = self.build(mid + 1, end, nums)
            node.update()

        return node

    def update(self, index, v):
        node_list = [self.root]
        while node_list[-1].start != node_list[-1].end:
            if index <= node_list[-1].left.end:
                node_list.append(node_list[-1].left)
            else:
                node_list.append(node_list[-1].right)
        
        for node in node_list[::-1]:
            node.update(v)

        return max(self.root.head, self.root.tail, self.root.both, self.root.neither)

class Solution(object):
    def maximumSumSubsequence(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: int
        """

        tree = Tree(nums)
        res = 0
        mod = 10 ** 9 + 7
        for index, v in queries:
            res += tree.update(index, v)
            if res >= mod:
                res -= mod
        
        return res
```
