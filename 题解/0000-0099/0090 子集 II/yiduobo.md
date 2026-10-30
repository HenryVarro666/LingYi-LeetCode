---
title: "90. 子集II"
aliases: ["yiduobo的每日leetcode 90.子集II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/136522899"
zhihu_id: "136522899"
zhihu_title: "yiduobo的每日leetcode 90.子集II"
question_id: "90"
question: "子集 II"
problem_url: "https://leetcode.cn/problems/subsets-ii/"
difficulty: "Medium"
created: "2020-04-26T21:51:14+08:00"
updated: "2020-04-26T21:51:14+08:00"
upvotes: 0
comments: 0
---

# 90. 子集II

> **[yiduobo的每日leetcode 90.子集II](https://zhuanlan.zhihu.com/p/136522899) · 知乎 · 2020-04-26 · 赞同 0**
> 力扣：[90. 子集 II](https://leetcode.cn/problems/subsets-ii/) · Medium · 灵茶山艾府：[两种方法：选或不选/枚举选哪个（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

90.子集II <https://leetcode-cn.com/problems/subsets-ii/>

78题的升级版本（传送门在这里[yiduobo：yiduobo的每日leetcode 78.子集](https://zhuanlan.zhihu.com/p/133839160)）。

还是类似的处理方法，记录下上一轮操作的位置，然后这一轮从这个位置开始继续往后做。由于nums中的数可以重复，因此还需要用一个dict来记录当前情况下每个数使用了几次。

最后附上python代码：

```python
class Solution(object):
    def subsetsWithDup(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        res = []
        count_dict = {}
        for num in nums:
            count_dict[num] = count_dict.get(num, 0) + 1

        self.dfs(count_dict.keys(), count_dict, [], res)
        return res

    def dfs(self, candidate, count_dict, now, res):
        res.append(now[:])

        for index, num in enumerate(candidate):
            if count_dict[num] > 0:
                count_dict[num] -= 1
                now.append(num)
                self.dfs(candidate[index:], count_dict, now, res)
                now.pop()
                count_dict[num] += 1
```
