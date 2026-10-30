---
title: "313. 超级丑数"
aliases: ["yiduobo的每日leetcode 313.超级丑数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158891100"
zhihu_id: "158891100"
zhihu_title: "yiduobo的每日leetcode 313.超级丑数"
question_id: "313"
question: "超级丑数"
problem_url: "https://leetcode.cn/problems/super-ugly-number/"
created: "2020-07-12T13:20:21+08:00"
updated: "2020-07-12T13:20:21+08:00"
upvotes: 0
comments: 0
---

# 313. 超级丑数

> **[yiduobo的每日leetcode 313.超级丑数](https://zhuanlan.zhihu.com/p/158891100) · 知乎 · 2020-07-12 · 赞同 0**
> 力扣：[313. 超级丑数](https://leetcode.cn/problems/super-ugly-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

313.超级丑数<https://leetcode-cn.com/problems/super-ugly-number/>

264题的升级版（传送门在这里[yiduobo：yiduobo的每日leetcode 264.丑数II](https://zhuanlan.zhihu.com/p/151845284)）。

可以完全沿用264题的做法，每次取出当前最小的丑数，然后分别与primes中的元素相乘，得到的结果去重后分别加入对应的队列，然后从各个队列的队首选取最小的一个重复上述步骤直到产生出第n个超级丑数为止。

一共需要进行n轮操作，每轮生成丑数需要k次乘法，获取各个队列中最小的队首元素也需要k比较，使用堆的话则是logk次，因此最终的时间复杂度还是O(nk)。

最后附上python代码：

```python
class Solution(object):

    def nthSuperUglyNumber(self, n, primes):
        """
        :type n: int
        :type primes: List[int]
        :rtype: int
        """

        if n == 1:
            return 1

        heap = []
        for index, prime in enumerate(primes):
            heappush(heap, (prime, index))

        candidate_list = [[] for _ in range(len(primes))]
        pos_list = [0] * len(primes)
        used = set()

        for step in range(1, n):
            now, candidate_index = heappop(heap)
            for index, prime in enumerate(primes):
                next_candidate = prime * now
                if next_candidate not in used:
                    used.add(next_candidate)
                    candidate_list[index].append(next_candidate)

            if pos_list[candidate_index] < len(candidate_list[index]):
                heappush(heap, (candidate_list[candidate_index][pos_list[candidate_index]], candidate_index))
                pos_list[candidate_index] += 1

        return now
```
