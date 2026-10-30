---
title: "3956. M个非重叠子数组最大和I"
aliases: ["yiduobo的每日leetcode 3956.M个非重叠子数组最大和I"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/prefix-sum", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2048170834477442248"
zhihu_id: "2048170834477442248"
zhihu_title: "yiduobo的每日leetcode 3956.M个非重叠子数组最大和I"
question_id: "3956"
question: "M 个非重叠子数组最大和 I"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-m-non-overlapping-subarrays-i/"
difficulty: "Hard"
rating: 2061
created: "2026-06-10T22:57:45+08:00"
updated: "2026-06-10T22:57:45+08:00"
upvotes: 1
comments: 0
---

# 3956. M个非重叠子数组最大和I

> **[yiduobo的每日leetcode 3956.M个非重叠子数组最大和I](https://zhuanlan.zhihu.com/p/2048170834477442248) · 知乎 · 2026-06-10 · 赞同 1**
> 力扣：[3956. M 个非重叠子数组最大和 I](https://leetcode.cn/problems/maximum-sum-of-m-non-overlapping-subarrays-i/) · Hard · 灵茶山艾府：[单调队列优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3956.M个非重叠子数组最大和I

<https://leetcode.cn/problems/maximum-sum-of-m-non-overlapping-subarrays-i/>

题目给出一个长度为n的整数数组nums，以及三个整数m、l和r，其中n不超过1000，m、l、r均不超过n。

现在要求从nums中选择至少一个，至多m个互不重叠，且长度在[l, r]范围内的子数组。

问所选子数组的总和最大可能是多少。

选择不重叠子数组类的问题，通常都是用动态规划进行求解。本题的状态表示很容易想到：令f[index][k]表示从前index个元素中选取k个符合条件的子数组所能得到的最大和，那么：

1、首先对于k \= 0的情况，所有的f[index][0]都为0，这个很容易理解，就是一个都没选，所以和显然为0

2、接下来对于k > 0的情况，基于定义，这里index应该从1到n进行遍历，那么对于f[index][k]：

2-1）可以不选择第index个元素，即nums[index]：

此时就有f[index][k] \= f[index - 1][k]

2-2）也可以选择第index个元素：

此时最后这个子数组的右边界就是index - 1，那么还需要决定对应的左边界p。

由于区间长度index - p + 1受到限制，即l \<\= index - p + 1 \<\= r，那么可以得出

index - r + 1 \<\= p \<\= index - l + 1

因此此时的转移方程为

f[index][k] \= max(f[p][k - 1] + nums[p] + nums[p + 1] + ... + nums[index - 1])，其中index - r + 1 \<\= p \<\= index - l + 1

注意到后面是一个区间和，在这里可以提前预处理出前缀和数组s。为了方便计算，在这里规定s[0] \= 0，而s[index] \= nums[0] + nums[1] + ... + nums[index - 1]，那么上面的转移方程就可以写成

f[index][k] \= max(f[p][k - 1] + s[index] - s[p])

这样一来，就得到了一个O(mn(r - l))的算法，不过基于本题的数据规模，极限情况下相当于O(n^3)，必须想办法进行优化。

注意到转移方程中，f[p][k - 1] + s[index] - s[p]，其中s[index]与决策点p无关，那么目标就是找出index - r + 1到index - l + 1之间，使得f[p][k - 1] - s[p]最大的位置p。这是一个区间最大值问题，可以使用线段树进行优化。不过基于本题中p的取值范围是一个随着index向后滑动的窗口这一特定，使用单调队列是更好的方法。

具体来说，对于两个决策点p和q，若满足p \< q，且f[p][k - 1] - s[p] \<\= f[q][k - 1] - s[q]，那么p就不会再成为后续index的最优决策点了，因为对于后续的index，p必然先于q过期，同时选择q的结果必然大于等于选择p的结果，因此在这里就没有必要保留p了。基于这一点，对于当前的index，所有可能的决策点p必然呈现f[p][k - 1] - s[p]单调递减的趋势，因为靠后的决策点如果更好，就可以直接淘汰掉靠前的决策点了。之所有保留靠后的决策点，是因为靠前的决策点可能会自然过期，此时就轮到这些靠后的决策点了。

基于这一点，就可以使用一个队列记录当前所有可能的决策点。对于当前的f[index][k]：

1、若队列头部的决策点在窗口之外，即这个决策点小于index - r，那么就将其从队列中弹出

2、若index >\= l，那么index - l此时就是新的可能的决策点，此时需要对于index - l与队尾的决策点，若f[index - l][k - 1] - s[index - l]更大，那么就需要弹出队尾的决策点，直到队列为空，或者队尾的决策点更优位置。接下来将index - l加入到队列中

3、最后，使用队首更新f[index][k]即可

这样一来，状态转移的复杂度就从O(r - l)优化到了均摊O(1)，整体的复杂度就变成了O(mn)，可以通过本题了。

需要注意的是，本题需要计算的是选取至少一个，至多m个子数组的最优结果，因此在这里的最终结果应该是f[-1][1]、f[-1][2]、...、f[-1][m]中的最大值。

另外，如果按照子数组的数量划分轮次，即先循环后面的k，那么每一轮的转移只与前一个位置以及上一轮有关，此时就可以通过滚动数组优化掉k这一维。

最后附上python代码：

```python
class Solution(object):
    def maximumSum(self, nums, m, l, r):
        """
        :type nums: List[int]
        :type m: int
        :type l: int
        :type r: int
        :rtype: int
        """
        
        n = len(nums)
        f = [0] * (n + 1)
        s = [0]
        for v in nums:
            s.append(s[-1] + v)

        res = None
        for _ in range(m):
            q = []
            head, tail = 0, 0

            g = f[:]
            f = [None] * (n + 1)

            for index in range(1, n + 1):
                if head < tail and index - q[head] > r:
                    head += 1

                if index >= l and g[index - l] is not None:
                    while tail > head and g[index - l] - s[index - l] > g[q[-1]] - s[q[-1]]:
                        q.pop()
                        tail -= 1
                    q.append(index - l)
                    tail += 1
                
                f[index] = f[index - 1]
                
                if head < tail and (f[index] is None or f[index] < g[q[head]] + s[index] - s[q[head]]):
                    f[index] = g[q[head]] + s[index] - s[q[head]]
        
        
            if res is None or res < f[-1]:
                res = f[-1]
            else:
                break

        return res
```
