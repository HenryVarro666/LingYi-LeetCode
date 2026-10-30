---
title: "2326. 螺旋矩阵IV"
aliases: ["yiduobo的每日leetcode 2326.螺旋矩阵IV"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/linked-list", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/557920262"
zhihu_id: "557920262"
zhihu_title: "yiduobo的每日leetcode 2326.螺旋矩阵IV"
question_id: "2326"
question: "螺旋矩阵 IV"
problem_url: "https://leetcode.cn/problems/spiral-matrix-iv/"
difficulty: "Medium"
created: "2022-08-26T00:26:08+08:00"
updated: "2022-08-26T00:26:08+08:00"
upvotes: 0
comments: 0
---

# 2326. 螺旋矩阵IV

> **[yiduobo的每日leetcode 2326.螺旋矩阵IV](https://zhuanlan.zhihu.com/p/557920262) · 知乎 · 2022-08-26 · 赞同 0**
> 力扣：[2326. 螺旋矩阵 IV](https://leetcode.cn/problems/spiral-matrix-iv/) · Medium · 灵茶山艾府：[模拟（代码同 59 题）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2326.螺旋矩阵IV

[力扣](https://leetcode.cn/problems/spiral-matrix-iv/)

题目给出一个链表和目标矩阵的规模，要求将链表中的数按顺序，以顺时针螺旋状填充到矩阵中。

本题螺旋状的前进顺序比较简单，因此可以选择直接模拟。

与常规的在地图上行走的问题一样，可以先定义方向矩阵dx和dy。注意到题目中是顺时针螺旋前进，且一开始是向右的，那么最终的前进方向就应该是 右 -> 下 -> 左 -> 上 -> 右 这样循环，因此在定义dx和dy时，一开始是向右，所有dx[0] \= 0, dy[0] \= 1；接下来向下，所以dx[1] \= 1, dy[1] \= 0；再之后是向左，因此dx[2] \= 0, dy[2] \= -1；最后是向上，因此dx[3] \= -1, dy[3] \= 0。

定义好dx和dy后，初始化一个空的目标矩阵，初始方向d \= 0，然后从单元格(0, 0)开始进行填充。若当前方向上的下一个单元格超出了矩阵边界，或者已经被填充过了，那么就将方向顺时针旋转90度，对应到代码上就是将当前d变为(d + 1) % 4。重复该过程直到下一个填充的单元格是合法的，此时进行填充，然后按上面同样的方式继续考察之后要填充的单元格，直到填充完毕。

最后附上python代码：

```python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def spiralMatrix(self, m, n, head):
        """
        :type m: int
        :type n: int
        :type head: Optional[ListNode]
        :rtype: List[List[int]]
        """

        res = [[-1] * n for _ in range(m)]
        now = head
        nowx, nowy = 0, 0
        nowd = 0

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        while now:
            res[nowx][nowy] = now.val
            now = now.next
            if not now:
                break
            nowx += dx[nowd]
            nowy += dy[nowd]
            while nowx < 0 or nowx == m or nowy < 0 or nowy == n or res[nowx][nowy] != -1:
                nowx -= dx[nowd]
                nowy -= dy[nowd]
                nowd = (nowd + 1) % 4
                nowx += dx[nowd]
                nowy += dy[nowd]
        
        return res
```
