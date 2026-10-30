---
title: "1526. 形成目标数组的子数组最少增加次数"
aliases: ["yiduobo的每日leetcode 1526.形成目标数组的子数组最少增加次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422497083"
zhihu_id: "422497083"
zhihu_title: "yiduobo的每日leetcode 1526.形成目标数组的子数组最少增加次数"
question_id: "1526"
question: "形成目标数组的子数组最少增加次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/"
difficulty: "Hard"
rating: 1872
created: "2021-10-17T18:41:48+08:00"
updated: "2021-10-17T18:41:48+08:00"
upvotes: 0
comments: 0
---

# 1526. 形成目标数组的子数组最少增加次数

> **[yiduobo的每日leetcode 1526.形成目标数组的子数组最少增加次数](https://zhuanlan.zhihu.com/p/422497083) · 知乎 · 2021-10-17 · 赞同 0**
> 力扣：[1526. 形成目标数组的子数组最少增加次数](https://leetcode.cn/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/) · Hard · 灵茶山艾府：[用差分思考，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1526.形成目标数组的子数组最少增加次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/)

对比这个问题有两种思路，不过有一点相同的地方是由于中间部分的位置可能收到两侧的影响，因此应该从两侧开始向中间处理。

第一种思路就是对于target[index]这个位置上的数，找出下一个比target[index]小的数的位置pos，那么就可以从index到pos - 1这一段就执行target[index] - target[pos]次操作拉平差距，然后剩下的则等到处理到pos这个位置时再进行操作。这种做法首先需要使用单调栈找出下一个更小数的位置，然后使用log(n)级别的数据结构处理区间值问题。

第二种思路相对更简洁，可以认为是第一种思路的精简版。简单来说，就是对于target[index]而言，若target[index] > target[index + 1]，那么就按思路一的做法进行操作。而target[index] \<\= target[index + 1]时，则可以等到处理index + 1时再进行操作，而不是第一种思路中的由最左侧的位置来进行操作。

最后附上python代码：

```python
class Solution(object):
    def minNumberOperations(self, target):
        """
        :type target: List[int]
        :rtype: int
        """

        res = 0
        n = len(target)
        for index in range(n - 1):
            if target[index] > target[index + 1]:           
                res += target[index] - target[index + 1]
        
        res += target[-1]
        return res
```
