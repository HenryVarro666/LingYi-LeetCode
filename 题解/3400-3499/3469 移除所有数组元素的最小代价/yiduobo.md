---
title: "3469. 移除所有数组元素的最小代价"
aliases: ["yiduobo的每日leetcode 3469.移除所有数组元素的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1896332567302631882"
zhihu_id: "1896332567302631882"
zhihu_title: "yiduobo的每日leetcode 3469.移除所有数组元素的最小代价"
question_id: "3469"
question: "移除所有数组元素的最小代价"
problem_url: "https://leetcode.cn/problems/find-minimum-cost-to-remove-array-elements/"
difficulty: "Medium"
rating: 2112
created: "2025-04-17T22:55:11+08:00"
updated: "2025-04-17T22:55:11+08:00"
upvotes: 0
comments: 0
---

# 3469. 移除所有数组元素的最小代价

> **[yiduobo的每日leetcode 3469.移除所有数组元素的最小代价](https://zhuanlan.zhihu.com/p/1896332567302631882) · 知乎 · 2025-04-17 · 赞同 0**
> 力扣：[3469. 移除所有数组元素的最小代价](https://leetcode.cn/problems/find-minimum-cost-to-remove-array-elements/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3469.移除所有数组元素的最小代价

[3469. 移除所有数组元素的最小代价 - 力扣（LeetCode）](https://leetcode.cn/problems/find-minimum-cost-to-remove-array-elements/description/)

题目给出一个整数数组nums，要求对nums执行若干次操作，直到nums为空。每次操作中，需要从nums的前三个元素中选择任意两个元素并移除它们，代价为移除的两个元素中的较大值。若nums剩余元素不足三个，则移除所有剩余元素，代价为剩余元素中的最大值。

问移除所有元素所需的最小成本。

首先可以明确的是，在进行了rnd轮移除操作后，第0到第rnd \* 2这一共rnd \* 2 + 1个元素中将被移除掉rnd \* 2个元素，只剩下唯一的一个。另一方面，在rnd轮移除操作后，由于前rnd \* 2 + 1个元素参与了移除操作，那么除了剩下的那一个元素之外，nums中排第二和第三的元素就应该是原始nums中的第rnd \* 2 + 2以及rnd \* 2 + 3个元素，对应的下标分别为rnd \* 2 + 1以及rnd \* 2 + 2。

可以发现，只需要保留操作的轮次rnd以及剩余元素的下标pre，就可以唯一确定下一轮操作时参与操作的三个元素是什么，于是可以令f[r][pre]表示已经经过了r轮操，剩下元素的下标为pre时，还需要多少代价才能使得nums变为空数组。那么对于f[r][pre]，记x \= r \* 2 + 1，y \= r \* 2 + 2，也就是上面讨论中的当前nums中排第二和第三的元素在原始nums中的下标，有：

1、若x >\= n：

说明经过r轮操作后nums中仅留下nums[pre]这一个元素，此时应该将其删除，代价为nums[pre]

2、若y >\= n：

说明此时nums中还剩下nums[pre]以及nums[x]，此时应该将这两个元素都删除，代价为max(nums[pre], nums[x])

3、其他情况下，按照正常的三选二进行删除。

选择删除nums[x]和nums[y]时，有f[r][pre] \=f[r + 1][pre] + max(nums[x], nums[y])

选择删除nums[x]和nums[pre]时，有f[r][pre] \= f[r + 1][y] + max(nums[x], nums[pre])

选择删除nums[y]和nums[pre]时，有f[r][pre] \= f[r + 1][x] + max(nums[y], nums[pre])

取上面三者的最小值作为最终的f[r][pre]即可

在具体实现上，应该先计算出总的操作轮次rnd，然后对nums进行倒推，先计算后面轮次对应的f值再计算前面轮次对应的f值。我在这里选择用记忆化搜索来实现，写起来相对方便点。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        rnd = (n - 1) // 2 + 1
        if (n - 1) % 2 == 0:
            rnd += 1

        f = [[None] * n for _ in range(rnd)]

        def calc(r, pre, f):
            if f[r][pre] is None:
                x = r * 2 + 1
                y = r * 2 + 2
                if x >= n:
                    f[r][pre] = nums[pre]
                elif y >= n:
                    f[r][pre] = max(nums[pre], nums[x])
                else:
                    f[r][pre] = min(calc(r + 1, pre, f) + max(nums[x], nums[y]), \
                                    calc(r + 1, y, f) + max(nums[x], nums[pre]), \
                                    calc(r + 1, x, f) + max(nums[y], nums[pre]))
            
            return f[r][pre]
        
        return calc(0, 0, f)
```
