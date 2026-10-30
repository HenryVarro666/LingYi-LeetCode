---
title: "LCP 30. 魔塔游戏"
aliases: ["yiduobo的每日leetcode LCP30.魔塔游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574011354"
zhihu_id: "574011354"
zhihu_title: "yiduobo的每日leetcode LCP30.魔塔游戏"
question_id: "LCP 30"
question: "魔塔游戏"
problem_url: "https://leetcode.cn/problems/p0NxJO/"
difficulty: "Medium"
rating: 1900
created: "2022-10-16T01:03:44+08:00"
updated: "2022-10-16T01:03:44+08:00"
upvotes: 0
comments: 0
---

# LCP 30. 魔塔游戏

> **[yiduobo的每日leetcode LCP30.魔塔游戏](https://zhuanlan.zhihu.com/p/574011354) · 知乎 · 2022-10-16 · 赞同 0**
> 力扣：[LCP 30. 魔塔游戏](https://leetcode.cn/problems/p0NxJO/) · Medium · 灵茶山艾府：[反悔贪心（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP30.魔塔游戏

[力扣](https://leetcode.cn/problems/p0NxJO/)

首先，题目要求所有房间都走到，因此可以先计算nums的和。若这个和为负数，那么无论怎么调整顺序，最终的血量都小于等于0，无法走完全程，此时直接返回-1。

接下来开始遍历nums，并使用一个变量now表示当前的血量。

若当前的nums[index]为正，那么无条件将其加入到now当中。反过来，如果将nums[index]加入到now中之后now小于等于0，那么就需要将之前使用过的某个负的nums[k]移动到最后再去访问。在这里显然应该移动负的最多的那个，因为在相同的操作次数下保有的血量是最多的。

那么一个自然的想法就是使用一个堆来维护当前访问过的负数房间。每遍历到一个负的nums[index]，先尝试将其累加到now中，同时将其加入到堆中。若此时的now小于等于0，那么就需要移动一个负的房间到末尾，此时只需要将堆顶从now中删去就行了，并不需要执行真的移动操作，因为走到末尾时血量一定是充足的。

最后附上python代码：

```python
class Solution(object):
    def magicTower(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if sum(nums) < 0:
            return -1

        heap = []
        now = 1
        res = 0
        for num in nums:
            now += num
            if num < 0:
                heapq.heappush(heap, num)
                if now <= 0:
                    now -= heapq.heappop(heap)
                    res += 1
        
        return res
```
