---
title: "826. 安排工作已达到最大收益"
aliases: ["yiduobo的每日leetcode 826.安排工作已达到最大收益"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344807628"
zhihu_id: "344807628"
zhihu_title: "yiduobo的每日leetcode 826.安排工作已达到最大收益"
question_id: "826"
question: "安排工作以达到最大收益"
problem_url: "https://leetcode.cn/problems/most-profit-assigning-work/"
difficulty: "Medium"
rating: 1709
created: "2021-01-20T22:52:30+08:00"
updated: "2021-01-20T22:52:30+08:00"
upvotes: 0
comments: 0
---

# 826. 安排工作已达到最大收益

> **[yiduobo的每日leetcode 826.安排工作已达到最大收益](https://zhuanlan.zhihu.com/p/344807628) · 知乎 · 2021-01-20 · 赞同 0**
> 力扣：[826. 安排工作以达到最大收益](https://leetcode.cn/problems/most-profit-assigning-work/) · Medium · 灵茶山艾府：[排序+双指针（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

826.安排工作已达到最大收益

[力扣](https://leetcode-cn.com/problems/most-profit-assigning-work/)

由于每份工作可以完成多次，那么对于每个工人而言，最优解就是完成力所能及且收益最大的工作。对于两份工作而言，若完成难度一样，那么收益较低的那一份显然没有必要去做。于是可以先筛除掉这些没必要去做的工作，那么剩下的工作必然满足难度越大，收益越大。

接下来可以将工作按难度从小到大进行排序，然后将工人按工作能力从大到小进行排序。遍历排序后的工人，使用一个变量now表示当前工人能完成的难度最大的工作，那么可以从后往前检测当前工人是否能完成now代表的工作，若不行则将now减一。由于工人的能力是从大到小进行排序的，因此这里的now必然是单调递减的，因此整个匹配工作的过程就是O(n)的。

最后附上python代码：

```python
class Solution(object):
    def maxProfitAssignment(self, difficulty, profit, worker):
        """
        :type difficulty: List[int]
        :type profit: List[int]
        :type worker: List[int]
        :rtype: int
        """

        work = sorted(zip(difficulty, profit), key=lambda d:(d[0], -d[1]))
        valuable_work = [work[0]]
        for index in range(1, len(work)):
            if work[index][1] > valuable_work[-1][1]:
                valuable_work.append(work[index])
        
        now = len(valuable_work) - 1
        res = 0
        for worker_ability in sorted(worker, key=lambda d:-d):
            while now >= 0 and valuable_work[now][0] > worker_ability:
                now -= 1
            if now < 0:
                return res
            res += valuable_work[now][1]
        
        return res
```
