---
title: "1806. 还原排列的最少操作步数"
aliases: ["yiduobo的每日leetcode 1806.还原排列的最少操作步数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464302270"
zhihu_id: "464302270"
zhihu_title: "yiduobo的每日leetcode 1806.还原排列的最少操作步数"
question_id: "1806"
question: "还原排列的最少操作步数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-reinitialize-a-permutation/"
created: "2022-02-06T14:44:07+08:00"
updated: "2022-02-06T14:44:07+08:00"
upvotes: 0
comments: 0
---

# 1806. 还原排列的最少操作步数

> **[yiduobo的每日leetcode 1806.还原排列的最少操作步数](https://zhuanlan.zhihu.com/p/464302270) · 知乎 · 2022-02-06 · 赞同 0**
> 力扣：[1806. 还原排列的最少操作步数](https://leetcode.cn/problems/minimum-number-of-operations-to-reinitialize-a-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1806.还原排列的最少操作步数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-operations-to-reinitialize-a-permutation/)

由于题目中每个位置的下一个目标位置都是恒定的，那么对于排列中任意位置上的数而言，其在变换若干步之后必然会走回原来的位置，设这个步骤数为k，那么在其变换过程中经过的位置上的数必然也满足变换k轮之后回到原来的位置。

有了这个结论，就只需要一趟遍历，对于每个还没找到这个步长k的位置进行模拟变换直到其回到原位。由于每个位置只会参与一次变换，那么就可以在O(n)的时间复杂度内找出每个位置变换回原位所需的步长，而最终答案很明显就是每个位置变换回原位所需步长的最小公倍数。

最后附上python代码：

```python
class Solution(object):
    def reinitializePermutation(self, n):
        """
        :type n: int
        :rtype: int
        """

        step_list = []
        used = [False] * n
        for num in range(n):
            if not used[num]:
                step = 0
                now = num
                while not used[now]:
                    used[now] = True
                    step += 1
                    now += now
                    if now >= n:
                        now = now - n + 1
                    

                step_list.append(step)
                
        res = 1
        for step in step_list:
            x, y = res, step
            while x:
                x, y = y % x, x
            
            res = res * step / y
        
        return res
```
