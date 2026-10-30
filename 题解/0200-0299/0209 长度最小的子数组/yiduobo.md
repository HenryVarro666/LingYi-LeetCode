---
title: "209. 长度最小的子数组"
aliases: ["yiduobo的每日leetcode 209.长度最小的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/面试经典-150-题/滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147365627"
zhihu_id: "147365627"
zhihu_title: "yiduobo的每日leetcode 209.长度最小的子数组"
question_id: "209"
question: "长度最小的子数组"
problem_url: "https://leetcode.cn/problems/minimum-size-subarray-sum/"
difficulty: "Medium"
created: "2020-06-10T22:37:53+08:00"
updated: "2020-06-10T22:37:53+08:00"
upvotes: 1
comments: 0
---

# 209. 长度最小的子数组

> **[yiduobo的每日leetcode 209.长度最小的子数组](https://zhuanlan.zhihu.com/p/147365627) · 知乎 · 2020-06-10 · 赞同 1**
> 力扣：[209. 长度最小的子数组](https://leetcode.cn/problems/minimum-size-subarray-sum/) · Medium · 灵茶山艾府：[【视频】两种写法：循环外更新/循环内更新，附题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

209.长度最小的子数组<https://leetcode-cn.com/problems/minimum-size-subarray-sum/>

根据题目描述，存在O(n)和O(nlogn)的做法。

先说nlogn的做法。对于位于index的数nums[i]，若这个数为要求的子数组的左端点，那么需要找到最小的j，使得nums[i + 1] + nums[i + 2] + ... + nums[j] >\= s - nums[i]。式子前面的部分可以通过前缀和来快速得到，即sum[j] - sum[i]。另外，题目保证了nums都是正整数，那么前缀和sum就是单调递增的，于是可以在sum中二分j的位置。

一趟扫描计算出前缀和sum，再一趟确定i的位置，对于每个i需要进行一次二分查找，因此最终的时间复杂度为O(nlogn)。

接下来是线性的算法。实际上还是需要对每个i找到最小的j，不过我们可以在找i时运用到i - 1以及其对应的j'的信息。具体来说就是对于i来说，若i - 1找到的最优右边界为j'，那么i的右边界j一定大于等于j'。证明也很简单：

nums[i] + nums[i + 1] + ... + nums[j] >\= s

那么一定有

nums[i - 1] + nums[i] + ... + nums[j] >\= s

若此时j小于j'，那么j'就不是是i - 1的最优右边界因为此时j显然更好，这里就出现了矛盾。

有了上面这个结论，我们可以用一个指针从左往右扫，确定当前i的位置，接下来j只需要在i - 1得到的j'的基础上往右逐个试探，找到第一个满足条件的位置即可。由于每个i被遍历一次，每个j也只会被遍历一次，因此最终的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def minSubArrayLen(self, s, nums):
        """
        :type s: int
        :type nums: List[int]
        :rtype: int
        """

        if not nums or sum(nums) < s:
            return 0

        now = nums[0]
        left = 0 
        right = 0
        res = len(nums)
        while left < len(nums):
            while right + 1 < len(nums) and now < s:
                right += 1
                now += nums[right]
            if now < s:
                break
            while left < right and now - nums[left] >= s:
                now -= nums[left]
                left += 1
            res = min(res, right - left + 1)
            now -= nums[left]
            left += 1
        
        return res
```
