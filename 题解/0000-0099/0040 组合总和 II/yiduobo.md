---
title: "40. 组合总和II"
aliases: ["yiduobo的每日leetcode 40.组合总和II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/122531313"
zhihu_id: "122531313"
zhihu_title: "yiduobo的每日leetcode 40.组合总和II"
question_id: "40"
question: "组合总和 II"
problem_url: "https://leetcode.cn/problems/combination-sum-ii/"
difficulty: "Medium"
created: "2020-04-01T22:00:10+08:00"
updated: "2020-04-01T22:00:10+08:00"
upvotes: 0
comments: 0
---

# 40. 组合总和II

> **[yiduobo的每日leetcode 40.组合总和II](https://zhuanlan.zhihu.com/p/122531313) · 知乎 · 2020-04-01 · 赞同 0**
> 力扣：[40. 组合总和 II](https://leetcode.cn/problems/combination-sum-ii/) · Medium · 灵茶山艾府：[两种方法：选或不选/枚举选哪个（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

40.组合总和II <https://leetcode-cn.com/problems/combination-sum-ii/>

上一题的升级版本，不过多出了一个需求，即每个数字在每个组合中只能使用一次。处理方法也很简单，在选择一个数字之后，同样是记录下这次选择的位置，下一轮从这个位置后一位开始往后选取即可。

另外，这个问题同样要求不能有相同的组合，意味着回溯回来再进行选择时，不应该选择重复的数字，因此我们可以先通过排序，然后计算出对于当前数组中的每一个数a\[k\]，计算出一个next_pos\[k\]，表示下一个不等于a\[k\]的数的下标是多少，然后在a\[k\]回溯时直接继续尝试a\[next_pos\[k\]\]而不是原来的a\[k + 1\]。

最后附上python代码，其中next_pos数组代表下一个不同的数的下标：

```python
class Solution(object):
    def combinationSum2(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """

        next_pos = [i + 1 for i in range(len(candidates))]
        candidates = sorted(candidates)
        
        now = None
        for index in range(len(candidates) - 1, -1, -1):
            if index + 1 != len(candidates) and candidates[index] == candidates[index + 1]:
                next_pos[index] = next_pos[index + 1]

        res = []
        self.dfs(candidates, target, 0, next_pos, [], res)
        return res

    def dfs(self, candidates, target, now_pos, next_pos, now_choose, res):
        if target == 0:
            res.append([x for x in now_choose])
            return

        index = now_pos
        while index < len(candidates):
            if candidates[index] > target:
                break
            target -= candidates[index]
            now_choose.append(candidates[index])
            self.dfs(candidates, target, index + 1, next_pos, now_choose, res)
            now_choose.pop()
            target += candidates[index]
            index = next_pos[index]
```
