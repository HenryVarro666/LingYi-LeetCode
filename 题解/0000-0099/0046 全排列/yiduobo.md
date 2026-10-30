---
title: "46. 全排列"
aliases: ["yiduobo的每日leetcode 46.全排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/125148143"
zhihu_id: "125148143"
zhihu_title: "yiduobo的每日leetcode 46.全排列"
question_id: "46"
question: "全排列"
problem_url: "https://leetcode.cn/problems/permutations/"
difficulty: "Medium"
created: "2020-04-04T23:06:27+08:00"
updated: "2020-04-04T23:06:27+08:00"
upvotes: 0
comments: 0
---

# 46. 全排列

> **[yiduobo的每日leetcode 46.全排列](https://zhuanlan.zhihu.com/p/125148143) · 知乎 · 2020-04-04 · 赞同 0**
> 力扣：[46. 全排列](https://leetcode.cn/problems/permutations/) · Medium · 灵茶山艾府：[【视频】回溯不会写？套路在此！精确计算搜索树的节点个数！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

46.全排列<https://leetcode-cn.com/problems/permutations/>

经典的搜索回溯问题，每次在list末尾加入一个未使用的数，然后进行下一步，当全部处理完之后弹出数组末尾的数并加入下一个未使用的数。

时间复杂度不太好分析，但是应该是指数级的。

最后附上python代码，used[index]表示nums中下标为index的数是否已经在使用过了：

```python
class Solution(object):
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        res = []
        used = [False for index in range(len(nums))]
        self.dfs(nums, 0, res, [], used)
        return res

    def dfs(self, nums, level, res, now, used):
        if level == len(nums):
            res.append([x for x in now])
            return

        for index, num in enumerate(nums):
            if not used[index]:
                now.append(num)
                used[index] = True
                self.dfs(nums, level + 1, res, now, used)
                used[index] = False
                now.pop()
```
