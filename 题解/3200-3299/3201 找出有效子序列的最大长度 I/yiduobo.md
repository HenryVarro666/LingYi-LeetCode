---
title: "3201. 找出有效子序列的最大长度I"
aliases: ["yiduobo的每日leetcode 3201.找出有效子序列的最大长度I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707444714"
zhihu_id: "707444714"
zhihu_title: "yiduobo的每日leetcode 3201.找出有效子序列的最大长度I"
question_id: "3201"
question: "找出有效子序列的最大长度 I"
problem_url: "https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-i/"
difficulty: "Medium"
created: "2024-07-07T00:32:53+08:00"
updated: "2024-07-07T00:32:53+08:00"
upvotes: 0
comments: 0
---

# 3201. 找出有效子序列的最大长度I

> **[yiduobo的每日leetcode 3201.找出有效子序列的最大长度I](https://zhuanlan.zhihu.com/p/707444714) · 知乎 · 2024-07-07 · 赞同 0**
> 力扣：[3201. 找出有效子序列的最大长度 I](https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-i/) · Medium · 灵茶山艾府：[分析式子+动态规划，两种方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3201.找出有效子序列的最大长度I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-i/description/)

题目给出一个整数数组nums，要求从nums中找出一个子序列sub，满足

(sub[0] + sub[1]) % 2 \= (sub[1] + sub[2]) % 2 \= ... \= (sub[-2] + sub[-1]) % 2

问sub最长可以是多少。

观察题目给出的式子，相邻项之和模2的结果只可能是0或者1。

当结果为0时，就意味着子序列中相邻项都同奇偶，更进一步的，整个子序列中的每一项都同奇偶。在这种情况下，最长的sub一定是nums中的全体奇数或者全体偶数构成的，于是只需一趟遍历统计nums中奇数和偶数的数量，其中较大的那一项就是这种情况下的最优解。

当结果为1时，说明子序列是奇偶交替出现的。对于这种情况，首先可以明确的是nums[0]一定可以加入到最优的子序列中，证明也很简单，若最优子序列中不包含nums[0]，那么不妨设其中首项为x，当nums[0]和x同奇偶时，可以用nums[0]替换x，此时子序列的长度不变；当nums[0]和x不同奇偶时，将nums[0]加入x的左侧就可以得到更优的子序列。综合起来，nums[0]一定可以加入到最优子序列中。确定了子序列首项为nums[0]后，就可以从nums[1]开始向后遍历，若当前遍历到的数与子序列中最后这一项奇偶性不同，就将其加入到子序列中，遍历完成后就得到了最优的子序列。

分别针对两种情况计算最优的子序列长度，然后取其中较大值返回即可。

最后附上python代码：

```python
class Solution(object):
    def maximumLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        even = 0
        pre = nums[0]
        res = 1
        if nums[0] % 2 == 0:
            even = 1
        
        for v in nums[1:]:
            if v % 2 == 0:
                even += 1
            
            if (pre + v) % 2 == 1:
                pre = v
                res += 1
        
        return max(res, even, len(nums) - even)
```
