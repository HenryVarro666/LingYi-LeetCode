---
title: "1696. 跳跃游戏"
aliases: ["yiduobo的每日leetcode 1696.跳跃游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/monotonic-queue", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/十一-优化-DP", "题单/动态规划/专题-跳跃游戏"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/447234303"
zhihu_id: "447234303"
zhihu_title: "yiduobo的每日leetcode 1696.跳跃游戏"
question_id: "1696"
question: "跳跃游戏 VI"
problem_url: "https://leetcode.cn/problems/jump-game-vi/"
difficulty: "Medium"
rating: 1954
created: "2021-12-19T12:39:43+08:00"
updated: "2021-12-19T12:39:43+08:00"
upvotes: 0
comments: 0
---

# 1696. 跳跃游戏

> **[yiduobo的每日leetcode 1696.跳跃游戏](https://zhuanlan.zhihu.com/p/447234303) · 知乎 · 2021-12-19 · 赞同 0**
> 力扣：[1696. 跳跃游戏 VI](https://leetcode.cn/problems/jump-game-vi/) · Medium · 灵茶山艾府：[一步步优化：从递归到递推到单调队列（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1696.跳跃游戏

[力扣](https://leetcode-cn.com/problems/jump-game-vi/)

动态规划的题目。令f[i]表示跳到i这个位置时的最大得分，那么对于f[i]，就有

f[i] \= max(f[j]) + nums[i]，其中j满足max(0, i - k) \<\= j \< i

直接使用这个转移方程来做的话是O(n^2)的，需要优化。注意到这里算是一个区间最大值问题，因此可以使用logn级的数据结构来优化。当然这种向后推移的区间最值问题也可以使用单调双向队列来做。

对于两个位置j和k，不妨设j \< k且f[j] \<\= f[k]，那么对于任意大于k的位置i：

1、由于j \< k，因此j如果可以更新到i，那么k必然也可以更新到i

2、由于f[j] \<\= f[k]，因此f[j] + nums[i] \<\= f[k] + nums[i]

也就是说此时没有必要继续保留j了

于是现在就有了一种做法。维护一个单调递减的双向队列deque来保存所有可用的上一个位置，然后从头开始向后枚举每个位置i，对于当前的i：

1、若deque不为空，且i - deque[0] > k，说明deque[0]已经超出了可用区间的左边界，此时需要将deque[0]弹出。重复此过程直到deque为空或者i - deque[0] \<\= k

2、此时首先用f\[i - 1\] + nums\[i\]来更新f\[i\]。若deque不为空，那么此时deque\[0\]对应的f是最大的可用位置，于是用f\[deque\[0\]\] + nums\[i\]来更新f\[i\]

3、得到f\[i\]之后，使用f\[i\]来更新deque。若deque不为空，且f\[deque\[-1\]\] \<\= f\[i\]，那么就将deque\[-1\]弹出。重复此过程直到deque为空或者f\[deque\[-1\]\] >\= f\[i\]。最后还需要将i加入到deque中

动态规划完成后，f[-1]就是最终答案了。此时状态转移的复杂度为O(1)，而对于每个位置，最多进出deque一次，均摊下来也是O(1)，因此最终的时间复杂度就是O(n)

最后附上python代码：

```python
class Solution(object):
    def maxResult(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        stack = [0]
        f = [nums[0]]
        l = 0

        for index in range(1, len(nums)):
            num = nums[index]
            while l < len(stack) and index - stack[l] > k:
                l += 1
            
            f.append(f[-1] + num)
            if l < len(stack):
                f[-1] = max(f[-1], f[stack[l]] + num)
            
            while len(stack) > l and f[stack[-1]] <= f[-1]:
                stack.pop()
            
            stack.append(index)
        
        return f[-1]
```
