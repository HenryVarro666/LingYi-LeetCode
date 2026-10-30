---
title: "3727. 最大交替平方和"
aliases: ["yiduobo的每日leetcode 3727.最大交替平方和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1966972943755113707"
zhihu_id: "1966972943755113707"
zhihu_title: "yiduobo的每日leetcode 3727.最大交替平方和"
question_id: "3727"
question: "最大交替平方和"
problem_url: "https://leetcode.cn/problems/maximum-alternating-sum-of-squares/"
difficulty: "Medium"
rating: 1455
created: "2025-10-29T22:12:17+08:00"
updated: "2025-10-29T22:12:17+08:00"
upvotes: 2
comments: 0
---

# 3727. 最大交替平方和

> **[yiduobo的每日leetcode 3727.最大交替平方和](https://zhuanlan.zhihu.com/p/1966972943755113707) · 知乎 · 2025-10-29 · 赞同 2**
> 力扣：[3727. 最大交替平方和](https://leetcode.cn/problems/maximum-alternating-sum-of-squares/) · Medium · 灵茶山艾府：[贪心：排序 / 快速选择（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3727.最大交替平方和

[3727. 最大交替平方和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-alternating-sum-of-squares/description/)

题目给出一个整数数组nums，可以将nums按任意顺序重新排列。

定义数组arr的交替得分为score \= arr[0]^2 - arr[1]^2 + arr[2]^2 - arr[3]^3 + ...

问将nums重新排列后可以得到的最大交替得分。

题目中关于score的式子是由平方项构成的，为了使得最终答案最大，就应该让偶数下标项的平方尽量大，奇数下标项的平方尽量小。而对于一个数而言，其绝对值越大，平方就越大，因此在这里就应该将绝对值较大的数放置在偶数下标，将绝对值较小的数放置在奇数下标。

于是只需将nums按绝对值从小到大进行排序，然后使用两个指针分别从头尾向中间扫，每次先取当前剩余元素中绝对值最大的那个，将其平方累加到答案中，然后取剩余元素中绝对值最小的那个，将其平方从答案中减去。重复此过程，直到使用完nums中的所有元素为止。

最后附上python代码：

```python
class Solution(object):
    def maxAlternatingSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        nums.sort(key=lambda d:abs(d))
        left, right = 0, len(nums) - 1
        res = 0
        while left <= right:
            res += nums[right] ** 2
            right -= 1
            if left <= right:
                res -= nums[left] ** 2
                left += 1
        
        return res
```
