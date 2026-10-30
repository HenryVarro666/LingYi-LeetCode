---
title: "2672. 有相同颜色的相邻元素数目"
aliases: ["yiduobo的每日leetcode 2672.有相同颜色的相邻元素数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649066843"
zhihu_id: "649066843"
zhihu_title: "yiduobo的每日leetcode 2672.有相同颜色的相邻元素数目"
question_id: "2672"
question: "有相同颜色的相邻元素数目"
problem_url: "https://leetcode.cn/problems/number-of-adjacent-elements-with-the-same-color/"
difficulty: "Medium"
created: "2023-08-09T22:50:47+08:00"
updated: "2023-08-09T22:50:47+08:00"
upvotes: 0
comments: 0
---

# 2672. 有相同颜色的相邻元素数目

> **[yiduobo的每日leetcode 2672.有相同颜色的相邻元素数目](https://zhuanlan.zhihu.com/p/649066843) · 知乎 · 2023-08-09 · 赞同 0**
> 力扣：[2672. 有相同颜色的相邻元素数目](https://leetcode.cn/problems/number-of-adjacent-elements-with-the-same-color/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2672.有相同颜色的相邻元素数目

[力扣](https://leetcode.cn/problems/number-of-adjacent-elements-with-the-same-color/description/)

由于题目需要计算的是相同颜色相邻元素的数目，那么每次修改颜色的操作实际上只会影响到修改的位置以及与该位置相邻位置的配对。

更具体的：

1、若修改的位置本身有颜色，且这个颜色与该位置左侧位置的颜色相同，那么在修改后配对的数目应该减去1。同样的，若该位置右侧位置的颜色也与该位置修改前的颜色相同，那么在修改后也应该将配对的数目减去1。

2、若修改后该位置的新颜色与其左侧位置的颜色相同，那么配对的数目应该加上1。同样的，若该位置的新颜色与其右侧位置的颜色相同，那么配对的数目也应该加上1。

根据上面的结论，就只需要一趟遍历，每次修改时都在上一次修改的基础上计算配对数的变化。

最后附上python代码：

```python
class Solution(object):
    def colorTheArray(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        color = [0] * n
        res = []
        now = 0
        for index, c in queries:
            if color[index] > 0:
                if index > 0 and color[index] == color[index - 1]:
                    now -= 1
                if index < n - 1 and color[index] == color[index + 1]:
                    now -= 1
            
            color[index] = c
            if index > 0 and color[index] == color[index - 1]:
                now += 1
            if index < n - 1 and color[index] == color[index + 1]:
                now += 1
            
            res.append(now)
        
        return res
```
