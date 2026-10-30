---
title: "3961. 设备评分的最大和"
aliases: ["yiduobo的每日leetcode 3961.设备评分的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2049536986382332026"
zhihu_id: "2049536986382332026"
zhihu_title: "yiduobo的每日leetcode 3961.设备评分的最大和"
question_id: "3961"
question: "设备评分的最大和"
problem_url: "https://leetcode.cn/problems/maximize-sum-of-device-ratings/"
difficulty: "Medium"
rating: 1880
created: "2026-06-15T22:04:00+08:00"
updated: "2026-06-15T22:04:04+08:00"
upvotes: 2
comments: 0
---

# 3961. 设备评分的最大和

> **[yiduobo的每日leetcode 3961.设备评分的最大和](https://zhuanlan.zhihu.com/p/2049536986382332026) · 知乎 · 2026-06-15 · 赞同 2**
> 力扣：[3961. 设备评分的最大和](https://leetcode.cn/problems/maximize-sum-of-device-ratings/) · Medium · 灵茶山艾府：[把最小值汇集到一起，一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3961.设备评分的最大和

<https://leetcode.cn/problems/maximize-sum-of-device-ratings/>

题目给出一个大小为m \* n的二维整数数组units，其中units[i][j]表示第i个设备中第j个单元的容量，均为正数。每个设备恰好包含n个单元。

设备的评分是其所有单元中的最小容量，设备的。

现在可以执行一下操作任意次(包括零次)：

- 选择一个之前从未被选择过的设备i
- 从i中移除一个单元，并将其添加到任意其他设备中
- 将设备i标记为已选择过

问执行操作后可能得到的最大设备评分之和为多少。

首先可以明确的是，由于units中均为整数，因此当n \= 1时，应该不执行任何操作，此时的答案就是所有的units[index][0]之和。

接下来，当n > 1时，就应该从这m个设备中选出一个接盘，从其他的m - 1个设备中都选出容量最小的那个单元，就这堆拖油瓶都塞给这个接盘的。这样做的理由是评分取决于设备中所有单元的最小容量，因此只有当抛掉最小容量，设备的得分才可能上涨。而对于被抛掉的设备，显然应该几种到一起祸害同一台设备。

基于这一点，就可以遍历每台设备，然后对于当前设备，一趟遍历找出其中容量最小和次小的两台设备，记二者的容量分别为first和second。接下来，first需要收集到一起丢给接盘设备，因此在这台接盘机器的最后得分必然是这些first中的最小值。另一方面，这台接盘机器将会损失掉自身的原始得分，即对应的second。为了使得最终得分综合最大，在这里就应该选择second最小的那台机器来接盘，因此在这里还需要记录这些second中的最小值，同时将这些second累加到最终的答案中。

全部遍历完成后，先将最终答案减去最小的second，然后加上最小的first，表示选择了second最小的那台设备接盘。

最后附上python代码：

```python
class Solution(object):
    def maxRatings(self, units):
        """
        :type units: List[List[int]]
        :rtype: int
        """

        m = len(units)
        if len(units[0]) == 1:
            return sum([units[index][0] for index in range(m)])

        mi_first = None
        mi_second = None

        res = 0
        for index in range(m):
            first = None
            second = None
            for v in units[index]:
                if first is None or first > v:
                    first, second = v, first
                elif second is None or second > v:
                    second = v
        
            if mi_first is None or mi_first > first:
                mi_first = first
            if mi_second is None or mi_second > second:
                mi_second = second
            res += second
        
        return res - mi_second + mi_first
```
