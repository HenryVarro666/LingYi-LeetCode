---
title: "3847. 计算比赛分数差"
aliases: ["yiduobo的每日leetcode 3847.计算比赛分数差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011483896718595143"
zhihu_id: "2011483896718595143"
zhihu_title: "yiduobo的每日leetcode 3847.计算比赛分数差"
question_id: "3847"
question: "计算比赛分数差"
problem_url: "https://leetcode.cn/problems/find-the-score-difference-in-a-game/"
difficulty: "Medium"
created: "2026-03-02T22:08:22+08:00"
updated: "2026-03-02T22:08:23+08:00"
upvotes: 1
comments: 0
---

# 3847. 计算比赛分数差

> **[yiduobo的每日leetcode 3847.计算比赛分数差](https://zhuanlan.zhihu.com/p/2011483896718595143) · 知乎 · 2026-03-02 · 赞同 1**
> 力扣：[3847. 计算比赛分数差](https://leetcode.cn/problems/find-the-score-difference-in-a-game/) · Medium · 灵茶山艾府：[模拟，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3847.计算比赛分数差

<https://leetcode.cn/problems/find-the-score-difference-in-a-game/description/>

题目给出一个整数数组nums，其中nums[index]表示在第index场比赛中获得的分数。

现在有两位玩家参与比赛，初始状态下，第一位玩家为主动玩家，第二位玩家为被动玩家。

接下来按顺序进行所有的比赛，对于第index场比赛：

- 若nums[index]为奇数，那么主动玩家和被动玩家互换角色
- 每第6场比赛，也就是index为5、11、17、...的比赛中，主动玩家和被动玩家互换角色
- 主动玩家将参与这场比赛，并得到nums[index]的分数

问所有比赛完成后，第一位玩家和第二位玩家的总分之差。

由于题目需要计算的是第一位玩家和第二位玩家的总分之差，因此可以使用一个标记变量sign来表示目前是谁在进行比赛。当sign为1时，表示第一位玩家是主动玩家，当sign为-1时，则表示第二位玩家是主动玩家。这样一来，只需将sign与当前比赛的分数相乘，就得到了本场比赛对答案的影响。

于是只需一趟遍历，根据当前比赛分数的奇偶性以及当前比赛的索引来修正sign，然后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def scoreDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        sign = 1
        for index, v in enumerate(nums):
            if v % 2 == 1:
                sign *= -1
            if index % 6 == 5:
                sign *= -1
            
            res += v * sign
        
        return res
```
