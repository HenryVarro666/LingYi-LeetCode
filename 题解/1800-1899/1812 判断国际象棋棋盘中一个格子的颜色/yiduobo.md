---
title: "1812. 判断国际象棋棋盘中一个格子的颜色"
aliases: ["yiduobo的每日leetcode 1812.判断国际象棋棋盘中一个格子的颜色"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464721211"
zhihu_id: "464721211"
zhihu_title: "yiduobo的每日leetcode 1812.判断国际象棋棋盘中一个格子的颜色"
question_id: "1812"
question: "判断国际象棋棋盘中一个格子的颜色"
problem_url: "https://leetcode.cn/problems/determine-color-of-a-chessboard-square/"
difficulty: "Easy"
created: "2022-02-07T22:01:29+08:00"
updated: "2022-02-07T22:01:29+08:00"
upvotes: 0
comments: 0
---

# 1812. 判断国际象棋棋盘中一个格子的颜色

> **[yiduobo的每日leetcode 1812.判断国际象棋棋盘中一个格子的颜色](https://zhuanlan.zhihu.com/p/464721211) · 知乎 · 2022-02-07 · 赞同 0**
> 力扣：[1812. 判断国际象棋棋盘中一个格子的颜色](https://leetcode.cn/problems/determine-color-of-a-chessboard-square/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1812.判断国际象棋棋盘中一个格子的颜色

[力扣](https://leetcode-cn.com/problems/determine-color-of-a-chessboard-square/)

比较基础的题目，可以通过奇偶性很快得到答案。假设棋盘的列也是从1到8编号对应a到h，那么行和列相加为偶数时对应的格子为黑色，否则为白色。

最后附上python代码，我在这里写的ord是取a到h的ascii码，其奇偶性与1到8恰好相同：

```python
class Solution(object):
    def squareIsWhite(self, coordinates):
        """
        :type coordinates: str
        :rtype: bool
        """

        return (ord(coordinates[0]) + int(coordinates[1])) % 2 == 1
```
