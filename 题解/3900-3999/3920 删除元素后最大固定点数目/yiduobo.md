---
title: "3920. 删除元素后最大固定点数目"
aliases: ["yiduobo的每日leetcode 3920.删除元素后最大固定点数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2035011888522728910"
zhihu_id: "2035011888522728910"
zhihu_title: "yiduobo的每日leetcode 3920.删除元素后最大固定点数目"
question_id: "3920"
question: "删除元素后最大固定点数目"
problem_url: "https://leetcode.cn/problems/maximize-fixed-points-after-deletions/"
difficulty: "Hard"
rating: 2264
created: "2026-05-06T22:21:36+08:00"
updated: "2026-05-06T22:21:37+08:00"
upvotes: 0
comments: 0
---

# 3920. 删除元素后最大固定点数目

> **[yiduobo的每日leetcode 3920.删除元素后最大固定点数目](https://zhuanlan.zhihu.com/p/2035011888522728910) · 知乎 · 2026-05-06 · 赞同 0**
> 力扣：[3920. 删除元素后最大固定点数目](https://leetcode.cn/problems/maximize-fixed-points-after-deletions/) · Hard · 灵茶山艾府：[最长递增子序列（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3920.删除元素后最大固定点数目

<https://leetcode.cn/problems/maximize-fixed-points-after-deletions/description/>

题目给出一个整数数组nums。

若nums[index] \= index，则称index位固定点。

现在可以从nums中删除任意个元素，在每次删除后，剩余的元素向左移动，并且下标从0开始重新分配。

要求返回执行任意次数的删除操作后，可以获得的最大固定点数量。

首先可以明确的是，对于下标index的元素v，只有当v \<\= index时，其才可能成为固定点。这里也很好理解，例如对于处于下标1的元素2，其下标是不可能变为2的。

根据这个限制，先对nums进行一趟遍历，从中选出所有满足条件的元素，形成二元组(v, delta)加入到候选数组candidate中，其中delta为index - v，也就是将v移动到固定点所需的删除下标0到index - 1之间的元素数量。

接下来，目标就是从candidate中选出尽量多的元素，这些元素首先需要满足v这一项是单调递增的。经过分析可以发现，这些选出的元素的delta必然是单调不减的，因为靠前的元素如果移除掉了太多的前缀元素，那么后续的元素就已经被移动到目标位置左侧，移动不回来了。

基于这一点，问题就变成了从candidate中选出一个尽量长的，一个维度上单调递增，另一个维度上单调不减的子序列。对于这个问题，可以将candidate按照v为第一关键字从小到大，delta为第二关键字从大到小进行排序，排序完成后对delta计算最长不减子序列就行了。这样做的理由是经过排序candidate中，所有非递减的delta序列对应的v序列必然是单调递增的。

最后附上python代码：

```python
class Solution(object):
    def maxFixedPoints(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        candidate = []
        for index, v in enumerate(nums):
            if v <= index:
                candidate.append((v, index - v))

        candidate.sort(key=lambda d:(d[0], -d[1]))

        f = []
        for _, delta in candidate:
            if not f or delta >= f[-1]:
                f.append(delta)
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right) // 2
                    if f[mid] <= delta:
                        left = mid + 1
                    else:
                        right = mid

                f[left] = delta

        return len(f)
```
