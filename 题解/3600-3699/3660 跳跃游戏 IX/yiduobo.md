---
title: "3660. 跳跃游戏IX"
aliases: ["yiduobo的每日leetcode 3660.跳跃游戏IX"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950244317412164841"
zhihu_id: "1950244317412164841"
zhihu_title: "yiduobo的每日leetcode 3660.跳跃游戏IX"
question_id: "3660"
question: "跳跃游戏 IX"
problem_url: "https://leetcode.cn/problems/jump-game-ix/"
difficulty: "Medium"
rating: 2187
created: "2025-09-14T15:48:29+08:00"
updated: "2025-09-14T15:48:29+08:00"
upvotes: 0
comments: 0
---

# 3660. 跳跃游戏IX

> **[yiduobo的每日leetcode 3660.跳跃游戏IX](https://zhuanlan.zhihu.com/p/1950244317412164841) · 知乎 · 2025-09-14 · 赞同 0**
> 力扣：[3660. 跳跃游戏 IX](https://leetcode.cn/problems/jump-game-ix/) · Medium · 灵茶山艾府：[结论 + 动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3660.跳跃游戏IX

[3660. 跳跃游戏 IX - 力扣（LeetCode）](https://leetcode.cn/problems/jump-game-ix/description/)

题目给出一个整数数组nums。

从下标i出发，可以向前跳到任意一个nums[j] > nums[i]的下标j，也可以向后跳到任意一个nums[j] \< nums[i]的下标j。

问对于nums中的每个下标，从该下标出发且可以跳跃任意次可以到达的最大值是多少。

对于nums中的每个下标，最理想的情况自然是跳跃到数组中的最大值所在的位置，而为了到达这个位置，则应该遵照先向左跳到可以到达的最大值，然后向右可以到达的最远的位置，然后再向左跳到可以到达的最大值，以此类推，直到无处可跳或者进入循环为止。

对于以上的跳跃方法，先向左跳的理由是对于某个位置，先向左跳之后数值会更大，接下来再往右跳可以跳的位置就更远。

对于向左跳的操作，应该跳到目前可达的数值最大的位置，一方面这样得到的数值更大，另一方面接下来如果需要再向右跳，可以跳的位置也更远。

而对于向右跳的操作，则应该跳到最远而不是数值最小的位置，因为向右跳的目的是为了能通过向左跳到达数值更大的位置。

对于从某个位置p出发向右跳可达的两个位置i和j，若i \< j，那么从i出发向左跳的目的地就应该选择p + 1到i - 1之间的某个大于nums[p]的位置，如果没有理想的位置，那么跳回到p然后就可以结束跳跃了。理由是此时的p是经过一次左跳得到的位置，也就是说nums[p]必然是前缀0到p之间的最大值，因此不会再往前跳到p - 1之前的位置。另一方面，如果从i跳到了一个还不如nums[p]的位置，那么和最上面的向左跳应该跳到数值最大的位置就矛盾了。

基于这一点，对于p可以到达的i和j，若i \< j，那么i可以到达的位置j也可以到达，但是i + 1到j - 1之间的位置i不可能到达，但是j可能到达，因此从p出发向右跳，就应该跳到最远，而不是最小的下标。

根据以上的结论，就只需计算出从每个位置向左跳可以到达的最大的位置的下标，以及向右跳可以到达的最远的位置的下标，然后一趟遍历，通过类似记忆化搜索的方式计算出每个位置可以到达的最大的值就行了。

具体来说，对于当前位置index，令其向左可以到达的最大值的下标为p，那么：

1、若p小于index，那么先递归计算p对应的结果，而index对应的结果就是p对应的结果

2、若p就是index本身，那么就无需向左跳了，直接考虑向右跳。记q为index向右跳可以到达的最远位置，q不存在，或者q向左跳可以到达的最远位置就是index，那么就无需反复横跳了，下标index对应的答案就是nums[index]

3、否则的话先递归计算q对应的结果，而index对应的结果就是q对应的结果

要得到向左跳可以到达的最大位置的下标，只需一趟遍历，记录前缀中最大值的下标就行了。而为了得到向右跳可以到达的最远位置的下标，则需要先将nums进行离散化，得到每个元素在数组中的序，然后倒序遍历，利用树状数组进行求解。

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        n = len(nums)

        left = [0]
        for index in range(1, n):
            if nums[index] >= nums[left[-1]]:
                left.append(index)
            else:
                left.append(left[-1])
        
        mapping = {}
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = len(mapping) + 1
        

        m = len(mapping)
        f = [-1] * (m + 1)

        def add(x, v):
            while x <= m:
                f[x] = max(f[x], v)
                x += x & -x
        
        def get(x):
            ma = -1
            while x:
                ma = max(ma, f[x])
                x -= x & -x
            return ma

        rightest = [-1]
        add(mapping[nums[-1]], n - 1)
        for index in range(n - 2, -1, -1):
            rightest.append(get(mapping[nums[index]] - 1))
            add(mapping[nums[index]], index)
        rightest.reverse()
        
        
        res = [None] * n
        
        def calc(index, res):
            if res[index] is None:
                p = left[index]
                if p != index:
                    res[index] = calc(p, res)
                elif rightest[index] == -1 or left[rightest[index]] == index:
                    res[index] = nums[index]
                else:
                    res[index] = calc(rightest[index], res)
            
            return res[index]

        for index in range(n):
            if res[index] is None:
                calc(index, res)
        
        return res
```
