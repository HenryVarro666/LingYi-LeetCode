---
title: "39. 组合总和"
aliases: ["yiduobo的每日leetcode 39.组合总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/dynamic-programming", "leetcode/backtracking", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/122528709"
zhihu_id: "122528709"
zhihu_title: "yiduobo的每日leetcode 39.组合总和"
question_id: "39"
question: "组合总和"
problem_url: "https://leetcode.cn/problems/combination-sum/"
difficulty: "Medium"
created: "2020-04-01T21:47:49+08:00"
updated: "2020-04-01T21:47:49+08:00"
upvotes: 0
comments: 0
---

# 39. 组合总和

> **[yiduobo的每日leetcode 39.组合总和](https://zhuanlan.zhihu.com/p/122528709) · 知乎 · 2020-04-01 · 赞同 0**
> 力扣：[39. 组合总和](https://leetcode.cn/problems/combination-sum/) · Medium · 灵茶山艾府：[三种方法：选或不选/枚举选哪个/完全背包预处理+可行性剪枝（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

39.组合总和<https://leetcode-cn.com/problems/combination-sum/>

搜索回溯的题目，当然如果target不会太大的话也可以用背包的思路来做。

搜索的思路还是每次尝试加入一个数，然后判断是否等于target。当等于target或者加入最小的数依然大于target时就回溯，然后尝试加入下一个数。

另外，题目要求不能有重复的解，因此在选取了一个数之后，剩下的数应该在当前这个数排在这个数后面的数中进行选取，于是一个简单的思路就是选取一个数之后记录下这个数的位置，然后下次选取时从这个位置往后选取。

最后附上python代码：

```python
class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """

        res = []
        self.dfs(sorted(candidates), 0, target, [], res)

        return res

    def dfs(self, candidates, now_pos, target, now_choose, res):
        if target == 0:
            res.append([x for x in now_choose])
            return

        for index in range(now_pos, len(candidates)):
            if candidates[index] > target:
                break
            target -= candidates[index]
            now_choose.append(candidates[index])
            self.dfs(candidates, index, target, now_choose, res)
            now_choose.pop()
            target += candidates[index]
```
