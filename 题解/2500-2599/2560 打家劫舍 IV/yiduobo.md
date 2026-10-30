---
title: "2560. 打家劫舍IV"
aliases: ["yiduobo的每日leetcode 2560.打家劫舍IV"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640273944"
zhihu_id: "640273944"
zhihu_title: "yiduobo的每日leetcode 2560.打家劫舍IV"
question_id: "2560"
question: "打家劫舍 IV"
problem_url: "https://leetcode.cn/problems/house-robber-iv/"
difficulty: "Medium"
rating: 2081
created: "2023-06-29T00:48:31+08:00"
updated: "2023-06-29T00:48:31+08:00"
upvotes: 1
comments: 0
---

# 2560. 打家劫舍IV

> **[yiduobo的每日leetcode 2560.打家劫舍IV](https://zhuanlan.zhihu.com/p/640273944) · 知乎 · 2023-06-29 · 赞同 1**
> 力扣：[2560. 打家劫舍 IV](https://leetcode.cn/problems/house-robber-iv/) · Medium · 灵茶山艾府：[两种方法：二分+DP/二分+贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2560.打家劫舍IV

[力扣](https://leetcode.cn/problems/house-robber-iv/)

首先，窃贼的能力值越高，成功的可能性就越大，因此本题可以使用二分法来找所需的最小窃取能力值。

另一方面，由于本题并不在意窃取的总金额，而是只需要保证窃取的房子数量，因此在这里可以使用贪心法来进行窃取，也就是一趟遍历，若当前的房子可以窃取，那么就执行窃取。

根据上面两个结论，就可以二分答案，二分的上下界自然是房屋金额的最小值和最大值。

对于当前二分到的mid，遍历nums数组，同时使用一个变量pre记录上一间房子是否窃取。对于当前遍历到的房屋金额nums[index]，若其小于等于mid，同时pre为false，那么就窃取这间房子，并更新pre为true，否则无法窃取这间房子，此时应该更新pre为false。

若最终窃取的房子数量超过了k，那么就调整二分上界为mid，否则调整二分下界为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minCapability(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        left = min(nums)
        right = max(nums)
        while left < right:
            mid = (left + right) / 2
            pre = False
            cnt = 0
            for v in nums:
                if v <= mid and not pre:
                    pre = True
                    cnt += 1
                else:
                    pre = False
            
            if cnt >= k:
                right = mid
            else:
                left = mid + 1
        
        return left
```
