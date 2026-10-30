---
title: "3701. 计算交替和"
aliases: ["yiduobo的每日leetcode 3701.计算交替和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1958245037394625652"
zhihu_id: "1958245037394625652"
zhihu_title: "yiduobo的每日leetcode 3701.计算交替和"
question_id: "3701"
question: "计算交替和"
problem_url: "https://leetcode.cn/problems/compute-alternating-sum/"
difficulty: "Easy"
created: "2025-10-05T19:09:41+08:00"
updated: "2025-10-05T19:11:57+08:00"
upvotes: 1
comments: 0
---

# 3701. 计算交替和

> **[yiduobo的每日leetcode 3701.计算交替和](https://zhuanlan.zhihu.com/p/1958245037394625652) · 知乎 · 2025-10-05 · 赞同 1**
> 力扣：[3701. 计算交替和](https://leetcode.cn/problems/compute-alternating-sum/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3701.计算交替和

[3701. 计算交替和 - 力扣（LeetCode）](https://leetcode.cn/problems/compute-alternating-sum/description/)

题目给出一个整数数组nums。交替和定义为将nums中偶数下标位置的元素相加，然后减去奇数下标位置的元素。问nums的交替和为多少。

对nums进行一趟遍历，根据当前下标的奇偶性来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def alternatingSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for index, v in enumerate(nums):
            if index % 2 == 0:
                res += v
            else:
                res -= v
        
        return res
```
