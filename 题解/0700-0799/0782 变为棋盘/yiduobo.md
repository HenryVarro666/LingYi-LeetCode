---
title: "782. 变为棋盘"
aliases: ["yiduobo的每日leetcode 782.变为棋盘"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/340743726"
zhihu_id: "340743726"
zhihu_title: "yiduobo的每日leetcode 782.变为棋盘"
question_id: "782"
question: "变为棋盘"
problem_url: "https://leetcode.cn/problems/transform-to-chessboard/"
difficulty: "Hard"
created: "2020-12-30T23:41:15+08:00"
updated: "2020-12-30T23:41:15+08:00"
upvotes: 0
comments: 0
---

# 782. 变为棋盘

> **[yiduobo的每日leetcode 782.变为棋盘](https://zhuanlan.zhihu.com/p/340743726) · 知乎 · 2020-12-30 · 赞同 0**
> 力扣：[782. 变为棋盘](https://leetcode.cn/problems/transform-to-chessboard/) · Hard · 灵茶山艾府：[【图解】逆向思维（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

782.变为棋盘

[力扣](https://leetcode-cn.com/problems/transform-to-chessboard/)

题目虽然看上去错综复杂的样子，但实际上仔细观察可以发现：

1、横竖操作之间互不影响

2、如果将一行的01看做二进制的01串，那么所有行的分布只能与第0行row[0]完全一致，或者与row[0]逐位相反，即为11...11^row。同时，与row[0]一致的行的数量必须等于n / 2或者(n + 1) / 2，这里的除法向下取整。

3、结论2在列上也成立。

这里简单说明一下结论2和3。对于最终结果中的每一行，设其行数为k，那么与k同奇偶的行其排布必须与第k行完全一致，而奇偶相反的行则的排序则必须与第k行逐位相反。若存在某一行，其即不与row[0]一致，也不是与row[0]逐位相反，那么无论怎么调整列，其都不可能与row[0]一致或者与row[0]逐位相反，因此最终在棋盘上没有该行可以放置的位置。

由于行列完全等价，因此这个结论在列上也成立。

有了上面的结论，我们就可以分别处理行和列，判断每一行是否满足与row[0]完全一致或者逐位相反，并统计数量。由于这里n的大小最大为30，因此可以使用2进制来压缩一行或者一列的分布情况。

统计完成后，若没有预料之外的行和列，且数量达标的话，就可以开始想办法将棋盘调整到最终状态。

这里对于n的奇偶性需要进行分别讨论，因为当n为偶数时，第0行既可以是0101..01这种形式，也可以是1010..10这种形式。而当n为奇数时，则需要选择对比与row[0]一致的行的数量row_cnt，以及逐位相反的数量n - row_cnt二者的大小，选择较大的一方作为最终的第0行。

为了写起来方便，这里可以判断row_cnt是否等于n / 2，若等于则选择row[0]取反，否则选择row[0]作为首行。对于n为奇数的情况，这是必然的选择，而对于n为偶数的情况，假设我们选择row[0]为首行时对列进行res次调整，那么选择row[0]取反作为首行时对列就需要进行n / 2 - res次调整，我们只需在二者中取较小值即可。

选定了最终作为首行的目标行target之后，我们可以从0开始按两行一个step往下进行遍历，若当前行不等于target，那么就需要对行执行一次交换操作。统计这个次数就是行需要进行交换的次数。

对于列的操作与行完全一致。

计算出res_row和res_col之后，若n为奇数，则直接返回二者之和，否则需要执行上面说的分别与n / 2 - res_row以及n / 2 - res_col取较小值，然后返回二者之和。

最后附上python代码：

```python
class Solution(object):
    def movesToChessboard(self, board):
        """
        :type board: List[List[int]]
        :rtype: int
        """

        m = len(board)

        row = []
        col = []
        for i in range(m):
            row.append(0)
            for j in range(m):
                row[-1] = (row[-1] << 1) + board[i][j]
        
        for j in range(m):
            col.append(0)
            for i in range(m):
                col[-1] = (col[-1] << 1) + board[i][j]

        cnt_row = cnt_col = 1
        for index in range(1, m):
            if row[index] == row[0]:
                cnt_row += 1
            elif row[index] ^ row[0] != (1 << m) - 1:
                return -1
            
            if col[index] == col[0]:
                cnt_col += 1
            elif col[index] ^ col[0] != (1 << m) - 1:
                return -1

        res_row = res_col = 0
        if cnt_row != m / 2 and cnt_row != (m + 1) / 2:
                return -1
        if cnt_col != m / 2 and cnt_col != (m + 1) / 2:
            return -1

        if cnt_row == m / 2:
            target_row = ((1 << m) - 1) ^ row[0]
        else:
            target_row = row[0]
            
        for index in range(0, m, 2):
            if row[index] != target_row:
                res_row += 1

        if cnt_col == m / 2:
            target_col = ((1 << m) - 1) ^ col[0]
        else:
            target_col = col[0]

        for index in range(0, m, 2):
            if col[index] != target_col:
                res_col += 1

        if m % 2 == 0:
            res_row = min(m / 2 - res_row, res_row)
            res_col = min(m / 2 - res_col, res_col)
        
        return res_col + res_row
```
