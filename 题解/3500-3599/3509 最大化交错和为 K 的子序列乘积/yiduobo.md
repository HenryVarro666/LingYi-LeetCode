---
title: "3509. 最大化交错和为K的子序列乘积"
aliases: ["yiduobo的每日leetcode 3509.最大化交错和为K的子序列乘积"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "leetcode/math", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902509868914565166"
zhihu_id: "1902509868914565166"
zhihu_title: "yiduobo的每日leetcode 3509.最大化交错和为K的子序列乘积"
question_id: "3509"
question: "最大化交错和为 K 的子序列乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-subsequences-with-an-alternating-sum-equal-to-k/"
difficulty: "Hard"
rating: 2703
created: "2025-05-05T00:14:22+08:00"
updated: "2025-05-05T00:14:22+08:00"
upvotes: 0
comments: 0
---

# 3509. 最大化交错和为K的子序列乘积

> **[yiduobo的每日leetcode 3509.最大化交错和为K的子序列乘积](https://zhuanlan.zhihu.com/p/1902509868914565166) · 知乎 · 2025-05-05 · 赞同 0**
> 力扣：[3509. 最大化交错和为 K 的子序列乘积](https://leetcode.cn/problems/maximum-product-of-subsequences-with-an-alternating-sum-equal-to-k/) · Hard · 灵茶山艾府：[暴力出奇迹：如何分析状态个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3509.最大化交错和为K的子序列乘积

[3509. 最大化交错和为 K 的子序列乘积 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-product-of-subsequences-with-an-alternating-sum-equal-to-k/description/)

题目给出一个整数数组nums以及两个整数k和limit。其中nums的长度不超过150，nums中元素的取值在0到12之间，而k的取值范围在-10^5到10^5之间，limit的取值范围在1到5000之间。

现在要求从nums中找出一个非空的子序列，这个子序列的交错和等于k，且子序列中元素的乘积在不超过limit的前提下最大。交错和指的是从下标0开始的数组中，偶数下标的元素之和减去奇数下标的元素之和。

问这个最大的乘积是多少。如果找不出合法的子序列，则返回-1。

题目乍一看是经典的动态规划问题，但是需要特别注意这个乘积不超过limit但是要求乘积最大的条件，限制了动态规划的发挥。因为常规的动态规划一般保留的是子状态中的最优解，但是在本题中，子状态的最优解与当前元素相乘后可能超出limit，但是如果子状态中不选择最优解，反而可能可以与当前元素相乘后得到一个更优的解。

无法使用动态规划的情况下，只能想办法使用暴力法。注意到nums的长度与元素值取值范围都有限，那么数组的交错和必然在-900到900之间，也就是说k的取值范围看上去比较大，但是k在-900到900之外时答案都必然是-1。另一方面，limit不超过5000，因此毛估最终合法的子序列数量应该不会太多。

于是可以一趟遍历，使用两个哈希表f和g分别记录当前所有交错和在-900到900之间，且元素乘积不超过limit的所有子序列，其中f记录的是长度为奇数的子序列，key为子序列和，value为和为这个key的所有可能子序列的乘积形成的集合；g记录的则是长度为偶数的子序列，key和value的定义与f相同。接下来对于当前遍历到的元素v，f和g都需要相互迭代，在这里需要先分别复制一份f和g，得到nxt_f和nxt_g，接下来使用f更新nxt_g，使用g更新nxt_f：

1、若v自身不超过limit，则可以将v加入到nxt_f[v]中，表示v单独形成一个合法的子序列

2、可以遍历f中所有的子序列和s，对于当前的s，如果将v加入其中，那么会形成一个长度为偶数的子序列，v在交错和中的取值应该是负的，因此新的子序列和nxt_s应该是s - v。若nxt_s在-900到900之间，那么就可以将nxt_s加入到nxt_g中。接下来遍历f[s]中的所有子序列乘积m，若m \* v不超过limit，就将其加入到nxt_g[nxt_s]中。另外需要特别处理v \= 0的情况，这种情况下即使f[s]中不存在任何小于等于limit的子序列乘积，也需要将0加入到nxt_g[nxt_s]中。

3、最后对于g中的子序列和s也如法炮制，对于当前的s，如果将v加入到其中，那么会形成一个长度为奇数的子序列，新的子序列和nxt_s应该是s + v。若nxt_s在-900到900之间，那么就可以将nxt_s加入到nxt_f中。接下来遍历g[s]中所有的子序列乘积m，若m \* v不超过limit，那么就将其加入到nxt_f[nxt_s]中。对于v \= 0的情况，也需要将0加入到nxt_f[nxt_s]中。

完成一轮的计算后，将f和g分别迭代到nxt_f和nxt_g，然后继续下一轮计算即可。

全部计算完成后，f[k]和g[k]中的子序列乘积中的最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, nums, k, limit):
        """
        :type nums: List[int]
        :type k: int
        :type limit: int
        :rtype: int
        """
        
        f = {}
        g = {}

        if k < -900 or k > 900:
            return -1

        for v in nums:
            nxt_f = copy.deepcopy(f)
            if v <= limit:
                if v not in nxt_f:
                    nxt_f[v] = set()
                nxt_f[v].add(v)
            nxt_g = copy.deepcopy(g)

            for s in f:
                nxt_s = s - v
                if nxt_s < -900 or nxt_s > 900:
                    continue
                if nxt_s not in nxt_g:
                    nxt_g[nxt_s] = set()
                for m in f[s]:
                    nxt_m = m * v
                    if nxt_m <= limit:    
                        nxt_g[nxt_s].add(nxt_m)
                if v == 0:
                    nxt_g[nxt_s].add(0)

            for s in g:
                nxt_s = s + v
                if nxt_s < -900 or nxt_s > 900:
                    continue
                if nxt_s not in nxt_f:
                    nxt_f[nxt_s] = set()    
                for m in g[s]:
                    nxt_m = m * v
                    if nxt_m <= limit:    
                        nxt_f[nxt_s].add(nxt_m)
                if v == 0:
                    nxt_f[nxt_s].add(0)
        
            f = copy.deepcopy(nxt_f)
            g = copy.deepcopy(nxt_g)

        res = -1
        if k in f and f[k]:
            res = max(res, max(f[k]))

        if k in g and g[k]:
            res = max(res, max(g[k]))
        
        return res
```
