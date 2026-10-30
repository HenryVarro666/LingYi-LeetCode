---
title: "2348. 全0子数组的数目"
aliases: ["yiduobo的每日leetcode 2348.全0子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/560716733"
zhihu_id: "560716733"
zhihu_title: "yiduobo的每日leetcode 2348.全0子数组的数目"
question_id: "2348"
question: "全 0 子数组的数目"
problem_url: "https://leetcode.cn/problems/number-of-zero-filled-subarrays/"
difficulty: "Medium"
rating: 1316
created: "2022-09-02T21:43:59+08:00"
updated: "2022-09-02T21:43:59+08:00"
upvotes: 0
comments: 0
---

# 2348. 全0子数组的数目

> **[yiduobo的每日leetcode 2348.全0子数组的数目](https://zhuanlan.zhihu.com/p/560716733) · 知乎 · 2022-09-02 · 赞同 0**
> 力扣：[2348. 全 0 子数组的数目](https://leetcode.cn/problems/number-of-zero-filled-subarrays/) · Medium · 灵茶山艾府：[两种更具一般性的方法：滑动窗口/增量法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2348.全0子数组的数目

[力扣](https://leetcode.cn/problems/number-of-zero-filled-subarrays/)

对于一段连续的k个0，其中有k个长度为1的全0子数组，k - 1个长度为2的全0子数组，...，1个长度为k的全0子数组。换言之，这一段连续的k个0可以提供总计(1 + k) \* k / 2个全0子数组。

于是只需一趟遍历，统计每一段连续出现的0的数量k。对于当前遍历到的数nums[index]，若其为0，说明这个数属于最近这一段连续0，此时应该将k加上1，否则说明最近这一段连续0结束了，此时应该使用(1 + k) \* k / 2更新答案，并重新置k为0。

需要注意的是，这个做法会漏掉最后这一段0，因此在遍历完成后还需要再使用当前的(1 + k) \* k / 2来更新答案。

最后附上python代码：

```python
class Solution(object):
    def zeroFilledSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        k = 0
        res = 0
        for num in nums:
            if num == 0:
                k += 1
            else:
                res += k * (k + 1) / 2
                k = 0
        
        return res + k * (k + 1) / 2
```
