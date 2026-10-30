---
title: "3151. 特殊数组I & 3152. 特殊数组II"
aliases: ["yiduobo的每日leetcode 3151.特殊数组I && 3152.特殊数组II", "3151. 特殊数组I", "3152. 特殊数组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703743548"
zhihu_id: "703743548"
zhihu_title: "yiduobo的每日leetcode 3151.特殊数组I && 3152.特殊数组II"
question_id: ["3151", "3152"]
question: ["特殊数组 I", "特殊数组 II"]
problem_url: ["https://leetcode.cn/problems/special-array-i/", "https://leetcode.cn/problems/special-array-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1523
created: "2024-06-17T02:41:57+08:00"
updated: "2024-06-17T02:41:57+08:00"
upvotes: 0
comments: 0
---

# 3151. 特殊数组I & 3152. 特殊数组II

> **[yiduobo的每日leetcode 3151.特殊数组I && 3152.特殊数组II](https://zhuanlan.zhihu.com/p/703743548) · 知乎 · 2024-06-17 · 赞同 0**
> 力扣：[3151. 特殊数组 I](https://leetcode.cn/problems/special-array-i/) · Easy · 灵茶山艾府：[遍历判断相邻元素（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3152. 特殊数组 II](https://leetcode.cn/problems/special-array-ii/) · Medium · 灵茶山艾府：[两种方法：前缀和 / 奇偶性相同的位置（Python/Java/C++/Go）](../3152%20特殊数组%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3151.特殊数组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/special-array-i/description/)

3152.特殊数组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/special-array-ii/description/)

两题对特殊数组的定义一致，都是对于一个数组，若其中相邻项两两之间不同奇偶，那么这就是一个特殊数组。第一题是给出一个数组，问其是否为特殊数组；第二题则是给出一个数组和若干询问，每个询问都是问数组中的某个子数组是否为特殊数组。

对于这类通过相邻元素判断数组是否符合某种条件的问题，一种常见的做法就是先根据相邻元素的具体情况将数组转化为01数组，即对于nums[index]以及nums[index - 1]，若符合条件，那么就置对应的元素为0，否则置对应的元素为1。、

得到这样一个01数组之后，其符合条件的子数组中的元素必然都为0，即子数组对应的区间和为0。那么每个询问中的某个子数组是否为特殊数组，就是问某个子数组的区间和是否为0，而对于区间和问题，只需提前预处理好前缀和就可以高效求解了。

最后附上python代码：

```python
class Solution(object):
    def isArraySpecial(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        s = [0]
        for index in range(1, len(nums)):
            s.append(s[-1])
            if (nums[index] + nums[index - 1]) % 2 == 0:
                s[-1] += 1
        
        return [s[x] == s[y] for x, y in queries]
```
