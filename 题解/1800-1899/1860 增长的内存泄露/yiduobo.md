---
title: "1860. 增长的内存泄漏"
aliases: ["yiduobo的每日leetcode 1860.增长的内存泄漏"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/473004542"
zhihu_id: "473004542"
zhihu_title: "yiduobo的每日leetcode 1860.增长的内存泄漏"
question_id: "1860"
question: "增长的内存泄露"
problem_url: "https://leetcode.cn/problems/incremental-memory-leak/"
difficulty: "Medium"
created: "2022-02-26T23:24:27+08:00"
updated: "2022-02-26T23:24:27+08:00"
upvotes: 0
comments: 0
---

# 1860. 增长的内存泄漏

> **[yiduobo的每日leetcode 1860.增长的内存泄漏](https://zhuanlan.zhihu.com/p/473004542) · 知乎 · 2022-02-26 · 赞同 0**
> 力扣：[1860. 增长的内存泄露](https://leetcode.cn/problems/incremental-memory-leak/) · Medium · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1860.增长的内存泄漏

[力扣](https://leetcode-cn.com/problems/incremental-memory-leak/)

题目的数据规模看上去很大，但是注意到每一时刻消耗的内存是逐步增大的，那么到了k时刻，一共消耗的内存就是(1 + k) \* k / 2。极限情况下，不妨设两块内存条的空间都是最大的，即2^31 - 1，那么不考虑因为内存分配问题导致的浪费，满打满算的话就是

(1 + k) \* k / 2 >\= 2^32 - 2

那么这里k必然小于sqrt(2) \* 2^16，还不到50000，也就是说在50000秒能必然会以为退出。那么在这里完全可以从第1秒开始模拟整个分配的过程，直到没有可用的内存空间为止。

最后附上python代码：

```python
class Solution(object):
    def memLeak(self, memory1, memory2):
        """
        :type memory1: int
        :type memory2: int
        :rtype: List[int]
        """

        now = 1
        while now <= max(memory1, memory2):
            if memory1 < memory2:
                memory2 -= now
            else:
                memory1 -= now
            now += 1
        
        return [now, memory1, memory2]
```
