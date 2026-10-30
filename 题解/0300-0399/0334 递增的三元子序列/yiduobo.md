---
title: "334. 递增的三元子序列"
aliases: ["yiduobo的每日leetcode 334.递增的三元子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161671041"
zhihu_id: "161671041"
zhihu_title: "yiduobo的每日leetcode 334.递增的三元子序列"
question_id: "334"
question: "递增的三元子序列"
problem_url: "https://leetcode.cn/problems/increasing-triplet-subsequence/"
difficulty: "Medium"
created: "2020-07-19T15:56:30+08:00"
updated: "2020-07-19T15:56:30+08:00"
upvotes: 0
comments: 0
---

# 334. 递增的三元子序列

> **[yiduobo的每日leetcode 334.递增的三元子序列](https://zhuanlan.zhihu.com/p/161671041) · 知乎 · 2020-07-19 · 赞同 0**
> 力扣：[334. 递增的三元子序列](https://leetcode.cn/problems/increasing-triplet-subsequence/) · Medium · 灵茶山艾府：[通用解法，把 3 改成 k 也能做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

334.递增的三元子序列<https://leetcode-cn.com/problems/increasing-triplet-subsequence/>

可以使用最长上升子序列的思路。这里只需要找到长度为3的子序列，于是只需要通过两个变量first与second分别表示当前长度为1和长度为2的上升子序列中最小的末尾元素，那么对于一个新来的元素x：

1、若x > second，说明找到了长度为3的上升子序列，返回答案即可

2、若x \<\= first，此时需要使用x更新first

3、否则的话一定是first \< x \<\=second，那么此时使用x更新second

一趟扫描，每次最多只需要比较两次，因此最终的时间复杂度为O(n)。只需要两个变量first与second，因此空间复杂度为O(1)。符合题目的要求。

最后附上python代码：

```python
class Solution(object):
    def increasingTriplet(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        if len(nums) < 3:
            return False

        first = nums[0]
        second = None
        for num in nums[1:]:
            if second is None:
                if num > first:
                    second = num
                else:
                    first = num
            else:
                if num > second:
                    return True
                if num <= first:
                    first = num
                else:
                    second = num

        return False
```
