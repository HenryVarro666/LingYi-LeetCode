---
title: "2397. 被列覆盖的最多行数"
aliases: ["yiduobo的每日leetcode 2397.被列覆盖的最多行数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/enumeration", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/566510307"
zhihu_id: "566510307"
zhihu_title: "yiduobo的每日leetcode 2397.被列覆盖的最多行数"
question_id: "2397"
question: "被列覆盖的最多行数"
problem_url: "https://leetcode.cn/problems/maximum-rows-covered-by-columns/"
difficulty: "Medium"
rating: 1719
created: "2022-09-20T23:29:34+08:00"
updated: "2022-09-20T23:29:34+08:00"
upvotes: 0
comments: 0
---

# 2397. 被列覆盖的最多行数

> **[yiduobo的每日leetcode 2397.被列覆盖的最多行数](https://zhuanlan.zhihu.com/p/566510307) · 知乎 · 2022-09-20 · 赞同 0**
> 力扣：[2397. 被列覆盖的最多行数](https://leetcode.cn/problems/maximum-rows-covered-by-columns/) · Medium · 灵茶山艾府：[两种方法：二进制枚举 / Gosper's Hack（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2397.被列覆盖的最多行数

[力扣](https://leetcode.cn/problems/maximum-rows-covered-by-columns/)

没有什么特别好的思路，不过题目中列的总数不超过12，那么完全可以直接暴力dfs，枚举每一种选取列的方式，然后计算当前选取方式下能覆盖多少行。对于这一步计算，则可以利用状态压缩来进行优化，即优先预处理出每一行需要哪些列来进行覆盖，将对应列的状态压缩后的表示储存起来。当dfs过程中枚举到某一种列的组合时，就只需要遍历每一行，判断其对应列的状态压缩表示是否为当前枚举到的列的状态表示的子集即可。

最后附上python代码：

```python
class Solution(object):
    def maximumRows(self, mat, cols):
        """
        :type mat: List[List[int]]
        :type cols: int
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])

        need = []
        for i in range(m):
            now = 0
            for j in range(n):
                if mat[i][j] == 1:
                    now += (1 << j)
            need.append(now)
        
        self.res = 0
        
        def dfs(now, used, level):
            if used == cols:
                cnt = 0
                for index in range(m):
                    if (now & need[index]) == need[index]:
                        cnt += 1
                self.res = max(self.res, cnt)
                return 
            
            if level == n:
                return
            
            dfs(now, used, level + 1)
            dfs(now | (1 << level), used + 1, level + 1)

        dfs(0, 0, 0)
        return self.res
```
