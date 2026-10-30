---
title: "1814. 统计一个数组中好对子的数目"
aliases: ["yiduobo的每日leetcode 1814.统计一个数组中好对子的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/465122669"
zhihu_id: "465122669"
zhihu_title: "yiduobo的每日leetcode 1814.统计一个数组中好对子的数目"
question_id: "1814"
question: "统计一个数组中好对子的数目"
problem_url: "https://leetcode.cn/problems/count-nice-pairs-in-an-array/"
created: "2022-02-08T23:13:09+08:00"
updated: "2022-02-08T23:13:09+08:00"
upvotes: 0
comments: 0
---

# 1814. 统计一个数组中好对子的数目

> **[yiduobo的每日leetcode 1814.统计一个数组中好对子的数目](https://zhuanlan.zhihu.com/p/465122669) · 知乎 · 2022-02-08 · 赞同 0**
> 力扣：[1814. 统计一个数组中好对子的数目](https://leetcode.cn/problems/count-nice-pairs-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1814.统计一个数组中好对子的数目

[力扣](https://leetcode-cn.com/problems/count-nice-pairs-in-an-array/)

将题目中的

nums[i] + rev(nums[j]) \= nums[j] + rev(nums[i])

移项后可得

nums[i] - rev(nums[i]) \= nums[j] - rev(nums[j])

可以发现，等式两侧的形式一趟且只与一个数有关，因此可以一趟遍历，使用哈希表记录每个数在上面这个式子下的结果。

对于这些差值而言，若某个差值出现的次数为cnt，那么从中间选出两个就是一组合法的好对子，此时一共可以选出cnt \* (cnt - 1) / 2组好对子。遍历所有的差值，利用每种差值的cnt计算对应的好对子数目并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def countNicePairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        delta_dict = {}
        for num in nums:
            tmp = num
            num_list = []
            while tmp:
                num_list.append(tmp % 10)
                tmp /= 10
            
            reverse = 0
            for digit in num_list:
                reverse = reverse * 10 + digit
            
            delta_dict[num - reverse] = delta_dict.get(num - reverse, 0) + 1
        
        res = 0
        mod = 10 ** 9 + 7
        for cnt in delta_dict.values():
            res = res + cnt * (cnt - 1) / 2
            res %= mod
        
        return res
```
