---
title: "2056. 棋盘上有效移动组合的数目"
aliases: ["yiduobo的每日leetcode 2056.棋盘上有效移动组合的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/backtracking", "leetcode/simulation", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/编程能力强化训练", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/512990884"
zhihu_id: "512990884"
zhihu_title: "yiduobo的每日leetcode 2056.棋盘上有效移动组合的数目"
question_id: "2056"
question: "棋盘上有效移动组合的数目"
problem_url: "https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard/"
difficulty: "Hard"
rating: 2611
created: "2022-05-12T00:02:05+08:00"
updated: "2022-05-12T00:04:00+08:00"
upvotes: 0
comments: 0
---

# 2056. 棋盘上有效移动组合的数目

> **[yiduobo的每日leetcode 2056.棋盘上有效移动组合的数目](https://zhuanlan.zhihu.com/p/512990884) · 知乎 · 2022-05-12 · 赞同 0**
> 力扣：[2056. 棋盘上有效移动组合的数目](https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard/) · Hard · 灵茶山艾府：[回溯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2056.棋盘上有效移动组合的数目

[力扣](https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard/)

没有什么好的想法，不过题目中最多只有四颗棋子，而对于活动范围最大的皇后，在8 \* 8的棋盘中的移动范围也只有不到30个位置，因此可以先计算出每颗棋子的所有的目的地，然后枚举每一种组合，最后的组合总数也就不到30^4。对于枚举到的最终情况，则可以从起始状况一步一步开始模拟，判断在棋子移动的过程中是否会出现棋子在某一时刻走到同一位置引起冲突的情况，若能顺利走到目的地，就将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def countCombinations(self, pieces, positions):
        """
        :type pieces: List[str]
        :type positions: List[List[int]]
        :rtype: int
        """

        dx = {}
        dy = {}

        dx[0] = [1, 0, -1, 0]
        dy[0] = [0, -1, 0, 1]

        dx[1] = [1, 1, 0, -1, -1, -1, 0, 1]
        dy[1] = [0, -1, -1, -1, 0, 1, 1, 1]

        dx[2] = [1, -1, -1, 1]
        dy[2] = [-1, -1, 1, 1]

        final_target = []
        n = len(pieces)

        for index in range(n):
            final_target.append([])
            final_target[-1].append(positions[index])
            if pieces[index] == "rook":
                type = 0
            elif pieces[index] == "queen":
                type = 1
            else:
                type = 2
            
            for d in range(len(dx[type])):
                nowx, nowy = positions[index]
                while True:
                    nowx += dx[type][d]
                    nowy += dy[type][d]
                    if nowx == 0 or nowy == 0 or nowx == 9 or nowy == 9:
                        break
                    final_target[-1].append([nowx, nowy])
        
        self.res = 0
        self.dfs(0, n, [], final_target, positions)
        return self.res

    def check(self, n, origin, final):
        at_pos = 0
        nowx = []
        nowy = []
        for index in range(n):
            if origin[index][0] == final[index][0] and origin[index][1] == final[index][1]:
                at_pos += 1
            nowx.append(origin[index][0])
            nowy.append(origin[index][1])
        
        while at_pos < n:
            used = set()
            at_pos = 0
            for index in range(n):
                at_pos_flag = True

                if nowx[index] != final[index][0]:
                    at_pos_flag = False
                    if nowx[index] > final[index][0]:
                        nowx[index] -= 1
                    else:
                        nowx[index] += 1

                if nowy[index] != final[index][1]:
                    at_pos_flag = False
                    if nowy[index] > final[index][1]:
                        nowy[index] -= 1
                    else:
                        nowy[index] += 1
                
                if at_pos_flag:
                    at_pos += 1

                key = (nowx[index] - 1) * 8 + nowy[index]
                if key not in used:
                    used.add(key)
                else:
                    return False
        
        return True

    def dfs(self, level, n, now, final_target, positions):
        if level == n:
            if self.check(n, positions, now):
                self.res += 1
            return

        for pos in final_target[level]:
            now.append(pos)
            self.dfs(level + 1, n, now, final_target, positions)
            now.pop()
```
