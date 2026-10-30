---
title: "3877. 达到目标异或值的最少删除次数"
aliases: ["yiduobo的每日leetcode 3877.达到目标异或值的最少删除次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/图论算法", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/三-背包", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2019893708733068359"
zhihu_id: "2019893708733068359"
zhihu_title: "yiduobo的每日leetcode 3877.达到目标异或值的最少删除次数"
question_id: "3877"
question: "达到目标异或值的最少删除次数"
problem_url: "https://leetcode.cn/problems/minimum-removals-to-achieve-target-xor/"
difficulty: "Medium"
rating: 1745
created: "2026-03-24T22:12:14+08:00"
updated: "2026-03-24T22:12:35+08:00"
upvotes: 3
comments: 0
---

# 3877. 达到目标异或值的最少删除次数

> **[yiduobo的每日leetcode 3877.达到目标异或值的最少删除次数](https://zhuanlan.zhihu.com/p/2019893708733068359) · 知乎 · 2026-03-24 · 赞同 3**
> 力扣：[3877. 达到目标异或值的最少删除次数](https://leetcode.cn/problems/minimum-removals-to-achieve-target-xor/) · Medium · 灵茶山艾府：[两种方法：0-1 背包 / BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3877.达到目标异或值的最少删除次数

<https://leetcode.cn/problems/minimum-removals-to-achieve-target-xor/description/>

题目给出一个整数数组nums和一个整数target。

现在可以从nums中移除任意数量的元素，问使得剩余元素按位异或和恰好等于target所需的最小移除次数。若无法达到target，则返回-1。

题目移除尽量少的元素，使得剩下的元素异或值等于target，就相当于从中选取尽量多的元素，使得这些元素的异或值等于target。对于这个问题，则可以使用动态规划进行求解。

令f[index][pre]表示从nums[0]到nums[index]中选取若干个元素，这些元素的异或值恰好等于pre时，最多可以选取多少个元素。对于f[index][pre]：

1、如果放弃掉nums[index]，那么就有f[index + 1][pre] \= max(f[index +1][pre], f[index][pre])

2、如果使用nums[index]，那么令nxt \= pre ^ nums[index]，就有f[index + 1][nxt] \= max(f[index + 1][nxt], f[index][pre] + 1)

全部计算完成后，最终答案就是f[-1][target]。

注意到每一列的状态只与上一轮有关，因此在这里可以通过滚动数组省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def minRemovals(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        
        ma = max(max(nums), target)
        p2 = 1
        while p2 <= ma:
            p2 += p2
        
        f = [-1] * (p2 + 1)
        f[0] = 0
        for v in nums:
            g = f[:]
            for pre in range(p2 + 1):
                if g[pre] != -1:
                    nxt = pre ^ v
                    f[nxt] = max(f[nxt], g[pre] + 1)

        if f[target] == -1:
            return -1
        return len(nums) - f[target]
```
