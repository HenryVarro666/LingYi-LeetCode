---
title: "3175. 找出连续赢K场比赛的第一位玩家"
aliases: ["yiduobo的每日leetcode 3175.找出连续赢K场比赛的第一位玩家"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705647575"
zhihu_id: "705647575"
zhihu_title: "yiduobo的每日leetcode 3175.找出连续赢K场比赛的第一位玩家"
question_id: "3175"
question: "找到连续赢 K 场比赛的第一位玩家"
problem_url: "https://leetcode.cn/problems/find-the-first-player-to-win-k-games-in-a-row/"
difficulty: "Medium"
created: "2024-06-27T01:01:30+08:00"
updated: "2024-06-27T01:01:30+08:00"
upvotes: 1
comments: 0
---

# 3175. 找出连续赢K场比赛的第一位玩家

> **[yiduobo的每日leetcode 3175.找出连续赢K场比赛的第一位玩家](https://zhuanlan.zhihu.com/p/705647575) · 知乎 · 2024-06-27 · 赞同 1**
> 力扣：[3175. 找到连续赢 K 场比赛的第一位玩家](https://leetcode.cn/problems/find-the-first-player-to-win-k-games-in-a-row/) · Medium · 灵茶山艾府：[打擂台（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3175.找出连续赢K场比赛的第一位玩家

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-first-player-to-win-k-games-in-a-row/description/)

题目给出一个长度为n，且其中元素值各不相同的数组skills，其中skills[i]表示第i位玩家的技能等级。所有玩家按照编号0到n - 1的顺序排成一列，接下来每一轮，队首的两个玩家进行比赛，技能等级高的玩家获胜，保持原位置不变，而败者则移动到队伍的末尾。问哪位玩家可以最先连续赢得k场比赛。

由于最终答案必然处于队列的首位，不妨设当前队首玩家的编号为index，而index在碰到index后方且比skills[index]的玩家时将会落败，即skills[index]的下一个更大元素。对于这个问题，可以使用单调栈进行预处理，具体可以参考之前的496题。

[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)

令f[index]表示skills[index]下一个更大元素在skills数组中的下标，那么对于f[index]：

1、f[index]不存在：

由于index是队首元素，说明在之前的比赛中所有人都比不过index，而此时f[index]不存在则说明在原始skills数组中，index后方的玩家，也就是还没有参加过比赛的所有玩家也比不过index，即skills[index]是数组中的最大值，此时的答案显然就是index

2、f[index]存在：

那么对于index + 1到f[index] - 1，一共f[index] - index - 1个玩家，他们仍然会输给index，而index则会输给f[index]。

若此时的index等于0，且f[index] - index - 1 >\= k，那么0就是最终答案。

若此时的index不等于0，且f[index] - index - 1 >\= k - 1，那么index就是最终答案。这里只需要赢过后面的k - 1个玩家的理由是在index成为队列头部之前，其必然与原来的队列头部进行过一次比赛并获胜，因此只需要赢过后面的k - 1个玩家。

若上面两点都不满足，那么index将输给f[index]，新的队列头部将变为f[index]，此时就应该将index更新为f[index]然后重复上面的过程。

最后附上python代码：

```python
class Solution(object):
    def findWinningPlayer(self, skills, k):
        """
        :type skills: List[int]
        :type k: int
        :rtype: int
        """

        n = len(skills)
        f = [-1] * n
        stack = []
        for index, v in enumerate(skills):
            while stack and skills[stack[-1]] < v:
                f[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        index = 0
        while f[index] != -1 and f[index] - index - 1 < k:
            if index == 0:
                k -= 1
            index = f[index]
        
        return index
```
