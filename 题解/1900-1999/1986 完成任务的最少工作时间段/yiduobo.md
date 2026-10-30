---
title: "1986. 完成任务的最少工作时间段"
aliases: ["yiduobo的每日leetcode 1986.完成任务的最少工作时间段"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/499428849"
zhihu_id: "499428849"
zhihu_title: "yiduobo的每日leetcode 1986.完成任务的最少工作时间段"
question_id: "1986"
question: "完成任务的最少工作时间段"
problem_url: "https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/"
difficulty: "Medium"
rating: 1995
created: "2022-04-16T00:56:09+08:00"
updated: "2022-04-16T00:56:10+08:00"
upvotes: 0
comments: 0
---

# 1986. 完成任务的最少工作时间段

> **[yiduobo的每日leetcode 1986.完成任务的最少工作时间段](https://zhuanlan.zhihu.com/p/499428849) · 知乎 · 2022-04-16 · 赞同 0**
> 力扣：[1986. 完成任务的最少工作时间段](https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/) · Medium · 灵茶山艾府：[子集动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1986.完成任务的最少工作时间段

[力扣](https://leetcode-cn.com/problems/minimum-number-of-work-sessions-to-finish-the-tasks/)

没有想到什么特别好的做法，不过由于这里n的规模比较小，因此可以使用状态压缩动态规划来做。

令f[state]表示选择state中的任务所需的最少工作时间，这里的保存的是具体的小时而不是时间段的数量。

对于f[state]而言，在最后一个时间段中已经使用的时间就是

used_part_time \= f[state] % sessionTime

接下来枚举所有没有使用过的任务，对于枚举到的任务index，执行该任务后状态就变成了

next_state \= state | (1 \<\< index)

另一方面，则是关于用时的计算。

若used_part_time + tasks[index] \<\= sessionTime，说明可以在最后这个时间段内完成index，于是有

f[next_state] \= min(f[next_state], f[state] + tasks[index])

若used_part_time + tasks[index] > sessionTime，那么说明需要额外安排一个时间段来执行index这个任务，于是有

f[next_state] \= min(f[next_state], f[state] - used_part_time + sessionTime + tasks[index])

动态规划完成后，f[(1 \<\< n) - 1]就是完成所有任务所需的小时数，通过这个时间计算出所需的时间段即可。

最后附上python代码：

```python
class Solution(object):
    def minSessions(self, tasks, sessionTime):
        """
        :type tasks: List[int]
        :type sessionTime: int
        :rtype: int
        """

        n = len(tasks)
        max_state = (1 << n)
        f = {}
        f[0] = 0
        q = [0]
        l = 0
        r = 1

        while l < r:
            now_state = q[l]
            l += 1
            used_part_time = f[now_state] % sessionTime
            for index in range(n):
                if (now_state & (1 << index)) == 0:
                    next_state = now_state | (1 << index)
                    if tasks[index] + used_part_time <= sessionTime:
                        next_time = f[now_state] + tasks[index]
                    else:
                        next_time = f[now_state] - used_part_time + sessionTime + tasks[index]
                    
                    if next_state not in f:
                        f[next_state] = next_time
                        q.append(next_state)
                        r += 1
                    else:
                        f[next_state] = min(f[next_state], next_time)
        
        res = f[max_state - 1] / sessionTime
        if f[max_state - 1] % sessionTime != 0:
            res += 1
        return res
```
