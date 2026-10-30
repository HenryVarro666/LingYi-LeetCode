---
title: "1950. 所有子数组最小值中的最大值"
aliases: ["yiduobo的每日leetcode 1950.所有子数组最小值中的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/623891600"
zhihu_id: "623891600"
zhihu_title: "yiduobo的每日leetcode 1950.所有子数组最小值中的最大值"
question_id: "1950"
question: "所有子数组最小值中的最大值"
problem_url: "https://leetcode.cn/problems/maximum-of-minimum-values-in-all-subarrays/"
created: "2023-04-22T03:06:11+08:00"
updated: "2023-04-22T03:06:11+08:00"
upvotes: 0
comments: 0
---

# 1950. 所有子数组最小值中的最大值

> **[yiduobo的每日leetcode 1950.所有子数组最小值中的最大值](https://zhuanlan.zhihu.com/p/623891600) · 知乎 · 2023-04-22 · 赞同 0**
> 力扣：[1950. 所有子数组最小值中的最大值](https://leetcode.cn/problems/maximum-of-minimum-values-in-all-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1950.所有子数组最小值中的最大值

[力扣](https://leetcode.cn/problems/maximum-of-minimum-values-in-all-subarrays/)

题目的数据规模较大，而数组总数是O(n^2)级的，不能直接暴力求解。

不妨从单个数字的角度来考虑。对于数组中的某个数nums[index]，只有当这个数是子数组中的最小值时才会对答案产生影响，因此在这里可以想办法看看nums[index]是哪些子数组的最小值。

令left\[index\]和right\[index\]分别表示index左侧最大的满足nums\[left\[index\]\] \< nums\[index\]以及右侧最小的满足nums\[right\[index\]\] \< nums\[index\]的下标，那么所有左边界在left\[index\] + 1到index之间，右边界在right\[index\] - 1到index之间的子数组中的最小值就都是nums\[index\]。换言之，nums\[index\]将成为某个长度为1、长度为2、...、长度为right\[index\] - left\[index\] - 1的子数组的最小值，从而影响到ans\[0\]、ans\[1\]、...、ans\[right\[index\] - left\[index\] - 2\]的取值。

其中left[index]以及right[index]的求解是经典的单调栈问题，在这里就不展开了。

到了这里，问题就转化成了给出一个数nums[index]以及其影响的区间[0, right[index] - left[index] - 2]，问这些区间合并后每个下标位置上的最大值是多少。虽然涉及到了区间修改，但是由于所有区间的左边界都为1，因此可以使用类似差分数组的处理方法，先使用nums[index]更新区间右边界的最大值，然后从大到小逆序一趟遍历，使用ans[i + 1]来更新ans[i]。

最后附上python代码：

```python
class Solution(object):
    def findMaximums(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        right = [n] * n
        stack = []
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index]:
                right[stack[-1]] = index
                stack.pop()
            stack.append(index)
        

        left = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[index]:
                left[stack[-1]] = index
                stack.pop()
            stack.append(index)

        res = [-1] * n
        for index in range(n):
            length = right[index] - 1 - (left[index] + 1) + 1
            res[length - 1] = max(res[length - 1], nums[index])
            
        for index in range(n - 2, -1, -1):
            res[index] = max(res[index], res[index + 1])
            
        return res
```
