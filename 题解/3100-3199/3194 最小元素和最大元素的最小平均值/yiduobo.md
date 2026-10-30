---
title: "3194. 最小元素和最大元素的最小平均值"
aliases: ["yiduobo的每日leetcode 3194.最小元素和最大元素的最小平均值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706906925"
zhihu_id: "706906925"
zhihu_title: "yiduobo的每日leetcode 3194.最小元素和最大元素的最小平均值"
question_id: "3194"
question: "最小元素和最大元素的最小平均值"
problem_url: "https://leetcode.cn/problems/minimum-average-of-smallest-and-largest-elements/"
difficulty: "Easy"
created: "2024-07-03T23:56:08+08:00"
updated: "2024-07-03T23:56:08+08:00"
upvotes: 1
comments: 0
---

# 3194. 最小元素和最大元素的最小平均值

> **[yiduobo的每日leetcode 3194.最小元素和最大元素的最小平均值](https://zhuanlan.zhihu.com/p/706906925) · 知乎 · 2024-07-03 · 赞同 1**
> 力扣：[3194. 最小元素和最大元素的最小平均值](https://leetcode.cn/problems/minimum-average-of-smallest-and-largest-elements/) · Easy · 灵茶山艾府：[排序+遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3194.最小元素和最大元素的最小平均值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-average-of-smallest-and-largest-elements/description/)

题目给出一个长度为n的整数数组nums，n为偶数。接下来的n // 2轮，每一轮都需要从nums中选出当前最小和最大的元素，从nums中移除并计算二者的平均值，问这n // 2个平均值中的最小值是多少。

由于每一轮都需要获取当前数组中的最小值和最大值，那么就可以将nums从小到大进行排序，接下来只需两个指针从两侧向中间遍历，指向的元素就是当前这一轮需要的最小值和最大值，计算二者的平均值然后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumAverage(self, nums):
        """
        :type nums: List[int]
        :rtype: float
        """

        nums.sort()
        left, right = 0, len(nums) - 1
        res = None

        while left < right:
            v = (nums[left] + nums[right]) * 0.5
            if res is None or res > v:
                res = v
            left += 1
            right -= 1
        
        return res
```
