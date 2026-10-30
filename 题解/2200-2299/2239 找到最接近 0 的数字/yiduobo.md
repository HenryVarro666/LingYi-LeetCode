---
title: "2239. 找到最接近0的数字"
aliases: ["yiduobo的每日leetcode 2239.找到最接近0的数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/545101452"
zhihu_id: "545101452"
zhihu_title: "yiduobo的每日leetcode 2239.找到最接近0的数字"
question_id: "2239"
question: "找到最接近 0 的数字"
problem_url: "https://leetcode.cn/problems/find-closest-number-to-zero/"
difficulty: "Easy"
created: "2022-07-22T23:45:43+08:00"
updated: "2022-07-22T23:45:43+08:00"
upvotes: 0
comments: 0
---

# 2239. 找到最接近0的数字

> **[yiduobo的每日leetcode 2239.找到最接近0的数字](https://zhuanlan.zhihu.com/p/545101452) · 知乎 · 2022-07-22 · 赞同 0**
> 力扣：[2239. 找到最接近 0 的数字](https://leetcode.cn/problems/find-closest-number-to-zero/) · Easy · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2239.找到最接近0的数字

[力扣](https://leetcode.cn/problems/find-closest-number-to-zero/)

越接近0绝对值就越小，因此只需一趟遍历，找出绝对值最小的数字就行了。另外根据题目要求，若两个数绝对值相同，那么取其中较大的作为答案。

最后附上python代码：

```python
class Solution(object):
    def findClosestNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = nums[0]
        for num in nums[1:]:
            if abs(num) < abs(res) or (abs(num) == abs(res) and num > res):
                res = num
        
        return res
```
