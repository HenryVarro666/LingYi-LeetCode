---
title: "3248. 矩阵中的蛇"
aliases: ["yiduobo的每日leetcode 3248.矩阵中的蛇"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721492608"
zhihu_id: "721492608"
zhihu_title: "yiduobo的每日leetcode 3248.矩阵中的蛇"
question_id: "3248"
question: "矩阵中的蛇"
problem_url: "https://leetcode.cn/problems/snake-in-matrix/"
difficulty: "Easy"
created: "2024-09-23T00:31:48+08:00"
updated: "2024-09-23T00:31:48+08:00"
upvotes: 0
comments: 0
---

# 3248. 矩阵中的蛇

> **[yiduobo的每日leetcode 3248.矩阵中的蛇](https://zhuanlan.zhihu.com/p/721492608) · 知乎 · 2024-09-23 · 赞同 0**
> 力扣：[3248. 矩阵中的蛇](https://leetcode.cn/problems/snake-in-matrix/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3248.矩阵中的蛇

[. - 力扣（LeetCode）](https://leetcode.cn/problems/snake-in-matrix/description/)

题目给出一个大小为n \* n的矩阵，其中第i行第j列的单元格编号为i \* n + j。矩阵中有一条蛇，初始位于单元格0，接下来给出一个字符串数组commands，表示蛇接下来会按照指令行动。指令包含up、down、left和right，分别表示蛇往上、下、左、右移动一格。题目保证蛇始终处于矩阵内，问蛇最终处于哪个单元格。

蛇一开始处于坐标(0, 0)，接下来只需根据commands模拟蛇在矩阵中的行动，得到蛇最终的下标，然后计算出下标对应的单元格编号即可。

最后附上python代码：

```python
class Solution(object):
    def finalPositionOfSnake(self, n, commands):
        """
        :type n: int
        :type commands: List[str]
        :rtype: int
        """

        x, y = 0, 0
        for c in commands:
            if c == 'UP':
                x -= 1
            elif c == 'DOWN':
                x += 1
            elif c == 'LEFT':
                y -= 1
            else:
                y += 1
        
        return x * n + y
```
