---
title: "1799. N次操作后的最大分数和"
aliases: ["yiduobo的每日leetcode 1799.N次操作后的最大分数和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463831099"
zhihu_id: "463831099"
zhihu_title: "yiduobo的每日leetcode 1799.N次操作后的最大分数和"
question_id: "1799"
question: "N次操作后的最大分数和"
problem_url: "https://leetcode.cn/problems/maximize-score-after-n-operations/"
created: "2022-02-03T21:30:22+08:00"
updated: "2022-02-03T21:30:23+08:00"
upvotes: 0
comments: 0
---

# 1799. N次操作后的最大分数和

> **[yiduobo的每日leetcode 1799.N次操作后的最大分数和](https://zhuanlan.zhihu.com/p/463831099) · 知乎 · 2022-02-03 · 赞同 0**
> 力扣：[1799. N次操作后的最大分数和](https://leetcode.cn/problems/maximize-score-after-n-operations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1799.N次操作后的最大分数和

[力扣](https://leetcode-cn.com/problems/maximize-score-after-n-operations/)

没有想出什么特别好的算法，只能老老实实用状态压缩动态规划来做。令f[state]表示选择了数组下标压缩后为state的数字可以得到的最大分数和。

对于f[state]，需要枚举剩余数字当中不属于state的两个数字。设当前枚举的数字的下标分别为i和j，那么加入nums[i]和nums[j]之后state变为了next \= state | (1 \<\< i) | (1 \<\< j)，于是就有

f[next] \= max(f[next], f[state] + gcd(nums[i], nums[j]) \* step)

这里的step等于next中数字的个数除以2

具体实现时，由于每次的next必然都大于state，而且有记录step的需求，因此可以使用类似bfs的做法来进行状态转移，从f[0]开始进行处理，每一轮都将首次出现的next加入到队列当中。

全部处理结束后，f[-1]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        m = len(nums)
        q = [0]
        f = [0] * (1 << m)
        l = 0
        r = 1
        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                for i in range(m - 1):
                    if now & (1 << i) == 0:
                        for j in range(i + 1, m):
                            if now & (1 << j) == 0:
                                next = now | (1 << i) | (1 << j)
                                if f[next] == 0:
                                    q.append(next)

                                x, y = nums[i], nums[j]
                                while x:
                                    x, y = y % x, x
                                f[next] = max(f[next], f[now] + y * step)

            l, r = r, len(q)

        return f[-1]
```
