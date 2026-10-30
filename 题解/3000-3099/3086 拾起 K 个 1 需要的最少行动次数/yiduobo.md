---
title: "3086. 拾起K个1需要的最少行动次数"
aliases: ["yiduobo的每日leetcode 3086.拾起K个1需要的最少行动次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/一-前缀和", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698855764"
zhihu_id: "698855764"
zhihu_title: "yiduobo的每日leetcode 3086.拾起K个1需要的最少行动次数"
question_id: "3086"
question: "拾起 K 个 1 需要的最少行动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-pick-k-ones/"
difficulty: "Hard"
rating: 2673
created: "2024-05-20T21:23:41+08:00"
updated: "2024-05-20T21:23:41+08:00"
upvotes: 2
comments: 0
---

# 3086. 拾起K个1需要的最少行动次数

> **[yiduobo的每日leetcode 3086.拾起K个1需要的最少行动次数](https://zhuanlan.zhihu.com/p/698855764) · 知乎 · 2024-05-20 · 赞同 2**
> 力扣：[3086. 拾起 K 个 1 需要的最少行动次数](https://leetcode.cn/problems/minimum-moves-to-pick-k-ones/) · Hard · 灵茶山艾府：[中位数贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3086.拾起K个1需要的最少行动次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-moves-to-pick-k-ones/description/)

题目给出一个01组成的数组，可以在数组中选择任意位置作为初始位置index进行拾取。另外还给出两种操作：

第一种是特殊操作，最多执行maxChanges次，可以让一个不处于index且等于0的数变为1

第二种操作使常规操作，可以执行任意次，可以交换相邻的0和1。

任意时刻若index对应的值为1，则可以拾取这个1，拾取操作不计入操作数。问拾取k个1需要的最少操作次数。

首先考虑特殊操作。由于特殊操作不能直接将index对应的值设置为1，那么就可以将index相邻位置上的值设置为1，然后利用常规操作将其交换到index，换言之，特殊操作就相当于通过两次操作拾取了一个1。

而对于常规操作，首先index如果直接设置在某个1上，那么相当于使用0次操作拾取了一个1；另外，如果index两侧有相邻的1，那么就相当于使用1次操作拾取了某一侧相邻的1；除了上面两种情况之外，拾取1的代价值均大于等于2，也就是说此时应该优先用完特殊操作，那么在这里就可以先处理各种特殊情况。

一趟遍历，检测nums中是否存在三个连续的1、两个连续的1、一个1，分别记为three、two、one。接下来：

1、若three为true，且k >\= 3，同时k - maxChanges \<\= 3，那么在这里就可以选择three对应的三个连续的1的正中间作为index，然后使用1 + 0 + 1 \= 2的代价拾取这三个连续的1。接下来对于剩下的k - 3个1，则都通过特殊操作来进行拾取，此时对应的答案就是2 + (k - 3) \* 2

2、在不满足情况1的前提下，若two为true，且k >\= 2，同时k - maxChanges \<\= 2，那么在这里就可以选择two对应的两个连续的1中的任意一个作为index，然后使用1 + 0 \= 1的代价拾取这两个连续的1。接下来对于剩下的k - 2个1，则都通过特殊操作来进行拾取，此时对应的答案就是1 + (k - 2) \* 2

3、在不满足情况1、2的前提下，若one为true，且k - maxChanges \<\= 1，那么在这里就可以选择任意一个1所在的位置作为index，然后使用0的代价拾取这个1。接下来对于剩下的k - 1个1，则都通过特殊操作来进行拾取，此时对应的答案就是(k - 1) \* 2

4、在不满足情况1、2、3的前提下，若k \<\= maxChanges，那么通过不满足情况3可以得知此时的nums全都是0，那么就可以任选位置作为index，然后通过k此特殊操作拾取k个1，此时对应的答案就是k \* 2

如果上述情况都不满足，那么就说明特殊操作的可用次数maxChanges还不够多。由于后续必然要通过常规操作拾取相邻位置之外的1，因此特殊操作可以默认全部使用，那么问题就变成了如何使用常规操作拾取k - maxChanges个1。方便起见，在这里将k更新为k - maxChanges。

对于常规操作，想要获取处于p的1，需要将p交换到index然后拾取，那么交换的次数就是abs(index - p)，换言之就是二者下标的距离。为了使得交换的次数最小，那么此时拾取的k个1一定处于一个连续的区间内，也就是说在这里可以使用一个边长的滑动窗口从左向右滑动，保证窗口内刚好有k个1，然后分别计算拾取这些窗口内的1需要的最小代价，加上特殊操作所需的maxChanges \* 2来更新最终答案。

此时的问题就变成了对于一段具有k个1的子数组，选择一个位置index，使得index到这k个1的距离和最小。这是经典的中位数贪心问题，将index设置在正中间的1所处的位置是最优的，此时的距离之和则可以通过index右侧所有1的下标之和减去index左侧所有1的下标之和计算得到，也就是两段区间和之差，通通可以转化成前缀和之差进行求解。在这里需要特别注意的是，当k为奇数时，存在唯一一个可行的index，而当k为偶数时，index则可以放在正中间的两个1之间的任意位置，在计算前缀和之差时需要注意分情况处理。

最后附上python代码：

```python
class Solution(object):
    def minimumMoves(self, nums, k, maxChanges):
        """
        :type nums: List[int]
        :type k: int
        :type maxChanges: int
        :rtype: int
        """

        n = len(nums)
        pos_list = []
        three = two = one = False
        for index in range(n):
            if nums[index] == 1:
                pos_list.append(index)
                one = True
                if index > 0 and nums[index - 1] == 1:
                    two = True
                    if index > 1 and nums[index - 2] == 1:
                        three = True

        if k >= 3 and k - maxChanges <= 3 and three:
            return 2 + (k - 3) * 2
        elif k >= 2 and k - maxChanges <= 2 and two:
            return 1 + (k - 2) * 2
        elif k - maxChanges <= 1 and one:
            return (k - 1) * 2
        elif k <= maxChanges:
            return k * 2

    
        k -= maxChanges
        
        prefix_s = [0]
        for v in pos_list:
            prefix_s.append(prefix_s[-1] + v)
        
        res = None
        print pos_list, k
        for left in range(len(pos_list) - k + 1):
            right = left + k - 1
            mid = (left + right) // 2

            if k % 2 == 0:
                cost = prefix_s[right + 1] - prefix_s[mid + 1] - (prefix_s[mid + 1] - prefix_s[left])
            else:
                cost = prefix_s[right + 1] - prefix_s[mid + 1] - (prefix_s[mid] - prefix_s[left])

            cost += maxChanges * 2

            if res is None or res > cost:
                res = cost
        
        return res
```
