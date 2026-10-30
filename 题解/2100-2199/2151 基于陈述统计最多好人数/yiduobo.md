---
title: "2151. 基于陈述统计最多好人数"
aliases: ["yiduobo的每日leetcode 2151.基于陈述统计最多好人数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/enumeration", "leetcode/er-jin-zhi", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/530619535"
zhihu_id: "530619535"
zhihu_title: "yiduobo的每日leetcode 2151.基于陈述统计最多好人数"
question_id: "2151"
question: "基于陈述统计最多好人数"
problem_url: "https://leetcode.cn/problems/maximum-good-people-based-on-statements/"
difficulty: "Hard"
rating: 1980
created: "2022-06-18T16:17:25+08:00"
updated: "2022-06-18T16:17:25+08:00"
upvotes: 0
comments: 0
---

# 2151. 基于陈述统计最多好人数

> **[yiduobo的每日leetcode 2151.基于陈述统计最多好人数](https://zhuanlan.zhihu.com/p/530619535) · 知乎 · 2022-06-18 · 赞同 0**
> 力扣：[2151. 基于陈述统计最多好人数](https://leetcode.cn/problems/maximum-good-people-based-on-statements/) · Hard · 灵茶山艾府：[二进制枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2151.基于陈述统计最多好人数

[力扣](https://leetcode.cn/problems/maximum-good-people-based-on-statements/)

没有什么特别好的想法，不过注意到题目中n的规模很小，那么完全可以枚举出所有的情况，一共是2^15\=32768种。由于好人一定说真话，坏人可能说真话可能说假话，那么实际上可以完全不理会坏人，只需要判断每种情况况下好人说的话是否与当前的情况相符就能确认当前情况是否可能成立，并使用好人的数目来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maximumGood(self, statements):
        """
        :type statements: List[List[int]]
        :rtype: int
        """

        n = len(statements)

        def dfs(now):
            if len(now) == n:
                cnt = 0
                for i in range(n):
                    if now[i] == 1:
                        for j in range(n):
                            if statements[i][j] == 2:
                                continue
                            if statements[i][j] != now[j]:
                                return 0

                        cnt += 1

                return cnt

            now.append(0)
            res = dfs(now)
            now[-1] = 1
            res = max(res, dfs(now))
            now.pop()
            return res
        
        return dfs([])
```
