---
title: "2055. 蜡烛之间的盘子"
aliases: ["yiduobo的每日leetcode 2055.蜡烛之间的盘子"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/512983527"
zhihu_id: "512983527"
zhihu_title: "yiduobo的每日leetcode 2055.蜡烛之间的盘子"
question_id: "2055"
question: "蜡烛之间的盘子"
problem_url: "https://leetcode.cn/problems/plates-between-candles/"
difficulty: "Medium"
rating: 1819
created: "2022-05-11T23:55:40+08:00"
updated: "2022-05-12T02:14:42+08:00"
upvotes: 0
comments: 0
---

# 2055. 蜡烛之间的盘子

> **[yiduobo的每日leetcode 2055.蜡烛之间的盘子](https://zhuanlan.zhihu.com/p/512983527) · 知乎 · 2022-05-11 · 赞同 0**
> 力扣：[2055. 蜡烛之间的盘子](https://leetcode.cn/problems/plates-between-candles/) · Medium · 灵茶山艾府：[线性做法：前缀和+每个位置的最近蜡烛](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2055.蜡烛之间的盘子

[力扣](https://leetcode.cn/problems/plates-between-candles/)

题目给出若干组询问，对于一组询问[x, y]，要求找出x到y之间的子字符串中处于两根蜡烛之间的盘子的数量。

对于一组询问[x, y]：

1、若区间内蜡烛的数目不足两根，那么答案必然为0

2、若蜡烛数量大于等于两根，设x右侧第一根蜡烛的位置为right[x]，那么x到right[x]之间的所有盘子左侧都是没有蜡烛的，这些蜡烛不能加入到答案中。同样的，设y左侧第一根蜡烛的位置为left[y]，那么left[y]到y之间的所有盘子右侧都是没有蜡烛的。除此之外，在right[x]到left[y]之间的盘子都可以加入到答案中。

从right[x]到left[y]之间一共有left[y] - right[x] + 1个物件，设其中有cnt个蜡烛，那么剩下的盘子数量就是left[y] - right[x] + 1 - cnt，也就是要求的最后答案。

对于上面的问题，可以发现有三个子问题需要求解：

1、某个位置x右侧第一根蜡烛的位置right[x]。对于这个问题，可以从右向左一趟遍历，对于当前位置index，如果是一根蜡烛，那么就有right[index] \= index，否则就有right[index] \= right[index + 1]

2、某个位置y左侧第一根蜡烛的位置left[y]。对于这个问题，可以从左向右一趟遍历，对于当前位置index，如果是一根蜡烛，那么就有left[index] \= index，否则就有left[index] \= left[index - 1]

3、区间[x, y]之间的蜡烛数目。这是经典的区间和问题，可以转化为前缀和求解

根据上面的结论，就可以通过几次遍历分别求出left、right以及前缀和数组，就下来就可以通过最上面给出的做法求解了。

最后附上python代码：

```python
class Solution(object):
    def platesBetweenCandles(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(s)

        left = []
        for index in range(n):
            if s[index] == '|':
                left.append(index)
            elif index == 0:
                left.append(-1)
            else:
                left.append(left[-1])
        
        right = []
        for index in range(n - 1, -1, -1):
            if s[index] == '|':
                right.append(index)
            elif index == n - 1:
                right.append(-1)
            else:
                right.append(right[-1])
        right.reverse()

        if s[0] == '|':
            cnt = [1]
        else:
            cnt = [0]
        
        for char in s[1:]:
            cnt.append(cnt[-1])
            if char == '|':
                cnt[-1] += 1
        
        res = []
        for x, y in queries:
            now = cnt[y]
            if x > 0:
                now -= cnt[x - 1]
            
            if now < 2:
                res.append(0)
            else:
                res.append(left[y] - right[x] + 1 - now)
        
        return res
```
