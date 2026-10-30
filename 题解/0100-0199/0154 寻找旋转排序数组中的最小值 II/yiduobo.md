---
title: "154. 寻找旋转排序数组中的最小值II"
aliases: ["yiduobo的每日leetcode 154.寻找旋转排序数组中的最小值II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143532000"
zhihu_id: "143532000"
zhihu_title: "yiduobo的每日leetcode 154.寻找旋转排序数组中的最小值II"
question_id: "154"
question: "寻找旋转排序数组中的最小值 II"
problem_url: "https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array-ii/"
difficulty: "Hard"
created: "2020-05-25T21:23:00+08:00"
updated: "2020-05-25T21:23:00+08:00"
upvotes: 1
comments: 0
---

# 154. 寻找旋转排序数组中的最小值II

> **[yiduobo的每日leetcode 154.寻找旋转排序数组中的最小值II](https://zhuanlan.zhihu.com/p/143532000) · 知乎 · 2020-05-25 · 赞同 1**
> 力扣：[154. 寻找旋转排序数组中的最小值 II](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array-ii/) · Hard · 灵茶山艾府：[基于 153 题的简洁写法，只需增加一个 if（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

154.寻找旋转排序数组中的最小值II <https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array-ii/submissions/>

上一题的升级版，由于数组中可能出现相等的数，那么在二分过程中nums[mid]等于nums[right]时将无从判别究竟是哪一部分发生了旋转，例如

1 2 2 2 2 2 2

2 2 2 2 2 1 2

都是合法的旋转结果，而第一次二分，可以看到nums[mid]等于nums[right]，此时无法判断答案究竟位于哪个部分。一个可行的做法是将nums[right]从nums中去除，即right -\= 1。这样做的话最坏情况下二分就退化到了O(n)，于是干脆就选择O(n)的做法即可。

最后附上python代码：

```python
class Solution(object):
    def findMin(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        return min(nums)
```
