---
title: "1343. 大小为K且平均值大于等于阈值的子数组数目"
aliases: ["yiduobo的每日leetcode 1343.大小为K且平均值大于等于阈值的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/396805308"
zhihu_id: "396805308"
zhihu_title: "yiduobo的每日leetcode 1343.大小为K且平均值大于等于阈值的子数组数目"
question_id: "1343"
question: "大小为 K 且平均值大于等于阈值的子数组数目"
problem_url: "https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/"
difficulty: "Medium"
rating: 1317
created: "2021-08-05T22:32:45+08:00"
updated: "2021-08-05T22:32:45+08:00"
upvotes: 1
comments: 0
---

# 1343. 大小为K且平均值大于等于阈值的子数组数目

> **[yiduobo的每日leetcode 1343.大小为K且平均值大于等于阈值的子数组数目](https://zhuanlan.zhihu.com/p/396805308) · 知乎 · 2021-08-05 · 赞同 1**
> 力扣：[1343. 大小为 K 且平均值大于等于阈值的子数组数目](https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/) · Medium · 灵茶山艾府：[【模板】定长滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1343.大小为K且平均值大于等于阈值的子数组数目

[力扣](https://leetcode-cn.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/)

题目要求是找出长度为K，且平均值大于等于threshold的子数组数目，那么转化一下，就是要找出长度为K，且子数组的和大于等于K \* threshold的子数组的数目。由于这里的子数组长度是固定的，那么可以使用一个大小为K的滑动窗口，从数组头部开始向后滑动。

窗口初始覆盖的位置应该是arr[0]到arr[k - 1]，那么可以先初始化窗口数组和now \= sum(arr[:k])。若now大于等于K \* threshold，那么我们初始化res为1，否则初始化res为0。

接下来我们将窗口一步步向右移动，对于当前位置index，我们将arr[index]加入到窗口中，同时将左边界的arr[index - k]从窗口中移出，那么此时应该修改窗口数组和修改为now - arr[index - k] + arr[k]，接下来检测当前的now与K \* threshold的大小关系，并更新答案，直到窗口滑动到数组末尾即可。

最后附上python代码：

```python
class Solution(object):
    def numOfSubarrays(self, arr, k, threshold):
        """
        :type arr: List[int]
        :type k: int
        :type threshold: int
        :rtype: int
        """

        now = sum(arr[:k])
        res = 0
        if now >= threshold * k:
            res = 1
        
        for index in range(k, len(arr)):
            now = now + arr[index] - arr[index - k]
            if now >= threshold * k:
                res += 1
        
        return res
```
