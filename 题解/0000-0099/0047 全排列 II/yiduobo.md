---
title: "47. 全排列II"
aliases: ["yiduobo的每日leetcode 47.全排列II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/125766510"
zhihu_id: "125766510"
zhihu_title: "yiduobo的每日leetcode 47.全排列II"
question_id: "47"
question: "全排列 II"
problem_url: "https://leetcode.cn/problems/permutations-ii/"
difficulty: "Medium"
created: "2020-04-05T23:24:02+08:00"
updated: "2020-04-05T23:24:02+08:00"
upvotes: 0
comments: 0
---

# 47. 全排列II

> **[yiduobo的每日leetcode 47.全排列II](https://zhuanlan.zhihu.com/p/125766510) · 知乎 · 2020-04-05 · 赞同 0**
> 力扣：[47. 全排列 II](https://leetcode.cn/problems/permutations-ii/) · Medium · 灵茶山艾府：[如何避免重复的排列？（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

47.全排列II <https://leetcode-cn.com/problems/permutations-ii/>

与上一题差不多的做法，不过要想不重复的话就必须保证同一轮的迭代中不能选择相同的数字，于是我们可以统计出每个数字出现的次数，然后每轮检查每个不同的数字。

如果当前数字剩余的可用次数大于0，那么选择这个数字并进行下一轮迭代，否则继续往后检测下一个数字。

若每个数字可用次数都为0，说明已经生成了一个可行的解，将其加入到res中并返回即可。

最后附上python代码，其中nums_count字典表示每个数字剩余的可用次数：

```python
class Solution(object):
    def permuteUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        nums_count = {}
        for num in nums:
            nums_count[num] = nums_count.get(num, 0) + 1

        res = []

        self.dfs(nums_count, [], res)
        return res

    def dfs(self, nums_count, now, res):
        rest_flag = True

        for num in nums_count:
            if nums_count[num] > 0:
                now.append(num)
                nums_count[num] -= 1
                self.dfs(nums_count, now, res)
                nums_count[num] += 1
                now.pop()
                rest_flag = False
            
        if rest_flag:
            res.append(now[:])
```
