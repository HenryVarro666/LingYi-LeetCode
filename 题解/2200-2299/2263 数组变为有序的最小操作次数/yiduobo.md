---
title: "2263. 数组变为有序的最小操作次数"
aliases: ["yiduobo的每日leetcode 2263.数组变为有序的最小操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/628736370"
zhihu_id: "628736370"
zhihu_title: "yiduobo的每日leetcode 2263.数组变为有序的最小操作次数"
question_id: "2263"
question: "数组变为有序的最小操作次数"
problem_url: "https://leetcode.cn/problems/make-array-non-decreasing-or-non-increasing/"
created: "2023-05-12T00:37:43+08:00"
updated: "2023-05-12T00:37:43+08:00"
upvotes: 0
comments: 0
---

# 2263. 数组变为有序的最小操作次数

> **[yiduobo的每日leetcode 2263.数组变为有序的最小操作次数](https://zhuanlan.zhihu.com/p/628736370) · 知乎 · 2023-05-12 · 赞同 0**
> 力扣：[2263. 数组变为有序的最小操作次数](https://leetcode.cn/problems/make-array-non-decreasing-or-non-increasing/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2263.数组变为有序的最小操作次数

[力扣](https://leetcode.cn/problems/make-array-non-decreasing-or-non-increasing/)

题目要求找出将数组变为单调不增或者单调不减的最少操作次数。对于单调不增，可以认为是将数组从后往前变为单调不减，因此实际上只需要找出将数组变为单调不减的最少操作次数，正向求解后只需将数组翻转再次求解，就得到了将数组变为单调不增的最少操作次数。

接下来考虑如何使用最少的次数将数组变为单调不减。

题目中数值的取值范围不大，因此可以将其加入到状态表示中，利用动态规划来求解。令f[i][j]表示将前i个数变为单调不减，且最后这个数值为j时所需的最少操作次数，那么对于f[i][j]，就有

f[i][j] \= min(f[i - 1][k]) + abs(j - nums[i])，其中k需要满足0 \<\= k \<\= j

这是绝对值函数的累加，属于凸函数单调性优化的题目，与之前的LCP59类似

[yiduobo：yiduobo的每日leetcode LCP59.搭桥过河](https://zhuanlan.zhihu.com/p/578857297)

那么同样可以使用堆来维护函数图像斜率的变化位置，不过这里情况有简单得多。对于每一轮的nums[i]，若其大于等于上一轮的最优区间的左边界，那么nums[i]就是本轮的最优取值位置，此时只需将nums[i]也加入到堆中即可。反之，若其小于上一轮最优区间的左边界，那么本轮的最优取值区间就是nums[i]到上一轮最优区间的左边界之间，此时函数图像中斜率为-2的位置为nums[i]，而不存在斜率为-1的线段，因此需要从堆中弹出堆顶元素，然后加入两次nums[i]，同时将上一轮最优区间的左边界减去x累加到答案中。

本题的优化有些难以理解，可以进一步参考一下LCP59中关于维护斜率相关的部分。

最后附上python代码：

```python
class Solution(object):
    def convertArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        
        def calc():
            heap = []
            res = 0

            for x in nums:
                if not heap:
                    heap.append(-x)
                else:
                    best = -heap[0]

                    if x < best:
                        heapq.heappop(heap)
                        heapq.heappush(heap, -x)
                        heapq.heappush(heap, -x)
                        res += best - x
                    else:
                        heapq.heappush(heap, -x)

            return res

        v1 = calc()
        nums.reverse()
        v2 = calc()
        return min(v1, v2)
```
