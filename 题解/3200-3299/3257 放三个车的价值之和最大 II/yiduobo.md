---
title: "3256. 放三个车的价值之和最大I & 3257. 放三个车的价值之和最大II"
aliases: ["yiduobo的每日leetcode 3256.放三个车的价值之和最大I && 3257.放三个车的价值之和最大II", "3256. 放三个车的价值之和最大I", "3257. 放三个车的价值之和最大II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/enumeration", "leetcode/graph", "leetcode/shortest-path", "题单/常用数据结构", "题单/动态规划", "题单/图论算法", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721943275"
zhihu_id: "721943275"
zhihu_title: "yiduobo的每日leetcode 3256.放三个车的价值之和最大I && 3257.放三个车的价值之和最大II"
question_id: ["3256", "3257"]
question: ["放三个车的价值之和最大 I", "放三个车的价值之和最大 II"]
problem_url: ["https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-i/", "https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-ii/"]
difficulty: "Hard"
rating: 2553
created: "2024-09-25T04:58:22+08:00"
updated: "2024-09-25T04:58:22+08:00"
upvotes: 3
comments: 0
---

# 3256. 放三个车的价值之和最大I & 3257. 放三个车的价值之和最大II

> **[yiduobo的每日leetcode 3256.放三个车的价值之和最大I && 3257.放三个车的价值之和最大II](https://zhuanlan.zhihu.com/p/721943275) · 知乎 · 2024-09-25 · 赞同 3**
> 力扣：[3256. 放三个车的价值之和最大 I](https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-i/) · Hard · 灵茶山艾府：[O(mn) 前后缀分解（Python/Java/C++/Go）](../3256%20放三个车的价值之和最大%20I/灵茶山艾府.md)
> 力扣：[3257. 放三个车的价值之和最大 II](https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-ii/) · Hard · 灵茶山艾府：[O(mn) 前后缀分解，附费用流写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3256.放三个车的价值之和最大I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-i/description/)

3257.放三个车的价值之和最大II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-value-sum-by-placing-three-rooks-ii/description/)

题目给出一个大小为m \* n的棋盘board，其中board[i][j]表示这个单元格的价值。

现在要求在棋盘上放置三个车，且这个车不能相互攻击，即这三个车中的任意两个都不能在同一行或者同一列。问如何放置可以使得这三个车所在的单元格价值之和最大。

两题的题设相同，第二题的数据规模较大，m和n都满足在3到500之间。

500这个规模是比较微妙的，使用O(n^2)或者O(n^2 \* log(n))的算法感觉留下的余地比较多，但是使用O(n^3)的算法又不行，所以本题还是要往O(n^2)或者O(n^2 \* log(n))的复杂度来考虑。

在这个复杂度下，可以做的事情就是遍历整个棋盘，也就是说在这里是允许多次遍历棋盘的。

题目要求放置三个车，那么不妨先考虑比较简单的情况。

首先考虑只需要放置一个车的情况。

对于这种情况，由于允许遍历棋盘，那么只需要进行一趟遍历，找出其中价值最高的单元格放置就行了。

---

接下来是需要放置两个车的情况。

此时最直观的放置方法自然是先进行一趟遍历，找出价值最高的单元格放置，然后在去掉其所在行和列之后，再对剩余的棋盘进行一趟遍历，找出剩余棋盘中价值最高的单元格进行放置。在实现上，可以认为是先计算仅放置一个车的最大值，然后修改棋盘，再计算仅放置一个车的最大值，计算二者之和。

那么在这里需要判断的问题是，是否可能存在其他的放置方法更优。答案是肯定的。例如棋盘

| 4 | 1 |
| --- | --- |
| 5 | 4 |

其中最大的单元格是(1, 0)，对应的值是5，而在选择这个单元格之后只剩下了右上角的1，相比之下选择两个4显然是更优的。

那么此时就需要考虑，假设最大值所在的单位格为(x1, y1)，选择(x1, y1)后剩余棋盘上的最大值(x2, y2)，那么现在有一种方案就是选择x1这一行上的次大值(x1, y1_2)以及选择y1这一列上的次大值(x1_2, y1)，需要判断后面这二者之和是否大于前面的二者之和。

判断的方法很简单，只需对x1这一行以及y1这一列分别进行遍历，取x1行上除了y1列之外其余单元格的最大值，以及y1列上除了x1行之外其余单元格的最大值，计算二者之和，与取(x1, y1)、(x2, y2)的方法进行比较就行了。需要注意这里的计算与前面的遍历不是嵌套执行的，因此不会影响时间复杂度。

接下来的问题是是否可能存在一种情况，即未选取最大值(x1, y1)，且也没有同时选取x1行上的次大值(x1, y1_2)以及y1列上的次大值(x1_2, y1)。答案是否定的。

理由是：

1、如果选取的两个单元格同时占据了x1行和y1列，那么将二者的取值必然小于等于(x1, y1_2)以及(x1_2, y1)，也就是说此时不如选取(x1, y1_2)以及(x1_2, y1)。

2、如果选择的两个单元格仅占据了x1行，那么将占据x1行对应的单元格移动到(x1, y1)，得到的和明显更优。

3、如果选择的两个单元格仅占据了y1列，那么与情况2）相同，将占据y1的单元格移动到(x1, y1)是更优的。

4、如果选择的两个单元格既没有占据x1行，也没有占据y1列，此时将任意单元格移动到(x1, y1)都是更优的。

根据上面的结论，说明放置两个棋子的最优解必然是(x1, y1)、(x2, y2)或者(x1, y1_2)、(x1_2, y1)这两种情况之一。那么只需分别找出这两种情况对应的单元格然后计算对应的和进行比较即可。

---

最后是本题，需要放置三个车的情况。

受到上面的启发，在讨论三个车的放置时，可以明确的是要么会将一个车放置在最优的单元格(x1, y1)上，要么会有两个车分别占据x1这一行以及y1这一列，否则的话必然可以将某个车移动到(x1, y1)上得到更优的答案。

接下来先讨论将一个车放置在(x1, y1)上的情况。

这种情况的处理比较简单，将棋盘的x1行以及y1列去掉后，问题就变成了放置两个车的最优解，直接套用上面的求解方法就行了。

最后是有两个车分别占据x1这一行以及y1这一列的情况。

不妨设x1这一行上前4大的单元格分别为(x1, y1)，(x1, y1_2)，(x1, y1_3)，(x1, y1_4)，那么(x1, y1_4)以及更小的单元格是不应该被选择的，理由是当选择了(x1, y1_4)或者更小的单元格时，另外的两个车最多占据y1、y1_2、y1_3这三列中的两列，换言之必然还剩余一列没有被占据，此时如果将(x1, y1_4)移动到没有被占据的这一列，得到的答案必然更优。

换言之，对于有两个车分别占据了x1这一行以及y1这一列的情况，在x1这一行上的车只能位于(x1, y1_2)或者(x1, y1_3)，而在y1这一列上的车只能位于(x1_2, y1)或者(x1_3, y1)。

接下来就只需分别求解前两个车放置的组合对应的第三个车的位置就行了：

1、单元格(x1, y1_2)以及(x1_2, y1)：

对于这种情况，需要再遍历一次剩余的棋盘找出剩余棋盘上的最大值。需要注意的是，由于(x1, y1_2)和(x1_2, y1)可以屏蔽掉x1_2这一行以及y1_2这一列，因此(x2, y2)或者(x3, y3)可能被屏蔽掉，此时需要重新在剩余棋盘上找到最大值。

2、单元格(x1, y1_2)以及(x1_3, y1)：

此时第三个车必然占据了x1_2这一行，否则将(x1_3, y1)移动到(x1_2, y1)明显更优。因此第三个车就是x1_2这一行上除了(x1_2, y1)之外的最大值，遍历x1_2这一行，计算除了(x1_2, y1)以及(x1_2, y1_2)之外的最大值即可。

3、单元格(x1, y1_3)以及(x1_2, y1)：

与情况2对称，此时只需要遍历y1_2这一列，计算除了(x1, y1_2)以及(x1_2, y1_2)之外的最大值即可。

4、单元格(x1, y1_3)以及(x1_3, y1)：

此时唯一需要考虑的就是(x1_2, y1_2)，因为若第三个车放在其他位置，都无法同时屏蔽x1_2这一行以及y1_2这一列，这也就意味着可以将(x1, y1_3)移动到(x1, y1_2)，或者将(x1_3, y1)移动到(x1_2, y1)。

当然，在这里也可以选择偷懒的写法，直接假设第一个车放在(x1, y1_2)、(x1, y1_3)、(x1_2, y1)、(x1_3, y1)中的某个位置，然后计算剩余两个车放置的最优解。时间复杂度不变，但是会多几次遍历。

最后附上python代码：

```python
class Solution(object):
    def maximumValueSum(self, board):
        """
        :type board: List[List[int]]
        :rtype: int
        """

        m = len(board)
        n = len(board[0])

        def max_in_board(vis_x_list, vis_y_list):
            vis_x = set(vis_x_list)
            vis_y = set(vis_y_list)
            x, y = None, None
            for i in range(m):
                for j in range(n):
                    if i not in vis_x and j not in vis_y and (x is None or board[x][y] < board[i][j]):
                        x, y = i, j
            return x, y
        
        def max_in_col(y, vis_x_list):
            vis_x = set(vis_x_list)
            x = None
            for i in range(m):
                if i not in vis_x and (x is None or board[x][y] < board[i][y]):
                    x = i
            return x

        def max_in_row(x, vis_y_list):
            vis_y = set(vis_y_list)
            y = None
            for j in range(n):
                if j not in vis_y and (y is None or board[x][y] < board[x][j]):
                    y = j
            return y

        x1, y1 = max_in_board([], [])
        x2, y2 = max_in_board([x1], [y1])
        x3, y3 = max_in_board([x1, x2], [y1, y2])
        x2_2 = max_in_col(y2, [x1, x2])
        y2_2 = max_in_row(x2, [y1, y2])
        res = board[x1][y1] + board[x2][y2] + board[x3][y3]
        res = max(res, board[x1][y1] + board[x2][y2_2] + board[x2_2][y2])
        
        x1_2 = max_in_col(y1, [x1])
        y1_2 = max_in_row(x1, [y1])
        x1_3 = max_in_col(y1, [x1, x1_2])
        y1_3 = max_in_row(x1, [y1, y1_2])
        y_x12_ma = max_in_row(x1_2, [y1, y1_2])
        x_y12_ma = max_in_col(y1_2, [x1, x1_2])

        xx, yy = max_in_board([x1, x1_2], [y1, y1_2])
        res = max(res, board[x1][y1_2] + board[x1_2][y1] + board[xx][yy])
        res = max(res, board[x1][y1_2] + board[x1_3][y1] + board[x1_2][y_x12_ma])
        res = max(res, board[x1][y1_3] + board[x1_2][y1] + board[x_y12_ma][y1_2])
        res = max(res, board[x1][y1_3] + board[x1_3][y1] + board[x1_2][y1_2])

        return res
```
