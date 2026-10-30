---
title: "2501. 数组中最长的方波"
aliases: ["yiduobo的每日leetcode 2501.数组中最长的方波"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/math", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634050844"
zhihu_id: "634050844"
zhihu_title: "yiduobo的每日leetcode 2501.数组中最长的方波"
question_id: "2501"
question: "数组中最长的方波"
problem_url: "https://leetcode.cn/problems/longest-square-streak-in-an-array/"
difficulty: "Medium"
rating: 1480
created: "2023-06-02T02:04:32+08:00"
updated: "2023-06-02T02:04:32+08:00"
upvotes: 0
comments: 0
---

# 2501. 数组中最长的方波

> **[yiduobo的每日leetcode 2501.数组中最长的方波](https://zhuanlan.zhihu.com/p/634050844) · 知乎 · 2023-06-02 · 赞同 0**
> 力扣：[2501. 数组中最长的方波](https://leetcode.cn/problems/longest-square-streak-in-an-array/) · Medium · 灵茶山艾府：[两种方法：暴力枚举 / 记忆化搜索](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2501.数组中最长的方波

[力扣](https://leetcode.cn/problems/longest-square-streak-in-an-array/)

使用一个集合记录所有出现在数组中的数，接下来从小到大一趟遍历，对于当前遍历到的数x，若x没有被访问过，那么就通过集合检测x^2是否出现在数组中，若出现过，则将x迭代为x^2并将其标记为访问过，重复此过程直到x^2没有出现在集合中为止。过程中访问过的数字数量就是当前子序列的长度，使用这个值更新答案然后继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def longestSquareStreak(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set(nums)
        vis = set()

        res = 0
        for num in sorted(list(num_set)):
            if num not in vis:
                cnt = 1
                vis.add(num)
                while num * num in num_set:
                    num *= num
                    vis.add(num)
                    cnt += 1
                
                res = max(res, cnt)
        
        if res == 1:
            return -1
        
        return res
```
