---
title: "2012. 数组美丽值求和"
aliases: ["yiduobo的每日leetcode 2012.数组美丽值求和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/504405848"
zhihu_id: "504405848"
zhihu_title: "yiduobo的每日leetcode 2012.数组美丽值求和"
question_id: "2012"
question: "数组美丽值求和"
problem_url: "https://leetcode.cn/problems/sum-of-beauty-in-the-array/"
difficulty: "Medium"
rating: 1468
created: "2022-04-25T00:50:12+08:00"
updated: "2022-04-25T00:50:13+08:00"
upvotes: 0
comments: 0
---

# 2012. 数组美丽值求和

> **[yiduobo的每日leetcode 2012.数组美丽值求和](https://zhuanlan.zhihu.com/p/504405848) · 知乎 · 2022-04-25 · 赞同 0**
> 力扣：[2012. 数组美丽值求和](https://leetcode.cn/problems/sum-of-beauty-in-the-array/) · Medium · 灵茶山艾府：[前缀最大值+后缀最小值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2012.数组美丽值求和

[力扣](https://leetcode-cn.com/problems/sum-of-beauty-in-the-array/)

题目将数组中的值分成了三类，其中得分为1的比较好判断，一趟遍历就可以判断完成。

对于得分为2的条件则需要提前做一些准备。题目要求对于nums[index]，其左侧的所有值都小于nums[index]，同时其右侧的所有值都大于nums[index]。换言之，就是要求nums[index]左侧的最大值小于nums[index]，同时nums[index]右侧的最小值大于nums[index]，问题就转化成了前缀最大值和后缀最小值问题，同样可以一趟遍历求解得到。

于是现在就有了一种做法：

1、正反两趟遍历，分别求解出前缀最大值数组l_max以及后缀最小值数组r_min

2、接下来再一趟遍历，对于当前处理的nums[index]，首先根据l_max[index - 1]以及r_min[index + 1]来判断nums[index]是否满足得分为2的条件。若满足，则更新答案，否则还需要判断nums[index]是否大于nums[index - 1]且小于nums[index + 1]。若满足，那么答案加上1，否则答案不变

最后附上python代码：

```python
class Solution(object):
    def sumOfBeauties(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)

        l_max = [nums[0]]
        for index in range(1, n):
            l_max.append(max(l_max[-1], nums[index]))
        
        r_min = [nums[-1]]
        for index in range(n - 2, -1, -1):
            r_min.append(min(r_min[-1], nums[index]))
        r_min.reverse()

        res = 0
        for index in range(1, n - 1):
            if l_max[index - 1] < nums[index] < r_min[index + 1]:
                res += 2
            elif nums[index - 1] < nums[index] < nums[index + 1]:
                res += 1
        
        return res
```
