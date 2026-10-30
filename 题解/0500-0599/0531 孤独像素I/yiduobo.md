---
title: "531. 孤独像素I"
aliases: ["yiduobo的每日leetcode 531.孤独像素I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600680425"
zhihu_id: "600680425"
zhihu_title: "yiduobo的每日leetcode 531.孤独像素I"
question_id: "531"
question: "孤独像素I"
problem_url: "https://leetcode.cn/problems/lonely-pixel-i/"
created: "2023-01-24T01:23:16+08:00"
updated: "2023-01-24T01:23:16+08:00"
upvotes: 0
comments: 0
---

# 531. 孤独像素I

> **[yiduobo的每日leetcode 531.孤独像素I](https://zhuanlan.zhihu.com/p/600680425) · 知乎 · 2023-01-24 · 赞同 0**
> 力扣：[531. 孤独像素I](https://leetcode.cn/problems/lonely-pixel-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

531.孤独像素I

[力扣](https://leetcode.cn/problems/lonely-pixel-i/)

题目对于孤独像素的定义为行和列中唯一的黑色像素，那么可以先遍历整个图片，使用两个数组统计每一行和每一列中黑色像素的数量，接下来再遍历整个图片，对于每个单元格，若其为黑色像素，且其所在行和所在列都只有一个黑色像素，那么该单元格上就是一个孤独像素，此时就应该更新答案。

最后附上python代码：

```python
class Solution(object):
    def findLonelyPixel(self, picture):
        """
        :type picture: List[List[str]]
        :rtype: int
        """

        m = len(picture)
        n = len(picture[0])
        row = [0] * m
        col = [0] * n

        for i in range(m):
            for j in range(n):
                if picture[i][j] == 'B':
                    row[i] += 1
                    col[j] += 1
        
        res = 0
        for i in range(m):
            for j in range(n):
                if picture[i][j] == 'B' and row[i] == 1 and col[j] == 1:
                    res += 1
        
        return res
```
