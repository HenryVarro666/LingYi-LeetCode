---
title: "78. 子集"
aliases: ["yiduobo的每日leetcode 78.子集"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/133839160"
zhihu_id: "133839160"
zhihu_title: "yiduobo的每日leetcode 78.子集"
question_id: "78"
question: "子集"
problem_url: "https://leetcode.cn/problems/subsets/"
difficulty: "Medium"
created: "2020-04-20T21:24:38+08:00"
updated: "2020-04-20T21:24:38+08:00"
upvotes: 0
comments: 0
---

# 78. 子集

> **[yiduobo的每日leetcode 78.子集](https://zhuanlan.zhihu.com/p/133839160) · 知乎 · 2020-04-20 · 赞同 0**
> 力扣：[78. 子集](https://leetcode.cn/problems/subsets/) · Medium · 灵茶山艾府：[【视频】三种写法：选或不选/枚举选哪个/二进制枚举（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

78.子集<https://leetcode-cn.com/problems/subsets/>

依然是搜索回溯的题目。为了去除重复情况，同样可以用上一题中保证now单调递增的做法，然后在每次操作时从last_pos + 1开始往后枚举。每一个now都是解的一种，于是在每一轮dfs中都需要将now加入到解当中。

最后附上python代码：

```python
class Solution(object):
    def subsets(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        
        res = []
        now = []

        self.dfs(nums, -1, now, res)
        return res

    def dfs(self, nums, last_pos, now, res):
        res.append(now[:])
        for index in range(last_pos + 1, len(nums)):
            now.append(nums[index])
            self.dfs(nums, index, now, res)
            now.pop()
```
