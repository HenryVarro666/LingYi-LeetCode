---
title: "1793. 好子数组的最大分数"
aliases: ["yiduobo的每日leetcode 1793.好子数组的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/two-pointers", "leetcode/monotonic-stack", "题单/滑动窗口与双指针", "题单/单调栈", "题单/滑动窗口与双指针/三-单序列双指针", "题单/单调栈/二-矩形"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463536849"
zhihu_id: "463536849"
zhihu_title: "yiduobo的每日leetcode 1793.好子数组的最大分数"
question_id: "1793"
question: "好子数组的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-score-of-a-good-subarray/"
difficulty: "Hard"
rating: 1946
created: "2022-02-01T22:55:19+08:00"
updated: "2022-02-01T22:55:19+08:00"
upvotes: 0
comments: 0
---

# 1793. 好子数组的最大分数

> **[yiduobo的每日leetcode 1793.好子数组的最大分数](https://zhuanlan.zhihu.com/p/463536849) · 知乎 · 2022-02-01 · 赞同 0**
> 力扣：[1793. 好子数组的最大分数](https://leetcode.cn/problems/maximum-score-of-a-good-subarray/) · Hard · 灵茶山艾府：[两种方法：单调栈/双指针（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1793.好子数组的最大分数

[力扣](https://leetcode-cn.com/problems/maximum-score-of-a-good-subarray/)

由于好子数组的分数计算方式取决于数组中的最小值以及长度，那么在想办法确定了候选答案数组中的最小值之和，就需要尽可能扩展数组的长度。

注意到题目要求数组中包含nums[k]，那么一个自然的想法就是使用两个指针l和r，从k - 1和k + 1开始分别向左右两侧扩展。方便起见，设当前扩展出来的数组中最小值为mi，此时扩展出来的边界为l和r，接下来需要考察nums[l - 1]以及nums[r + 1]：

1、nums[l - 1] >\= mi或nums[r + 1] >\= mi：

此时扩展数组不会影响mi，但是能扩展数组的长度，因此应该将l和r都向外扩展，同时更新答案。

2、nums[l - 1] \= nums[r + 1] \< mi：

此时如果选择扩展一边，那么也应该扩展另一边，至于先后顺序则无关紧要。扩展后需要同时更新mi以及答案。

3、nums[l - 1] \< nums[r + 1] \< mi：

可以证明，如果最终答案的右边界为r，即没有选择nums[r + 1]的话，那么其左边界也必然大于l - 1。具体可以使用反证法：若最终答案的右边界为r，左边界l' \<\= l - 1，那么答案中的最小值mi必然小于等于nums[l - 1]。由于nums[r + 1] > nums[l - 1]，那么此时将nums[r + 1]加入到答案中必然是更优的，产生了矛盾。

根据上面的结论，在这种情况下就应该选择将r向右扩展，同时更新mi以及答案。

4、nums[r + 1] \< nums[l + 1] \< mi：

与情况3对称，此时就应该选择将l向左扩展，同时更新mi以及答案。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = mi = nums[k]
        l = k - 1
        r = k + 1
        n = len(nums)
        while l >= 0 and r < n:
            if nums[l] > nums[r]:
                if nums[l] < mi:
                    mi = nums[l]
                res = max(res, mi * (r - l))
                l -= 1
            else:
                if nums[r] < mi:
                    mi = nums[r]
                res = max(res, mi * (r - l))
                r += 1

        while l >= 0:
            if nums[l] < mi:
                mi = nums[l]
            res = max(res, mi * (r - l))
            l -= 1
        
        while r < n:
            if nums[r] < mi:
                mi = nums[r]
            res = max(res, mi * (r - l))
            r += 1
        
        return res
```
