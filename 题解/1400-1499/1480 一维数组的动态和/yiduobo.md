---
title: "1480. 一维数组的动态和"
aliases: ["yiduobo的每日leetcode 1480.一维数组的动态和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/dynamic-programming", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/415560197"
zhihu_id: "415560197"
zhihu_title: "yiduobo的每日leetcode 1480.一维数组的动态和"
question_id: "1480"
question: "一维数组的动态和"
problem_url: "https://leetcode.cn/problems/running-sum-of-1d-array/"
difficulty: "Easy"
created: "2021-09-29T22:34:07+08:00"
updated: "2021-09-29T22:34:07+08:00"
upvotes: 0
comments: 0
---

# 1480. 一维数组的动态和

> **[yiduobo的每日leetcode 1480.一维数组的动态和](https://zhuanlan.zhihu.com/p/415560197) · 知乎 · 2021-09-29 · 赞同 0**
> 力扣：[1480. 一维数组的动态和](https://leetcode.cn/problems/running-sum-of-1d-array/) · Easy · 灵茶山艾府：[两种 O(n) 写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1480.一维数组的动态和

[力扣](https://leetcode-cn.com/problems/running-sum-of-1d-array/)

比较基础的题目，就是要求数组的前缀和，之间一趟扫描累加即可。

最后附上python代码：

```python
class Solution(object):
    def runningSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        res = [nums[0]]
        for index in range(1, len(nums)):
            res.append(res[-1] + nums[index])
        
        return res
```
