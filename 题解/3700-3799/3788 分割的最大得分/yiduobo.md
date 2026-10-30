---
title: "3788. 分割的最大得分"
aliases: ["yiduobo的每日leetcode 3788.分割的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1988660057483788960"
zhihu_id: "1988660057483788960"
zhihu_title: "yiduobo的每日leetcode 3788.分割的最大得分"
question_id: "3788"
question: "分割的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-of-a-split/"
difficulty: "Medium"
rating: 1306
created: "2025-12-28T17:24:01+08:00"
updated: "2025-12-28T17:24:02+08:00"
upvotes: 1
comments: 0
---

# 3788. 分割的最大得分

> **[yiduobo的每日leetcode 3788.分割的最大得分](https://zhuanlan.zhihu.com/p/1988660057483788960) · 知乎 · 2025-12-28 · 赞同 1**
> 力扣：[3788. 分割的最大得分](https://leetcode.cn/problems/maximum-score-of-a-split/) · Medium · 灵茶山艾府：[前后缀分解，O(1) 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3788.分割的最大得分

[3788. 分割的最大得分 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-score-of-a-split/)

题目给出一个长度为n的整数数组nums。

现在要求在0到n - 2之间找出一个下标index分割数组，对于选择的index

- 令prefixSum(index)表示数组的前缀和，即nums[0] + nums[1] + ... + nums[index]
- 令suffixMin(index)表示数组后缀的最小值，即min(nums[index + 1], nums[index + 2], ..., nums[n - 1])

在index处的分割得分为prefixSum(index) - suffixMin(index)。

问所有合法分割中的最大得分是多少。

根据题目中对prefixSum和suffixMin的定义，只需正反两趟遍历，分别计算这两个数组，然后再枚举分割点index，计算最终答案即可。

另外在具体实现上，由于suffixMin(index)的定义是基于nums[index + 1]开始的后缀，为了方便，在这里可以修改为suffixMin(index)表示的就是nums[index]开始的后缀中的最小值，在计算得分时则需要改成prefixSum(index) - suffixMin(index + 1)。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = [nums[0]]
        for v in nums[1:]:
            s.append(s[-1] + v)
        
        mi = [nums[-1]]
        for v in nums[-2::-1]:
            mi.append(min(mi[-1], v))
        mi.reverse()
        
        res = s[0] - mi[1]
        for index in range(1, len(nums) - 1):
            res = max(res, s[index] - mi[index + 1])
        
        return res
```
