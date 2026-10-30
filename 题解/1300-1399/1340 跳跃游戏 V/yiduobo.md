---
title: "1340. 跳跃游戏V"
aliases: ["yiduobo的每日leetcode 1340.跳跃游戏V"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/monotonic-stack", "题单/动态规划", "题单/单调栈", "题单/动态规划/专题-跳跃游戏", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/396436211"
zhihu_id: "396436211"
zhihu_title: "yiduobo的每日leetcode 1340.跳跃游戏V"
question_id: "1340"
question: "跳跃游戏 V"
problem_url: "https://leetcode.cn/problems/jump-game-v/"
difficulty: "Hard"
rating: 1866
created: "2021-08-04T23:01:08+08:00"
updated: "2021-08-04T23:01:08+08:00"
upvotes: 0
comments: 0
---

# 1340. 跳跃游戏V

> **[yiduobo的每日leetcode 1340.跳跃游戏V](https://zhuanlan.zhihu.com/p/396436211) · 知乎 · 2021-08-04 · 赞同 0**
> 力扣：[1340. 跳跃游戏 V](https://leetcode.cn/problems/jump-game-v/) · Hard · 灵茶山艾府：[两种方法：正着跳 / 倒着跳，O(n) 时间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1340.跳跃游戏V

[力扣](https://leetcode-cn.com/problems/jump-game-v/)

首先，从某个位置开始是可以向左或者向右跳的，根据题目描述来看似乎有很多可以选择的目标地点，但是实际上左边和右边最佳的目标地点是有限的。

不妨设我们现在要往左跳，设当前位置为p，同时设i为p - i到p - 1之间，满足arr[i] \< arr[p]同时arr[i]最大的位置，另外设j为p - i到p - 1之间，满足arr[i] \< arr[p]的另一个位置，那么

1、p - i \<\= d且p - j \<\= d

我们可以推出abs(i - j) \<\= d

2、arr[i]到arr[j]之间的所有位置k对应的arr[k]都满足arr[k] \< arr[i]，因为这里的前提条件是arr[i]是满足条件的位置中arr最大的那个位置。

通过以上两点，我们可以知道从i开始是可以选择j作为下一跳的目标地点的，因此当我们从p开始起跳时，显然不应该选择j作为下一跳的目标，因为我们此时可以先从p跳到i，再从i跳到j，必然是由于直接从p跳到j的。

换言之，对于每个位置p，实际上可以选择的下一跳的位置并不多。不妨设x为arr[p - i]到arr[p - 1]中小于arr[p]的最大arr值，那么从p开始向左跳的候选位置就是p - i到p - 1之间所有值等于x的位置。同样地，从p开始向右跳的候选位置就是p + 1到p + i之间所有值等于不超过arr[p]的最大值的位置。

这样一来，我们就可以先通过正反两趟扫描，借助单调栈求出每个位置下一跳的候选数组。

以求解左侧候选目的地为例。不妨设有两个位置i和j，满足i \< j且arr[i] \< arr[j]，那么对于j之后的所有位置p而言，i都不可能成为目的地，因为若p的目的地选择了i，就说明arr[p] > max(arr[i], arr[p - 1]) >\= arr[j]，j也是p的合法目的地，因此此时选择j作为p的目的地显然是更好的，于是i不可能成p下一跳的目的地。

转化一下，就是使用一个单调递减的栈来维护所有可能的下一跳目的地，那么对于当前位置p，若当前栈顶对应的arr小于arr\[p\]，那么需要将栈顶弹出。同时若栈顶对应的位置与p之间的距离在d之内，那么说明栈顶位置是合法的下一跳位置，那么此时需要检测arr\[p\] - arr\[stack\[-1\]\]的值并更新候选位置。

求得所有目的地候选集之后，令f[i]表示从位置i起跳的最大步数，那么对于f[i]：

1、我们可以向左跳，那么此时应该枚举左侧候选目的地中的每个位置left[index]，于是有

f\[i\] \= max(f\[i\], f\[left\[index\]\] + 1）

2、我们也可以向右跳，那么此时应该枚举右侧候选目的地中的每个位置right[index]，于是有

f\[i\] \= max(f\[i\], f\[right\[index\]\] + 1)

上面的做法看上去并不是严格的O(n)，但是实际上每个位置最多只会成为一次左侧目的地以及一次右侧目的地，因此均摊下来总体的时间复杂度还是O(n)的。

最后附上python代码：

```python
class Solution(object):
    def maxJumps(self, arr, d):
        """
        :type arr: List[int]
        :type d: int
        :rtype: int
        """

        n = len(arr)
        stack = [0]
        left = [None]
        for index in range(1, n):
            left.append(None)
            while stack and arr[stack[-1]] < arr[index]:
                if index - stack[-1] <= d:
                    if left[-1] is None or arr[left[-1][0]] < arr[stack[-1]]:
                        left[-1] = [stack[-1]]
                    else:
                        left[-1].append(stack[-1])
                stack.pop()
            stack.append(index)
        
        stack = [n - 1]
        right = [None]
        for index in range(n - 2, -1, -1):
            right.append(None)
            while stack and arr[stack[-1]] < arr[index]:
                if stack[-1] - index <= d:
                    if right[-1] is None or arr[right[-1][0]] < arr[stack[-1]]:
                        right[-1] = [stack[-1]]
                    else:
                        right[-1].append(stack[-1])
                stack.pop()
            stack.append(index)
        right.reverse()

        f = [None] * n
        for index in range(n):
            if f[index] is None:
                self.dfs(index, f, left, right)
        
        return max(f)
    
    def dfs(self, now, f, left, right):
        if f[now] is None:
            tmp = 0
            if left[now] is not None:
                for next in left[now]:
                    tmp = max(tmp, self.dfs(next, f, left, right))
            if right[now] is not None:
                for next in right[now]:
                    tmp = max(tmp, self.dfs(next, f, left, right))
            f[now] = tmp + 1
        
        return f[now]
```
