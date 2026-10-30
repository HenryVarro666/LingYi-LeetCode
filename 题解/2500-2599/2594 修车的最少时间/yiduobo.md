---
title: "2594. 修车的最少时间"
aliases: ["yiduobo的每日leetcode 2594.修车的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/shi-pin", "leetcode/ti-dan", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643827074"
zhihu_id: "643827074"
zhihu_title: "yiduobo的每日leetcode 2594.修车的最少时间"
question_id: "2594"
question: "修车的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-repair-cars/"
difficulty: "Medium"
rating: 1915
created: "2023-07-16T00:04:15+08:00"
updated: "2023-07-16T00:04:15+08:00"
upvotes: 0
comments: 0
---

# 2594. 修车的最少时间

> **[yiduobo的每日leetcode 2594.修车的最少时间](https://zhuanlan.zhihu.com/p/643827074) · 知乎 · 2023-07-16 · 赞同 0**
> 力扣：[2594. 修车的最少时间](https://leetcode.cn/problems/minimum-time-to-repair-cars/) · Medium · 灵茶山艾府：[二分答案+优化（附题单！）Python/Java/C++/Go/JS](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2594.修车的最少时间

[力扣](https://leetcode.cn/problems/minimum-time-to-repair-cars/)

修车的时间越长，就有越多的车可以被修好，也就是说本题可以通过二分答案来求解。

对于当前二分到的时间mid，遍历所有的修车工人。对于能力值为r的工人，其在mid分钟内能修好的车的数目为sqrt(mid / r)，将这个值累加到mid分钟能修好的车的总量cnt中。遍历完成后，若cnt大于等于cars，说明时间足够，此时应该更新二分上界为mid，否则更新二分下界为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def repairCars(self, ranks, cars):
        """
        :type ranks: List[int]
        :type cars: int
        :rtype: int
        """

        n = len(ranks)

        left = 1
        right = (cars / n + 1) ** 2 * max(ranks)
        while left < right:
            mid = (left + right) / 2
            cnt = 0
            for r in ranks:
                cnt += int(sqrt(mid * 1.0 / r))
            
            if cnt >= cars:
                right = mid
            else:
                left = mid + 1
        
        return left
```
