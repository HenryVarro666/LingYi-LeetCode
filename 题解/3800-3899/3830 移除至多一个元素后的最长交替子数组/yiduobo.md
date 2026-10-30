---
title: "3830. 移除至多一个元素后的最长交替子数组"
aliases: ["yiduobo的每日leetcode 3830.移除至多一个元素后的最长交替子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/六-分组循环", "题单/动态规划/六-状态机-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2002219588172128661"
zhihu_id: "2002219588172128661"
zhihu_title: "yiduobo的每日leetcode 3830.移除至多一个元素后的最长交替子数组"
question_id: "3830"
question: "移除至多一个元素后的最长交替子数组"
problem_url: "https://leetcode.cn/problems/longest-alternating-subarray-after-removing-at-most-one-element/"
difficulty: "Hard"
rating: 2162
created: "2026-02-06T03:54:39+08:00"
updated: "2026-02-06T03:54:42+08:00"
upvotes: 1
comments: 0
---

# 3830. 移除至多一个元素后的最长交替子数组

> **[yiduobo的每日leetcode 3830.移除至多一个元素后的最长交替子数组](https://zhuanlan.zhihu.com/p/2002219588172128661) · 知乎 · 2026-02-06 · 赞同 1**
> 力扣：[3830. 移除至多一个元素后的最长交替子数组](https://leetcode.cn/problems/longest-alternating-subarray-after-removing-at-most-one-element/) · Hard · 灵茶山艾府：[三种方法：前后缀分解 / 分组循环 / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3830.移除至多一个元素后的最长交替子数组

<https://leetcode.cn/problems/longest-alternating-subarray-after-removing-at-most-one-element/description/>

题目给出一个整数数组nums。

若一个从left开始到right的子数组满足以下条件之一，就称其为交替子数组：

- nums[left] \< nums[left + 1] > nums[left + 2] \< nums[left + 3] > ...
- nums[left] > nums[left + 1] \< nums[left + 2] > nums[left + 3] \< ...

换言之，比较子数组中的相邻元素，这些比较在严格大于和严格小于之间交替进行，则该子数组是交替的。

现在可以从数组中移除至多一个元素，问可以得到的最长交替子数组的长度是多少。

长度为1的子数组认为是交替的。

题目中的交替子数组可以理解成按照 波峰-波谷-波峰-波谷-... 或者 波谷-波峰-波谷-波峰-... 排布的子数组，那么在不移除元素的情况下，可以一趟遍历直接计算出最长的交替子数组。

令low[index]以及high[index]分别表示以nums[index]为最后一个波谷以及最后一个波峰的最长交替子数组长度，那么：

1、当index \= 0，或者nums[index] \= nums[index - 1]时，有low[index] \= 1、high[index] \= 1。也就是这个交替子数组中只包含nums[index]自身

2、当nums[index] \< nums[index - 1]时，有low[index] \= high[index - 1] + 1、high[index] \= 1。表示nums[index]可以放在以nums[index - 1]为最后一个波峰的交替子数组后面，作为最后一个波谷；反之，如果nums[index]要作为最后一个波峰，这个交替子数组中就只能包含nums[index]自身。

3、与情况2对称，当nums[index] > nums[index - 1]时，有high[index] \= low[index - 1] + 1、low[index] \= 1。理由也与情况2对称。

计算完成后，max(low)和max(high)中的较大值即为不移除任意元素时最长交替子数组的长度。

接下来考虑移除一个元素的情况。

首先可以明确的是，移除nums[0]或者nums[-1]是没有意义的，而移除掉1到len(nums) - 2之间的某个nums[index]后，如果nums[index - 1]与nums[index + 1]能拼到一起，那么这次移除才有意义。

更进一步的，在移除nums[index]后，要么是nums[index - 1]当波峰，nums[index + 1]当波谷，要么反过来nums[index - 1]当波谷，nums[index - 1]当波峰。

对于以上两种情况，都需要知道：

- 从index - 1开始向前，以nums[index - 1]为最后一个波峰/最后一个波谷时的最长交替子数组长度。对于这个问题，可以直接照搬一开始讨论的不删除元素的计算方法得到。在这里分别记为to_left_low[index - 1]以及to_left_high[index - 1]。
- 从index + 1开始向后，以nums[index + 1]为第一个波峰/第一个波谷时的最长交替子数组长度。对于这个问题，可以参考上面的做法，改为从后往前进行遍历，将low和high的意义改为作为第一个波谷/波峰时最长交替子数组的长度。在这里分别记为to_right_low[index + 1]以及to_right_high[index + 1]。

接下来，若nums[index - 1] \< nums[index + 1]，就可以使用to_left_low[index - 1] + to_right_high[index + 1]来更新答案；若nums[index - 1] > nums[index + 1]，则可以使用to_left_high[index - 1] + to_right_low[index + 1]来更新答案。

基于上面的结论，就可以先正反两趟遍历，先预处理出to_left_low、to_left_high、to_right_low、to_right_high这四个数组，接下来再按照上面两种情况中对应的方法找出最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def longestAlternating(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        to_left_high = [1] * n
        to_left_low = [1] * n
        for index in range(1, n):
            if nums[index] == nums[index - 1]:
                continue
            if nums[index] < nums[index - 1]:
                to_left_low[index] = to_left_high[index - 1] + 1
            else:
                to_left_high[index] = to_left_low[index - 1] + 1
        
        to_right_high = [1] * n
        to_right_low = [1] * n
        for index in range(n - 2, -1, -1):
            if nums[index] == nums[index + 1]:
                continue
            if nums[index] < nums[index + 1]:
                to_right_low[index] = to_right_high[index + 1] + 1
            else:
                to_right_high[index] = to_right_low[index + 1] + 1
        
        res = max(max(to_left_high), max(to_left_low))
        for index in range(1, n - 1):
            if nums[index - 1] > nums[index + 1]:
                res = max(res, to_left_high[index - 1] + to_right_low[index + 1])
            if nums[index - 1] < nums[index + 1]:
                res = max(res, to_left_low[index - 1] + to_right_high[index + 1])
        return res
```
