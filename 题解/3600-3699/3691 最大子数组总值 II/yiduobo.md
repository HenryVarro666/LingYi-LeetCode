---
title: "3691. 最大子数组总值II"
aliases: ["yiduobo的每日leetcode 3691.最大子数组总值II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/binary-search", "leetcode/sliding-window", "leetcode/monotonic-queue", "leetcode/monotonic-stack", "leetcode/heap-priority-queue", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1955351878796830330"
zhihu_id: "1955351878796830330"
zhihu_title: "yiduobo的每日leetcode 3691.最大子数组总值II"
question_id: "3691"
question: "最大子数组总值 II"
problem_url: "https://leetcode.cn/problems/maximum-total-subarray-value-ii/"
difficulty: "Hard"
rating: 2469
created: "2025-09-29T21:35:38+08:00"
updated: "2025-09-29T21:35:38+08:00"
upvotes: 2
comments: 0
---

# 3691. 最大子数组总值II

> **[yiduobo的每日leetcode 3691.最大子数组总值II](https://zhuanlan.zhihu.com/p/1955351878796830330) · 知乎 · 2025-09-29 · 赞同 2**
> 力扣：[3691. 最大子数组总值 II](https://leetcode.cn/problems/maximum-total-subarray-value-ii/) · Hard · 灵茶山艾府：[两种方法：ST 表 + 最大堆 / 二分 + Lazy 线段树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3691.最大子数组总值II

<https://leetcode.cn/problems/maximum-total-subarray-value-ii/description/>

题目给出一个长度为n的整数数组nums以及一个整数k，其中n不超过50000，k不超过100000。现在要求从nums中选出恰好k个非空子数组，这些子数组可以重叠，同一个子数组只能被选择一次。

对于一个子数组，其值被定义为子数组中最大值与最小值之差。

问选出的k个子数组的值之和最大可能是多少。

之前3689题的加强版。本题中每个子数组只能被使用一次，那么就不能再沿用之前的处理方法了。

对于这类第k大值相关的问题，如果直接计算第k大值比较困难的话，一种可能的处理方法就是二分这个第k大值，将问题转化为对于当前二分到的mid，判断是否存在至少k个子数组，其值大于等于mid。

另一方面，对于一个固定了左边界的子数组而言，且右边界越大，子数组中的最大值就最大，最小值就越小，也就是说这个子数组的值就越大。基于这一点，就可以利用变长滑动窗口，计算出对于每个特定的左边界index，最小的，且满足子数组值大于等于mid的右边界p，那么左边界为index，右边界在p到n - 1之间的所有子数组的值都将大于等于mid，这样一来就可以很方便的统计值大于等于mid的子数组数目，然后更新二分的上下界了。

---

接下来需要处理的问题就是如何通过滑动窗口找出每个左边界对应的最小右边界。这个问题实际上就是滑动窗口最大/最小值问题，可以使用堆或者单调队列来进行处理。我在这里使用的是后者。

接下来以最大值来进行说明。单调队列成立的前提是对于窗口内的两个下标i和j，若i \< j且nums[i] \< nums[j]，那么nums[i]就不可能再成为窗口内的最大值了，因为nums[i]会先于nums[j]被移出窗口的左边界，也就是说窗口内始终存在nums[j]这个大于nums[i]的元素。基于这一点，nums[i]就不可能成为窗口内的最大值了。

更进一步的，需要保留下来的元素必然是单调递减的，因此在这里就可以使用单调队列来维护窗口内可能成为最大值的元素。另一方面，由于窗口左边界会不断向右滑动，因此队列中最左侧的元素可能会过期，此时需要将其从队列中弹出，这也是使用单调队列而不是单调栈的理由。

---

到了这里，就可以利用滑动窗口配合单调队列计算出每个左边界对应的最小右边界，然后计算出值大于等于mid的子数组数目，从而通过二分法找到第k大的子数组的值v。

接下来还需要想办法计算出前k大的子数组的值之和。通过上面滑动窗口配合单调队列的方法，只能计算出值大于等于v的子数组的数目，如果想计算具体的子数组值之和，还需要从最小的右边界开始向后遍历，具体计算每个子数组的值然后累加。这样做的话有一个问题就是可能存在非常多的值恰好等于v的子数组，这样一来时间复杂度就非常高了。

一种可行的处理方法是将界限往上抬一抬，通过上面的方法，计算出对于每个左边界，可以使得值大于等于v + 1的最小右边界，然后再暴力计算所有的子数组值之和。由于题目中的k不超过100000，而值大于等于v + 1的子数组数目必然小于k，因此在这里暴力计算是完全没问题的。计算完值大于等于v + 1的子数组值之和后，还需要使用值恰好为v的子数组值来补足题目要求的k。对于这个问题，只需要在上面计算过程中统计值大于等于v + 1的的子数组数目cnt，然后将剩下的(k - cnt)个值恰好为v的子数组值累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def maxTotalValue(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        right = max(nums) - min(nums)
        left = 0
        while left < right:
            mid = (left + right + 1) // 2
            p = 0
            cnt = 0
            ma = deque()
            mi = deque()
            for index, v in enumerate(nums):
                while p < len(nums) and (not ma or nums[ma[0]] - nums[mi[0]] < mid):
                    while ma and nums[p] > nums[ma[-1]]:
                        ma.pop()
                    ma.append(p)

                    while mi and nums[p] < nums[mi[-1]]:
                        mi.pop()
                    mi.append(p)

                    p += 1

                if not ma or nums[ma[0]] - nums[mi[0]] < mid:
                    break

                cnt += len(nums) - p + 1
                if cnt >= k:
                    break
                
                if ma and ma[0] == index:
                    ma.popleft()
                if mi and mi[0] == index:
                    mi.popleft()
            
            if cnt >= k:
                left = mid
            else:
                right = mid - 1

        res = 0
        p = 0
        cnt = 0
        ma = deque()
        mi = deque()
        for index, v in enumerate(nums):
            while p < len(nums) and (not ma or nums[ma[0]] - nums[mi[0]] < left + 1):
                while ma and nums[p] > nums[ma[-1]]:
                    ma.pop()
                ma.append(p)

                while mi and nums[p] < nums[mi[-1]]:
                    mi.pop()
                mi.append(p)

                p += 1
            
            if not ma or nums[ma[0]] - nums[mi[0]] < left + 1:
                break

            res += nums[ma[0]] - nums[mi[0]]
            cnt += 1
            q = p
            rest_ma = nums[ma[0]]
            rest_mi = nums[mi[0]]
            while q < len(nums):
                rest_ma = max(rest_ma, nums[q])
                rest_mi = min(rest_mi, nums[q])
                res += rest_ma - rest_mi
                cnt += 1
                q += 1

            if ma and ma[0] == index:
                ma.popleft()
            if mi and mi[0] == index:
                mi.popleft()

        return res + (k - cnt) * left
```
