---
title: "1425. 带限制的子序列和"
aliases: ["yiduobo的每日leetcode 1425.带限制的子序列和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/408802499"
zhihu_id: "408802499"
zhihu_title: "yiduobo的每日leetcode 1425.带限制的子序列和"
question_id: "1425"
question: "带限制的子序列和"
problem_url: "https://leetcode.cn/problems/constrained-subsequence-sum/"
created: "2021-09-09T23:37:14+08:00"
updated: "2021-09-09T23:37:51+08:00"
upvotes: 0
comments: 0
---

# 1425. 带限制的子序列和

> **[yiduobo的每日leetcode 1425.带限制的子序列和](https://zhuanlan.zhihu.com/p/408802499) · 知乎 · 2021-09-09 · 赞同 0**
> 力扣：[1425. 带限制的子序列和](https://leetcode.cn/problems/constrained-subsequence-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1425.带限制的子序列和

[力扣](https://leetcode-cn.com/problems/constrained-subsequence-sum/)

经典的动态规划问题。令f[i]表示以nums[i]结尾的最大子序列和，那么对于f[i]而言：

1、首先可以把nums[i]单独拎出来作为备选答案，因此可以先初始化f[i] \= nums[i]

2、另外，根据题目要求，如果我们要选择nums[i]作为子序列的结尾，那么其前面一个数j的选择范围就是i - 1到i - k之间这一共k个数。于是就有f[i] \= max(f[i], nums[i] + f[j])，其中j的取值范围为i - k \<\= j \<\= i - 1

上面的做法是O(nk)，其中n为数组的长度。这个复杂度太高了，需要想办法优化。

注意到转移方程中每次都是从前k个f中取最大值，那么在这里我们可以使用一个堆来进行优化。不过还存在更好的做法：

若存在一组j1和j2，满足j1 \< j2且f[j1] \<\= f[j2]，那么对于后续的计算，我们是不可能再用到f[j1]来更新答案的。对于后续的任意f[i]而言，若我们选择从f[j1]转移过去，那么就有f[i] \= f[j1] + nums[i]，其i - j1 \<\= k

由于j1 \< j2，那么也必然满足i - j2 \<\= k，而由于f[j2] >\= f[j1]，那么就有f[j2] + nums[i] >\= f[i]，因此我们此时选择从f[j2]转移过来是更好的。

这也就意味着备选位置对应的f是单调递减的。由于我们需要同时关注左边界，因此在这里需要维护一个双端队列q来储存这些位置。

那么对于f[i]：

1、首先初始化f[i] \= nums[i]

2、接下来我们需要调整队列的头部，使得队列中储存的所有位置与i的距离都小于等于k，也就是当i - q[head] > k时，我们将队列头部弹出，直到i - q[head] \<\= k，或队列为空

3、若此时的队列非空，那么其中对应的f最大的位置必然是队列头部q\[head\]。若f\[q\[head\]\]大于0，那么我们就用f\[q\[head\]\] + nums\[i\]来更新f\[i\]

4、最后我们需要用当前的f\[i\]来更新队列。若f\[i\] >\= f\[q\[tail\]\]，那么就将队尾的元素弹出，直到f\[i\] \< f\[q\[tail\]\]，或队列为空。若f\[i\]大于0，我们也将f\[i\]加入到队列的末尾

最后附上python代码：

```python
class Solution(object):
    def constrainedSubsetSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        q = []
        l = r = 0
        res = -10000
        f = []
        for index, num in enumerate(nums):
            while l < r and index - q[l] > k:
                l += 1
            
            f.append(num)
            if r > l:
                f[-1] += f[q[l]]
            res = max(res, f[-1])
            if f[-1] > 0:
                while r > l and f[q[-1]] <= f[-1]:
                    q.pop()
                    r -= 1
        
                q.append(index)
                r += 1

        return res
```
