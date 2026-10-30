---
title: "2873. 有序三元组中的最大值I & 2874. 有序三元组中的最大值II"
aliases: ["yiduobo的每日leetcode 2873.有序三元组中的最大值I && 2874.有序三元组中的最大值II", "2873. 有序三元组中的最大值I", "2874. 有序三元组中的最大值II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/enumeration", "leetcode/medium", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662626395"
zhihu_id: "662626395"
zhihu_title: "yiduobo的每日leetcode 2873.有序三元组中的最大值I && 2874.有序三元组中的最大值II"
question_id: ["2873", "2874"]
question: ["有序三元组中的最大值 I", "有序三元组中的最大值 II"]
problem_url: ["https://leetcode.cn/problems/maximum-value-of-an-ordered-triplet-i/", "https://leetcode.cn/problems/maximum-value-of-an-ordered-triplet-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1583
created: "2023-10-21T20:07:50+08:00"
updated: "2023-10-21T20:07:50+08:00"
upvotes: 0
comments: 0
---

# 2873. 有序三元组中的最大值I & 2874. 有序三元组中的最大值II

> **[yiduobo的每日leetcode 2873.有序三元组中的最大值I && 2874.有序三元组中的最大值II](https://zhuanlan.zhihu.com/p/662626395) · 知乎 · 2023-10-21 · 赞同 0**
> 力扣：[2873. 有序三元组中的最大值 I](https://leetcode.cn/problems/maximum-value-of-an-ordered-triplet-i/) · Easy · 灵茶山艾府：[两种 O(n) 做法：枚举 j / 枚举 k（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[2874. 有序三元组中的最大值 II](https://leetcode.cn/problems/maximum-value-of-an-ordered-triplet-ii/) · Medium · 灵茶山艾府：[两种方法：枚举 j / 枚举 k（Python/Java/C++/C/Go/JS/Rust）](../2874%20有序三元组中的最大值%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2873.有序三元组中的最大值I && 2874.有序三元组中的最大值II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-value-of-an-ordered-triplet-i/)

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-value-of-an-ordered-triplet-ii/)

两个题目的题设相同，都是要求找出一个三元组(i, j, k)，使得(nums[i] - nums[j]) \* nums[k]的值最大，不过后面这题的数据规模较大，不能使用暴力法求解。

对于这类三元组的求解，常见的做法是枚举中间元素的下标，本题就是枚举j，然后尝试找出适配j的最优的i和k。

由于数组中的元素都是正数，且最终答案只取非负数，因此没有必要考虑nums[i]小于nums[j]的情况，而当nums[i]大于等于nums[j]时，则应该使得nums[i]以及nums[k]尽量大。到了这里，问题就变成了给出一个j，找出nums[0]到nums[j - 1]中的最大值，以及nums[j +1]到nums[-1]中的最大值，即前缀最大值与后缀最大值的问题。于是只需正反两趟遍历，计算前缀和后缀的最大值数组prefix以及suffix，然后枚举j，使用(prefix[j - 1] - nums[j]) \* suffix[j + 1]来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumTripletValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        n = len(nums)

        prefix = [nums[0]]
        for index in range(1, n):
            prefix.append(max(prefix[-1], nums[index]))
        
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(max(suffix[-1], nums[index]))
        suffix.reverse()

        for j in range(1, n - 1):
            res = max(res, (prefix[j - 1] - nums[j]) * suffix[j + 1])
        
        return res
```
