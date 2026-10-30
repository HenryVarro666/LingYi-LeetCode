---
title: "3205. 最大数组跳跃得分I"
aliases: ["yiduobo的每日leetcode 3205.最大数组跳跃得分I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707553192"
zhihu_id: "707553192"
zhihu_title: "yiduobo的每日leetcode 3205.最大数组跳跃得分I"
question_id: "3205"
question: "最大数组跳跃得分I"
problem_url: "https://leetcode.cn/problems/maximum-array-hopping-score-i/"
created: "2024-07-07T23:56:38+08:00"
updated: "2024-07-07T23:56:38+08:00"
upvotes: 0
comments: 0
---

# 3205. 最大数组跳跃得分I

> **[yiduobo的每日leetcode 3205.最大数组跳跃得分I](https://zhuanlan.zhihu.com/p/707553192) · 知乎 · 2024-07-07 · 赞同 0**
> 力扣：[3205. 最大数组跳跃得分I](https://leetcode.cn/problems/maximum-array-hopping-score-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3205.最大数组跳跃得分I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-array-hopping-score-i/description/)

题目给出一个数组nums，要求从下标0开始向后跳，直到到达数组的最后一个元素。对于每次跳跃，只能从当前下标i跳到某个j > i的下标j，这次跳跃的得分为(j - i) \* nums[j]。问跳到数组末尾时最大可能的得分是多少。

观察题目中给出的得分式子，可以发现从0跳到数组末尾的距离总和是一定的，那么为了得分最大，就应该尽量放大后续的nums[j]。

在这里可以先证明数组中的最大值nums[ma]是必然会被作为某次跳跃的终点，若其不是某次跳跃的终点，那么不妨设某次从nums[p]到nums[q]的跳跃直接越过了nums[ma]，即p \< ma \< q，那么在这里可以先从p跳到ma，再跳到q，得分就是(ma - p) \* nums[ma] + (q - ma) \* nums[q]，另一方面，直接跳跃的得分为(q - p) \* nums[q]，而

(ma - p) \* nums[ma] + (q - ma) \* nums[q] > (ma - p) \* nums[q] + (q - ma) \* nums[q] \= (q - p) \* nums[q]

也就是说选择ma作为中继点的得分更优。

接下来，可以证明从0点开始应该直接跳到ma，得分为ma \* nums[ma]。若其中经过了某点p，那么得分为p \* nums[p] + (ma - p) \* nums[ma]，而

p \* nums[p] + (ma - p) \* nums[ma] \< p \* nums[ma] + (ma - p) \* nums[ma] \= ma \* nums[ma]

也就是说直接跳到ma的得分更优。

根据上面的结论，就可以先从0跳到ma，而接下来从ma起跳的问题，则可以认为子问题给出一个数组nums[ma + 1:]，从数组头跳到数组尾的最佳得分，那么此时就应该找到nums[ma + 1:]中的最大值对应的下ma'，然后从ma跳到ma'，接下来从ma'起跳继续找剩余数组中的最大值，直到来到数组末尾。

对于这个问题，只需从后往前倒序遍历找出一个递增的序列，若当前遍历到的元素大于序列的末尾元素，就将其加入到序列中，并计算从当前位置跳到序列末尾元素对应的位置的得分并累加。遍历完成后，再加上从下标0跳到序列末尾元素对应位置的得分即可。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        p = n - 1
        res = 0

        for index in range(n - 2, 0, -1):
            if nums[index] > nums[p]:
                res += (p - index) * nums[p]
                p = index
        
        res += p * nums[p]
        return res
```
