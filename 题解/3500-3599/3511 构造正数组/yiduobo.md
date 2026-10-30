---
title: "3511. 构造正数组"
aliases: ["yiduobo的每日leetcode 3511.构造正数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902516466038846825"
zhihu_id: "1902516466038846825"
zhihu_title: "yiduobo的每日leetcode 3511.构造正数组"
question_id: "3511"
question: "构造正数组"
problem_url: "https://leetcode.cn/problems/make-a-positive-array/"
created: "2025-05-05T00:29:58+08:00"
updated: "2025-05-05T00:29:58+08:00"
upvotes: 3
comments: 0
---

# 3511. 构造正数组

> **[yiduobo的每日leetcode 3511.构造正数组](https://zhuanlan.zhihu.com/p/1902516466038846825) · 知乎 · 2025-05-05 · 赞同 3**
> 力扣：[3511. 构造正数组](https://leetcode.cn/problems/make-a-positive-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3511.构造正数组

[3511. 构造正数组 - 力扣（LeetCode）](https://leetcode.cn/problems/make-a-positive-array/description/)

题目给出一个数组nums，其中元素值在-10^9到10^9之间。接下来定义若一个数组中每个包含超过两个元素的子数组的所有数字之和都是正数，那么就认为这个数组是正的。

现在可以对nums执行操作任意次，每次操作可以将nums中的任意元素替换为-10^18到10^18之间的任意整数。

问至少需要多少次操作才能使得nums变为正的。

题目实际上是需要通过若干次操作，使得nums中所有长度大于等于3的子数组的元素之和都大于0，而对于子数组和这一问题，则可以转化为前缀和来进行计算。更进一步的，对于当前的前缀和s[index]，若在s[0]到s[index - 3]之间存在某个前缀和s[p]，其大于s[index]，那么从p + 1到index这一段的子数组和，也就是s[index] - s[p]就必然小于0，此时就需要将s[index]修改为10^18。

于是只需一趟遍历，一边计算前缀和s，一边计算符合边界条件的最大前缀和ma，若某一时刻ma大于s[index]，那么就执行操作。

在具体实现上，当某次操作执行时，由于s[index]被修改到了一个特别大的水平，可以认为把index与之前的部分截断出去无需再考虑了，因此在这里可以重新计算前缀和s，而不需要真的将10^18累加到前缀和中。需要注意如果这样操作的话，就需要额外使用一个变量left记录当前子数组的起点，只有当index - left + 1 >\= 3，也就是子数组长度等于3时，才判断ma与s[index]的大小，同时只有当index >\= left + 1时，才更新ma。

最后附上python代码：

```python
class Solution(object):
    def makeArrayPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = [0]
        left = 0
        res = 0
        ma = 0
        for index, v in enumerate(nums):
            s.append(s[-1] + v)
            if index - left + 1>= 3 and ma >= s[-1]:
                res += 1
                ma = 0
                s[-1] = 0
                left = index + 1
            elif index >= left + 1:
                ma = max(ma, s[-3])

        return res
```
