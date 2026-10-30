---
title: "410. 分割数组的最大值"
aliases: ["yiduobo的每日leetcode 410.分割数组的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "题单/二分算法", "题单/动态规划", "题单/二分算法/二-二分答案", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/187591149"
zhihu_id: "187591149"
zhihu_title: "yiduobo的每日leetcode 410.分割数组的最大值"
question_id: "410"
question: "分割数组的最大值"
problem_url: "https://leetcode.cn/problems/split-array-largest-sum/"
difficulty: "Hard"
created: "2020-08-17T23:29:43+08:00"
updated: "2020-08-17T23:29:43+08:00"
upvotes: 0
comments: 0
---

# 410. 分割数组的最大值

> **[yiduobo的每日leetcode 410.分割数组的最大值](https://zhuanlan.zhihu.com/p/187591149) · 知乎 · 2020-08-17 · 赞同 0**
> 力扣：[410. 分割数组的最大值](https://leetcode.cn/problems/split-array-largest-sum/) · Hard · 灵茶山艾府：[二分答案，附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

410.分割数组的最大值<https://leetcode-cn.com/problems/split-array-largest-sum/>

乍一看感觉用动态规划可以做，即使用f[i][j]表示将前i个数分成j个连续子数组时，各自和的最小值是多少。二维的状态一维的转移，因此最终的时间复杂度为O(n^2m)。

不过注意到题目中已经限制了数组中的数都是非空的，那么可以使用二分答案加贪心的思路。

对于数组中连续的一段数nums[l:r]，如果这些数的和小于等于k，那么将其分割成若干个连续子数组之后，由于数组中的数都非负，那么各个子数组的和也必然小于等于k。

到了这里就有了一种做法：设答案为k，然后从数组的头部开始进行划分。每次都尽可能多地将数加入到当前的子数组中，如果无法加入则另起新的子数组。这样划分完毕之后，如果划分出来的子数组数量小于等于m，说明存在某种划分方式使得划分出来的各个子数组最大值小于等于k。二分答案k，然后每次一趟扫描验证答案，最终的时间复杂度为O(nlog(max - min))。

最后附上python代码：

```python
class Solution(object):
    def splitArray(self, nums, m):
        """
        :type nums: List[int]
        :type m: int
        :rtype: int
        """

        l = max(nums)
        r = sum(nums)

        while l < r:
            mid = (l + r) / 2
            cnt = 1
            now = 0
            for num in nums:
                if now + num <= mid:
                    now += num
                else:
                    cnt += 1
                    now = num
            if cnt <= m:
                r = mid
            else:
                l = mid + 1

        return l
```
