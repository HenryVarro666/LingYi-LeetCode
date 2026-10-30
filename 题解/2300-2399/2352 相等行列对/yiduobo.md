---
title: "2352. 相等行列对"
aliases: ["yiduobo的每日leetcode 2352.相等行列对"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561248814"
zhihu_id: "561248814"
zhihu_title: "yiduobo的每日leetcode 2352.相等行列对"
question_id: "2352"
question: "相等行列对"
problem_url: "https://leetcode.cn/problems/equal-row-and-column-pairs/"
difficulty: "Medium"
created: "2022-09-05T00:34:21+08:00"
updated: "2022-09-05T00:34:21+08:00"
upvotes: 1
comments: 0
---

# 2352. 相等行列对

> **[yiduobo的每日leetcode 2352.相等行列对](https://zhuanlan.zhihu.com/p/561248814) · 知乎 · 2022-09-05 · 赞同 1**
> 力扣：[2352. 相等行列对](https://leetcode.cn/problems/equal-row-and-column-pairs/) · Medium · 灵茶山艾府：[哈希表（Python 两行）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2352.相等行列对

[力扣](https://leetcode.cn/problems/equal-row-and-column-pairs/)

题目给出一个n \* n的矩阵，要求找出矩阵中相等的行列对的数目。由于n的规模比较小，在这里可以直接暴力枚举行和列然后进行判断，也可以先枚举行，将行加入到哈希表中然后再枚举列，利用哈希表来进行判断。

我在这里采用的是trie树，同样是枚举行，将行视为字符串，每个格子上的数字视为字符，然后将其加入到trie树中。接下来再枚举列，通过trie树判断与其相同的行的数目并更新答案。

最后附上python代码：

```python
class Node(object):

    def __init__(self):
        self.childs = {}
        self.weight = 0

class Solution(object):
    def equalPairs(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        n = len(grid)
        root = Node()
        for i in range(n):
            now = root
            for j in range(n):
                if grid[i][j] not in now.childs:
                    now.childs[grid[i][j]] = Node()
                now = now.childs[grid[i][j]]
            
            now.weight += 1
        
        res = 0
        for j in range(n):
            now = root
            for i in range(n):
                if grid[i][j] not in now.childs:
                    break
                now = now.childs[grid[i][j]]
            
            res += now.weight
        
        return res
```
