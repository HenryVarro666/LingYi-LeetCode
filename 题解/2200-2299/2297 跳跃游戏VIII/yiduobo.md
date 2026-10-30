---
title: "2297. 跳跃游戏VIII"
aliases: ["yiduobo的每日leetcode 2297.跳跃游戏VIII"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629368313"
zhihu_id: "629368313"
zhihu_title: "yiduobo的每日leetcode 2297.跳跃游戏VIII"
question_id: "2297"
question: "跳跃游戏VIII"
problem_url: "https://leetcode.cn/problems/jump-game-viii/"
created: "2023-05-15T02:07:30+08:00"
updated: "2023-05-15T02:07:30+08:00"
upvotes: 0
comments: 0
---

# 2297. 跳跃游戏VIII

> **[yiduobo的每日leetcode 2297.跳跃游戏VIII](https://zhuanlan.zhihu.com/p/629368313) · 知乎 · 2023-05-15 · 赞同 0**
> 力扣：[2297. 跳跃游戏VIII](https://leetcode.cn/problems/jump-game-viii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2297.跳跃游戏III

[力扣](https://leetcode.cn/problems/jump-game-viii/)

观察题目中跳跃的条件，可以发现：

1、每个位置必然可以跳到下一个位置的

2、每个位置如果要越过某些位置向后跳，那么其最多只有一个落脚点j。对于题目给出的两个条件而言，第一个条件要求nums[k] \< nums[i]，而第二个条件要求nums[k] >\= nums[i]，也就是说不可能同时满足。另一方面，也不可能出现连续满足同一个条件的情况，因为对于条件1中的nums[j]，要求nums[j] >\= nums[i]，而对于j右侧的位置，j在这里作为新的nums[k]就不满足nums[k] \< nums[i]这个条件了。对于条件2也同样可以这样证明。

而对于落脚点的求解，第一个条件中的落脚点可以通过一个单调递减的栈mi来求解，而第二个条件中的落脚点则可以通过单调递增的栈ma来求解。

根据这两个结论，就得到了一种动态规划的做法。令f[i]表示跳到位置i所需的最小代价，那么对于f[i]：

1、首先可以初始化f[i] \= f[i - 1] + cost[i]

2、接下来对于这两个栈：

2-1）若mi栈顶元素小于等于nums\[i\]，也就是nums\[mi\[-1\]\] \<\= nums\[i\]，那么根据条件1就可以从mi\[-1\]跳到i这个位置，于是有f\[i\] \= min(f\[i\], f\[mi\[-1\]\] + cost\[i\])。另一方面，mi\[-1\]以及找到了唯一的落脚点，因此需要将其从栈中弹出。最后，还需要将i加入到mi中。

2-2）同样的，若ma栈顶元素大于nums\[i\]，也就是nums\[ma\[-1\]\] > nums\[i\]，那么根据条件2就可以从ma\[-1\]跳到i这个位置，于是有f\[i\] \= min(f\[i\], f\[ma\[-1\]\] + cost\[i\])。另一方面，ma\[-1\]以及找到了唯一的落脚点，因此需要将其从栈中弹出。最后，还需要将i加入到ma中。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums, costs):
        """
        :type nums: List[int]
        :type costs: List[int]
        :rtype: int
        """

        f = [0]
        mi = [0]
        ma = [0]

        n = len(nums)
        for index in range(1, n):
            f.append(f[-1] + costs[index])

            while mi and nums[mi[-1]] <= nums[index]:
                f[-1] = min(f[-1], f[mi[-1]] + costs[index])
                mi.pop()
            
            while ma and nums[ma[-1]] > nums[index]:
                f[-1] = min(f[-1], f[ma[-1]] + costs[index])
                ma.pop()
            
            mi.append(index)
            ma.append(index)
        
        return f[-1]
```
