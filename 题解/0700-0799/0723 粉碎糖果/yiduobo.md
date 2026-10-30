---
title: "723. 粉碎糖果"
aliases: ["yiduobo的每日leetcode 723.粉碎糖果"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604999700"
zhihu_id: "604999700"
zhihu_title: "yiduobo的每日leetcode 723.粉碎糖果"
question_id: "723"
question: "粉碎糖果"
problem_url: "https://leetcode.cn/problems/candy-crush/"
created: "2023-02-10T01:07:34+08:00"
updated: "2023-02-10T01:07:34+08:00"
upvotes: 0
comments: 0
---

# 723. 粉碎糖果

> **[yiduobo的每日leetcode 723.粉碎糖果](https://zhuanlan.zhihu.com/p/604999700) · 知乎 · 2023-02-10 · 赞同 0**
> 力扣：[723. 粉碎糖果](https://leetcode.cn/problems/candy-crush/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

723.粉碎糖果

[力扣](https://leetcode.cn/problems/candy-crush/)

没有什么特别好的思路，不过好在本题的数据范围很小，可以直接暴力处理。

话又说回来，消消乐这类的游戏也不太可能到50\*50的板子吧。。

具体实现上，使用一个集合remove_pos记录每一轮需要消除的单元格，接下来每一轮：

1、清空remove_pos

2、对board进行一趟遍历。对于当前遍历到的位置board[i][j]，若其不为0：

2-1）board[i][j]与board[i][j + 1]和board[i][j + 2]相等，那么就将这三个单元格加入到remove_pos中

2-2）board[i][j]与board[i + 1][j]和board[i + 2][j]相等，那么也将这三个单元格加入到remove_pos中

3、遍历remove_pos，将其中所有的单元格清零

4、从左向右逐列遍历board，对于当前列，从下向上遍历，将非0值向下填充

重复上述过程直到某一轮的remove_pos为空为止，最终的时间复杂度为O((mn)^2)，不算太好但也勉强够用了。

最后附上python代码：

```python
class Solution(object):
    def candyCrush(self, board):
        """
        :type board: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(board)
        n = len(board[0])

        while True:
            remove_pos = set()

            for i in range(m):
                for j in range(n):
                    if j + 2 < n and board[i][j] > 0 and board[i][j] == board[i][j + 1] == board[i][j + 2]:
                        remove_pos.add((i, j))
                        remove_pos.add((i, j + 1))
                        remove_pos.add((i, j + 2))

                    if i + 2 < m and board[i][j] > 0 and board[i][j] == board[i + 1][j] == board[i + 2][j]:
                        remove_pos.add((i, j))
                        remove_pos.add((i + 1, j))
                        remove_pos.add((i + 2, j))

            if len(remove_pos) == 0:
                break

            for x, y in remove_pos:
                board[x][y] = 0

            for j in range(n):
                p = m - 1
                for i in range(m - 1, -1, -1):
                    if board[i][j] > 0:
                        board[p][j] = board[i][j]
                        if p > i:
                            board[i][j] = 0
                        p -= 1
                
                for i in range(p, -1, -1):
                    board[i][j] = 0

        return board
```
