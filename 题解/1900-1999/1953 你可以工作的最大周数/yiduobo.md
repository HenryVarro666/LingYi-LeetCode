---
title: "1953. 你可以工作的最大周数"
aliases: ["yiduobo的每日leetcode 1953.你可以工作的最大周数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/492247728"
zhihu_id: "492247728"
zhihu_title: "yiduobo的每日leetcode 1953.你可以工作的最大周数"
question_id: "1953"
question: "你可以工作的最大周数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-weeks-for-which-you-can-work/"
difficulty: "Medium"
rating: 1804
created: "2022-04-02T18:13:21+08:00"
updated: "2022-04-02T18:13:21+08:00"
upvotes: 0
comments: 0
---

# 1953. 你可以工作的最大周数

> **[yiduobo的每日leetcode 1953.你可以工作的最大周数](https://zhuanlan.zhihu.com/p/492247728) · 知乎 · 2022-04-02 · 赞同 0**
> 力扣：[1953. 你可以工作的最大周数](https://leetcode.cn/problems/maximum-number-of-weeks-for-which-you-can-work/) · Medium · 灵茶山艾府：[结论题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1953.你可以工作的最大周数

[力扣](https://leetcode-cn.com/problems/maximum-number-of-weeks-for-which-you-can-work/)

之前好像遇到过一个简化版的题，那个题里面的n确定就等于3，而得到的最终结论就是设数组中的最大值为max_n，总和为s，那么若max_n \<\= s - max_n + 1，就可以全部完成，答案为s，否则答案为是(s - max_n) \* 2 + 1。

对于本题，也是同样的结论。记milestone从大到小的顺序进行排序后的结果为m，那么：

1、若此时的m[0] \= m[1]：

首先不断循环执行任务0和任务1，直到m[0] \= m[1] \= m[2]

接下来则不断循环执行任务0、任务1、任务2，直到m[0] \= m[1] \= m[2] \= m[3]

以此类推，不断循环执行前k个m值相等的任务，直到其m等于第k + 1个任务的m，这样就可以保证所有任务全部做完

2、若此时的m[0] > m[1]：

首先不断循环执行任务0和任务n - 1，直到m[0] \= m[1] + 1或者m[n - 1] \= 0。若某一时刻m[n - 1] \= 0，且m[0]依然大于m[1]，那么就不断循环执行任务0和任务n - 2，直到m[0] \= m[1] + 1或者m[n - 2] \= 0。

重复上面的过程，直到m[0] \= m[1] + 1。在这个过程中，最多消耗掉其他所有的任务。若某一时刻可以使得m[0] \= m[1] + 1，那么必然要满足

m[0] - m[2] - m[3] - ... - m[n - 1] \<\= m[1] + 1

即

m[0] \<\= m[1] + m[2] + ... + m[n - 1] + 1 \= s - m[0] + 1

若某一时刻m[0] \= m[1] + 1，那么首先从m[0]中剥离出一个任务，此时就有m[0] \= m[1] >\= m[2] >\= ... >\= m[n - 1]，此时就变为了情况1，已经明确可以得到一个不以任务0结尾，且可以把所有任务都执行完的执行序列。最后再将之前从m[0]中剥离出来的任务0放在执行序列的最末尾，就可以保证所有任务全部做完

综合上面两种情况，说明了只要m[0] \<\= s - m[0] + 1，就可以执行完所有任务，答案为s。

反过来若m[0] > s - m[0] + 1，那么就应该尽可能多安排任务0,。可以发现，上面讨论中的情况2就已经是尽最大的可能安排任务0了。一直到m[n - 1]到m[2]被消耗完为止，一共安排了m[2] + m[3] + ... + m[n - 1]个任务0。接下来对于剩下的m[0]和m[1]，二者交替则还可以安排m[1] + 1场任务0，因此总共可以安排

m[1] + m[2] + ... + m[n - 1] + 1 \= s - m[0] + 1场任务0，因此总共可以安排的任务数为

s - m[0] + 1 + m[1] + m[2] + ... + m[n - 1] \= (s - m[0]) \* 2 + 1

最后附上python代码：

```python
class Solution(object):
    def numberOfWeeks(self, milestones):
        """
        :type milestones: List[int]
        :rtype: int
        """

        s = sum(milestones)
        max_n = max(milestones)

        if max_n > s - max_n + 1:
            return s - max_n + s - max_n + 1
        
        return s
```
