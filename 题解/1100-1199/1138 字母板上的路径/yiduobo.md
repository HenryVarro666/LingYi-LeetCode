---
title: "1138. 字母板上的路径"
aliases: ["yiduobo的每日leetcode 1138.字母板上的路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376861005"
zhihu_id: "376861005"
zhihu_title: "yiduobo的每日leetcode 1138.字母板上的路径"
question_id: "1138"
question: "字母板上的路径"
problem_url: "https://leetcode.cn/problems/alphabet-board-path/"
difficulty: "Medium"
created: "2021-05-31T23:37:20+08:00"
updated: "2021-05-31T23:37:20+08:00"
upvotes: 0
comments: 0
---

# 1138. 字母板上的路径

> **[yiduobo的每日leetcode 1138.字母板上的路径](https://zhuanlan.zhihu.com/p/376861005) · 知乎 · 2021-05-31 · 赞同 0**
> 力扣：[1138. 字母板上的路径](https://leetcode.cn/problems/alphabet-board-path/) · Medium · 灵茶山艾府：[注意 z 的位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1138.字母板上的路径

[力扣](https://leetcode-cn.com/problems/alphabet-board-path/)

首先，如果将字母a到z按0到25进行编码的话，那么很快就能找到每个编码与其在字母板上坐标的对应关系。对于编码为num的字母，由于一行有5个字母，因此所在行row \= num / 5，其所在列col \= num % 5。

有了行列信息之后，就可以很快得到从一个字母到另一个字母所需要的指令列表的。不妨设当前位于(nowx, nowy)，需要移动到(x, y)，那么：

1、若nowx > x，说明需要向上移动，距离为nowx - x，因此需要序列'U' \* (nowx - x)。同理，若nowx \< x，说明需要向下移动，距离为x - nowx，因此需要序列'D' \* (x - nowx)。

2、若nowy > y，说明需要向左移动，距离为nowy - x，因此需要序列'L' \* (nowy - y)。同理，若nowy \< y，说明需要向右移动，距离为y - nowy，因此需要序列'R' \* (y - nowy)。

接下来需要将行和列所需的指令序列合并起来。需要注意的是，这里的字母板并不规整，如果从某个字母到z的话，应当先移动列，再移动行。同样地，从z往别的字母移动时则应当先移动行，再移动列。对于非z字母之间的移动，行列的顺序则无所谓。

根据上面的计算方法，逐个枚举target中的字母生成对应的指令序列即可。

最后附上python代码：

```python
class Solution(object):
    def alphabetBoardPath(self, target):
        """
        :type target: str
        :rtype: str
        """

        nowx = 0
        nowy = 0
        res = ''
        for char in target:
            num = ord(char) - 97
            x = num / 5
            y = num % 5

            if nowy > y:
                h = 'L' * (nowy - y)
            else:
                h = 'R' * (y - nowy)
            

            if nowx > x:
                v = 'U' * (nowx - x)
            else:
                v = 'D' * (x - nowx)

            if nowx == 5:
                res += v
                res += h
            else:
                res += h
                res += v

            nowx = x
            nowy = y
            res += '!'
        
        return res
```
