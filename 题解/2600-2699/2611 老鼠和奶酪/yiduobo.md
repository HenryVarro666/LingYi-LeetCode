---
title: "2611. 老鼠和奶酪"
aliases: ["yiduobo的每日leetcode 2611.老鼠和奶酪"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645434974"
zhihu_id: "645434974"
zhihu_title: "yiduobo的每日leetcode 2611.老鼠和奶酪"
question_id: "2611"
question: "老鼠和奶酪"
problem_url: "https://leetcode.cn/problems/mice-and-cheese/"
difficulty: "Medium"
rating: 1663
created: "2023-07-24T02:22:45+08:00"
updated: "2023-07-24T02:22:45+08:00"
upvotes: 0
comments: 0
---

# 2611. 老鼠和奶酪

> **[yiduobo的每日leetcode 2611.老鼠和奶酪](https://zhuanlan.zhihu.com/p/645434974) · 知乎 · 2023-07-24 · 赞同 0**
> 力扣：[2611. 老鼠和奶酪](https://leetcode.cn/problems/mice-and-cheese/) · Medium · 灵茶山艾府：[贪心，最优可以 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2611.老鼠和奶酪

[力扣](https://leetcode.cn/problems/mice-and-cheese/)

对于这类问题，一种常见的处理方法是先假设所有的东西都归其中一人所有，那么在此基础上就某个物品改成分给另一个人的代价就是这两人对于这个物品的价值之差，接下来只需按题目要求选出价值最大或最小的若干件物品就行了。

对于本题，不妨设所有奶酪一开始都分给了第二只老鼠，那么此时的总得分为reward2的总和。接下来遍历每个奶酪，对于第index个奶酪若这个奶酪改为分给第一只老鼠的话，产生的价值之差就是reward1[index] - reward2[index]。题目要求选出k块奶酪给第一只老鼠，那么为了使得答案最大，就应该选择价值差最大的k块奶酪分给第一只老鼠，问题到这里就转化成了给出一个数组，求top k大的数的和。

对于这个问题，可以利用小顶堆来求解。一趟遍历，不断将数组中的数加入到堆中，若堆中的数超过k个，那么就堆顶元素弹出，最后堆中剩下的就是最大的k个数。

最后附上python代码：

```python
class Solution(object):
    def miceAndCheese(self, reward1, reward2, k):
        """
        :type reward1: List[int]
        :type reward2: List[int]
        :type k: int
        :rtype: int
        """

        heap = []
        res = 0
        for v1, v2 in zip(reward1, reward2):
            res += v2
            heapq.heappush(heap, v1 - v2)
            if len(heap) > k:
                heapq.heappop(heap)
            
        return res + sum(heap)
```
