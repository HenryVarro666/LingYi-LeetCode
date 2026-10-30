---
title: "3547. 图中边值的最大和"
aliases: ["yiduobo的每日leetcode 3547.图中边值的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907609256506664035"
zhihu_id: "1907609256506664035"
zhihu_title: "yiduobo的每日leetcode 3547.图中边值的最大和"
question_id: "3547"
question: "图中边值的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-edge-values-in-a-graph/"
difficulty: "Hard"
created: "2025-05-22T22:57:59+08:00"
updated: "2025-05-22T22:57:59+08:00"
upvotes: 0
comments: 0
---

# 3547. 图中边值的最大和

> **[yiduobo的每日leetcode 3547.图中边值的最大和](https://zhuanlan.zhihu.com/p/1907609256506664035) · 知乎 · 2025-05-22 · 赞同 0**
> 力扣：[3547. 图中边值的最大和](https://leetcode.cn/problems/maximum-sum-of-edge-values-in-a-graph/) · Hard · 灵茶山艾府：[贪心，O(1) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3547.图中边值的最大和

[3547. 图中边值的最大和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-sum-of-edge-values-in-a-graph/description/)

题目给出一个包含n个节点的无向连通图，节点编号为0到n - 1，每个节点最多与其他两个节点相连。

图中包含m条边，使用一个二维数组edges表示，其中edges\[index\] \= \[a\[index\], b\[index\]\]，表示a\[index\]和b\[index\]之间有一条边。

现在要求将1到n分配给图中的节点，而图中边的权重定义为其两端节点值的乘积。问如何分配才能使得图中边权之和最大。

首先可以明确的是，由于每个节点最多与其他两个节点相连，同时这又是张连通图，那么图的形态要么是一条链，要么是一个环，也就是样例1和样例2中的这两种情况。是链还是环，取决于m是等于n还是等于n - 1。

接下来需要考虑如何分配1到n。为了使得乘积之和最大，就应该让大的元素尽量参与运算。对于环的情况，每种元素都参与两次运算，没有差别，而对于链的情况，则应该让较大的元素处于中间，让较小的元素处于两端。

接下来对于元素的配对，也应该让大的元素强强联合，那么在放置n之后，接下来就应该将n - 1和n - 2分别放置在n的两侧，需要注意对于链的情况，如果链的长度为偶数，则需要将n - 1放置在剩余位置较多的那一侧。再接下来，此时需要配对的最大元素为n - 1，因此需要将n - 3放在n - 1的旁边，然后将n - 4放在n - 2的旁边，将n - 5放在n - 3的旁边，以此类推，直到放置完所有元素。

可以发现，上面的放置方案是固定的，因此可能存在某种通项公式。

不妨先考虑链的情况，因为环的情况可以认为是在1 \* 2的地方划开变为链，计算边权和之后再加上1 \* 2这条边的权重就行了。

首先对于n，有n \* (n - 1) + n \* (n - 2)

接下来对于n - 1这一侧，有(n - 1) \* (n - 3) + (n - 3) \* (n - 5) + ...

而对于n - 2这一侧，则有(n - 2) \* (n - 4) + (n - 4) \* (n - 6) + ...

将n - 1和n - 2中的乘积都用平方差公式来替代，则有

(n - 2)^2 - 1 + (n - 4)^2 - 1 + ...

(n - 3)^2 - 1 + (n - 5)^2 - 1 + ...

不管3 \* 1和4 \* 2具体在哪一侧，最后都将形成2^2 - 1以及3^2 - 1

又由于n \* (n - 2)是(n - 1)^2 - 1，因此这些边权之和就可以写成

2^2 - 1 + 3^2 - 1 + ... + (n - 1)^2 - 1 + n \* (n - 1)

将n \* (n - 1)写成n^2 - 1 - (n - 1)，然后再添加一项1^2 - 1，就得到了

1^2 - 1 + 2^2 - 1 + 3^2 - 1 + ... + n^2 - 1 - (n - 1)

将平方项提取出来，使用平方和公式，再减去其他的n个1以及一个n - 1，就有

n \* (n + 1) \* (n \* 2 + 1) // 6 - n \* 2 + 1

最后，只需根据m是否等于n来确定是否需要将1 \* 2这条边的边权添加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """
        
        res = n * (n + 1) * (n * 2 + 1) // 6 - n * 2 + 1
        if len(edges) == n:
            res += 2
        
        return res
```
