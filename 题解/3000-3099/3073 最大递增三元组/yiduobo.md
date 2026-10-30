---
title: "3073. 最大递增三元组"
aliases: ["yiduobo的每日leetcode 3073.最大递增三元组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697566758"
zhihu_id: "697566758"
zhihu_title: "yiduobo的每日leetcode 3073.最大递增三元组"
question_id: "3073"
question: "最大递增三元组"
problem_url: "https://leetcode.cn/problems/maximum-increasing-triplet-value/"
created: "2024-05-13T22:53:19+08:00"
updated: "2024-05-13T22:53:19+08:00"
upvotes: 0
comments: 0
---

# 3073. 最大递增三元组

> **[yiduobo的每日leetcode 3073.最大递增三元组](https://zhuanlan.zhihu.com/p/697566758) · 知乎 · 2024-05-13 · 赞同 0**
> 力扣：[3073. 最大递增三元组](https://leetcode.cn/problems/maximum-increasing-triplet-value/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3073.最大递增三元组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-increasing-triplet-value/)

对于这类三元组问题，常见的思路还是枚举中间元素nums[j]，然后分别找出最优的nums[i]以及nums[k]。

本题依然是枚举nums[j]，由于题目要求nums[i] - nums[j] + nums[k]最大，那么就应该让nums[i]和nums[k]在合法范围内尽量大。

先考虑nums[k]。题目要求满足nums[k] > nums[j]，那么取nums[j + 1]到nums[n - 1]中的最大值作为nums[k]显然是最优的，因为这样既可以尽量满足nums[k] > nums[j]，又可以让最终结果尽可能大。于是在这里从后往前一趟遍历，使用一个数组right记录每个位置及其右侧所有位置中的最大值。另外需要注意的是，当right[j + 1]小于等于nums[j]时，说明j右侧没有比nums[j]大的元素，此时找不到合法的k。

接下来考虑nums[i]。nums[i]的取值同样是越大越好，但是也不能太大，必须要小于nums[j]，也就是说要找出数组前缀nums[0]到nums[j - 1]中最大的，且值位于1到nums[j] - 1之间的数。这是动态的前缀区间最大值问题，与上一题相同，本题依然是适合使用树状数组求解。同样的，本题中的数值取值范围太大，依然要利用数值到序的映射，通过映射建立树状数组求解。

根据上面的结论，就可以先排序后建立数字到序的映射，然后一趟逆序遍历，计算right，最后再一趟顺序遍历枚举nums[j]，一边利用树状数组求解最优的nums[i]，再配合通过right得到的最优的nums[k]来更新答案，然后使用nums[j]及其序更新树状数组并继续向后枚举即可。

最后附上python代码：

```python
class Solution(object):
    def maximumTripletValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mapping = {}
        rank = 1
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = rank
                rank += 1
        
        left = [0] * rank
        right = [nums[-1]]
        for index in range(len(nums) - 2, -1, -1):
            right.append(max(right[-1], nums[index]))
        right.reverse()

        def add(x, v):
            while x < rank:
                left[x] = max(left[x], v)
                x += x & -x
        
        def get(x):
            ma = 0
            while x > 0:
                ma = max(ma, left[x])
                x -= x & -x
            return ma

        add(mapping[nums[0]], nums[0])
        res = 0
        for index in range(1, len(nums) - 1):
            left_ma = get(mapping[nums[index]] - 1)
            if left_ma != 0 and nums[index] < right[index + 1]:
                res = max(res, left_ma - nums[index] + right[index + 1])
            add(mapping[nums[index]], nums[index])

        return res
```
