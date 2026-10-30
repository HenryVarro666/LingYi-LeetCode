---
title: "2420. 找到所有好下标"
aliases: ["yiduobo的每日leetcode 2420.找到所有好下标"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569864627"
zhihu_id: "569864627"
zhihu_title: "yiduobo的每日leetcode 2420.找到所有好下标"
question_id: "2420"
question: "找到所有好下标"
problem_url: "https://leetcode.cn/problems/find-all-good-indices/"
difficulty: "Medium"
rating: 1695
created: "2022-10-01T00:59:15+08:00"
updated: "2022-10-01T00:59:15+08:00"
upvotes: 0
comments: 0
---

# 2420. 找到所有好下标

> **[yiduobo的每日leetcode 2420.找到所有好下标](https://zhuanlan.zhihu.com/p/569864627) · 知乎 · 2022-10-01 · 赞同 0**
> 力扣：[2420. 找到所有好下标](https://leetcode.cn/problems/find-all-good-indices/) · Medium · 灵茶山艾府：[递推 + 枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2420.找到所有好下标

[力扣](https://leetcode.cn/problems/find-all-good-indices/)

对于这类问题，通常的做法是枚举中间的位置，然后检测两侧是否符合要求。对于本题，恰好就是枚举好下标的位置，然后检测左右两侧的k个元素是否是非递增和非递减的。

在这里可以先预处理出两个数组left和right，其中left[index]表示以nums[index]结尾的最长非递增子数组的长度，相对的，right[index]则表示以nums[index]开头的最长非递减子数组的长度。对于left和right的求解，则可以正反两趟遍历利用上一个位置的值来更新当前位置的值。

得到left和right后，只需要枚举所有的中间下标index，然后判断left[index - 1]和right[index + 1]是否都大于等于k即可。

最后附上python代码：

```python
class Solution(object):
    def goodIndices(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        n = len(nums)
        left = [1]
        for index in range(1, n):
            if nums[index] <= nums[index - 1]:
                left.append(left[-1] + 1)
            else:
                left.append(1)
        
        right = [1]
        for index in range(n - 2, -1, -1):
            if nums[index] <= nums[index + 1]:
                right.append(right[-1] + 1)
            else:
                right.append(1)
        right.reverse()

        res = []
        for index in range(k, n - k):
            if left[index - 1] >= k and right[index + 1] >= k:
                res.append(index)
        
        return res
```
