---
title: "773. 滑动谜题"
aliases: ["yiduobo的每日leetcode 773.滑动谜题"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339775646"
zhihu_id: "339775646"
zhihu_title: "yiduobo的每日leetcode 773.滑动谜题"
question_id: "773"
question: "滑动谜题"
problem_url: "https://leetcode.cn/problems/sliding-puzzle/"
created: "2020-12-26T20:21:23+08:00"
updated: "2020-12-26T20:21:23+08:00"
upvotes: 0
comments: 0
---

# 773. 滑动谜题

> **[yiduobo的每日leetcode 773.滑动谜题](https://zhuanlan.zhihu.com/p/339775646) · 知乎 · 2020-12-26 · 赞同 0**
> 力扣：[773. 滑动谜题](https://leetcode.cn/problems/sliding-puzzle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

773.滑动谜题

[力扣](https://leetcode-cn.com/problems/sliding-puzzle/)

有一道经典的搜索题，名叫8数码问题，是这道题的升级版本，即在3\*3的空间内，有八块板子和一个空格，要求经过一些移动使得板子能移动到指定的位置。

对于这个问题，有两种经典的做法，分别是启发式搜索以及bfs，我这里使用的是bfs这一种。首先，对于题目中的板子，如果从上往下从左往右排下来，那么就可以形成一个0到5的全排列。对于这个排列，可以使用康拓展开来进行编码。

具体的编码原理为，对于k个不同数字组成的全排列，一共有k！种，那么对于本题0-5这些数字，如果第一个数字为0，那么后续1到5就有5！\=120种可能性，若第一个数字为1，那么0以及2到5同样是120中可能性，于是我们按照这个顺序进行编码，可以得到以剩余所有数字中第k小数字开头的所有排列编码位于120 \* (k - 1) 到120 \* k - 1之间。确定了首位之后，我们可以从剩下的数字中继续计算后续的编码区间，此时对于剩余数字中第k小数字开头序列的编码则是4! \* (k - 1)到4! \* k - 1之间，以此往后类推。

以最后一个样例中的4、1、2、5、0、3为例：

1、第一位为4，是剩余数字中第5小的，那么编码区间位于480到599之间。

2、第二位为1，是剩余数字中第2小的，那么编码区间位于24到47之间，与第一步的结果累加，可以得到以12开头的排列编码区间位于480+ 24到480+ 47之间。

3、第三位为2，是剩余数字中第2小的，那么编码区间位于6到11之间，综合前两步的结果就是以123开头的排列编码区间位于480+ 24 + 6到480+ 24 + 11之间。

4、第四位为5，是剩下数字中第3小的，那么编码区间位于4到5之间，综合前三部的结果就是以1234开头的排列编码区间位于480+ 24 + 6 + 4到480+ 24 + 6 + 5之间。

5、第五位为0，是剩下数字中最小的，那么编码为0，那么最终的编码就是480+24+6+4+0 \= 514。

反过来，从编码出发，我们就可以每次除以当前剩余数减一的阶乘，来确定当前排列的最高位是多少，例如上面的514，我们还剩下6个数，那么

1）514/ 120 \= 4，余数为34，那么排列的首位是剩余数字中第5小的，即为4，此时还剩下0、1、2、3、5共5个数字

2）34/ 24 \= 1，余数为10，那么排列的第二位是剩余数字中第2小的，即为1，此时还剩下0、2、3、5共4个数字

3）10 / 6 \= 1，余数为4，那么排列的第三位是剩余数字中第2小的，即为2，此时还剩下0、3、5共3个数字

4）4 / 2 \= 2，余数为0，那么排列的第四位是剩余数字中第3小的，即为5，此时还剩下0、3共2个数字

5）0 / 1 \= 0，那么排列的第五位是剩余数字中第1小的，即为0

6）最后剩下的3位最后一位，此时就得到了原始的排列4、1、2、5、0、3

有了上面的编码方式，那么我们就可以对滑动过程中，这总共6！\= 720种可能情况进行0到719的编码，从而达到在搜索过程中去重的目的。

具体的搜索过程倒是平平无奇，就是枚举当前0的四个方向，若没有出界，那么就尝试交换。若交换后的状态没有出现过，那么将其加入到bfs队列中。若某次交换后达成了最终的目标状态，那么就返回交换次数。若bfs完成，那么说明没有达成目标状态，返回-1。

最后附上python代码：

```python
class Solution(object):
    def slidingPuzzle(self, board):
        """
        :type board: List[List[int]]
        :rtype: int
        """

        factor = [1, 1, 2, 6, 24, 120, 720]
        now = self.cantor(board, factor)
        target = self.cantor([[1, 2, 3], [4, 5, 0]], factor)
        if now == target:
            return 0

        used = [False] * factor[-1]
        q = [now]
        used[now] = True
        l, r = 0, 1
        step = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        while l < r:
            step += 1
            for now in q[l: r]:
                now_board = self.cantor_reverse(now, factor)
                for nowx in range(2):
                    for nowy in range(3):
                        if now_board[nowx][nowy] == 0:
                            break
                    if now_board[nowx][nowy] == 0:
                        break
            
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < 2 and y >= 0 and y < 3:
                        now_board[nowx][nowy], now_board[x][y] = now_board[x][y], now_board[nowx][nowy]
                        tmp = self.cantor(now_board, factor)
                        if not used[tmp]:
                            used[tmp] = True
                            q.append(tmp)
                        now_board[nowx][nowy], now_board[x][y] = now_board[x][y], now_board[nowx][nowy]
            
            if used[target]:
                return step

            l, r = r, len(q)
        
        return -1

    def cantor(self, board, factor):
        tmp = board[0] + board[1]
        res = 0
        for i in range(6):
            cnt = 0
            for j in range(i + 1, 6):
                if tmp[i] > tmp[j]:
                    cnt += 1
            res += cnt * factor[6 - i - 1]

        return res

    def cantor_reverse(self, num, factor):
        res = []
        used = [False] * 6
        for i in range(6):
            cnt = num / factor[6 - i - 1]
            num -= cnt * factor[6 - i - 1]
            for j in range(6):
                if not used[j]:
                    if cnt == 0:
                        res.append(j)
                        used[j] = True
                        break
                    cnt -= 1
        
        return [res[:3], res[3:6]]
```
