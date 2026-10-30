---
title: "3537. 填充特殊网格"
aliases: ["yiduobo的每日leetcode 3537.填充特殊网格"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/五-其他递归/分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907208974815695956"
zhihu_id: "1907208974815695956"
zhihu_title: "yiduobo的每日leetcode 3537.填充特殊网格"
question_id: "3537"
question: "填充特殊网格"
problem_url: "https://leetcode.cn/problems/fill-a-special-grid/"
difficulty: "Medium"
rating: 1542
created: "2025-05-17T23:24:18+08:00"
updated: "2025-05-17T23:24:18+08:00"
upvotes: 0
comments: 0
---

# 3537. 填充特殊网格

> **[yiduobo的每日leetcode 3537.填充特殊网格](https://zhuanlan.zhihu.com/p/1907208974815695956) · 知乎 · 2025-05-17 · 赞同 0**
> 力扣：[3537. 填充特殊网格](https://leetcode.cn/problems/fill-a-special-grid/) · Medium · 灵茶山艾府：[递归之美（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3537.填充特殊网格

[3537. 填充特殊网格 - 力扣（LeetCode）](https://leetcode.cn/problems/fill-a-special-grid/description/)

题目给出一个非负整数n，表示一个(2^n) \* (2^n)的网格。现在要求使用0到2^(2n) - 1之间的整数填充这个网格，使其成为一个特殊网格。一个网格是特殊网格，其要么是一个1 \* 1的网格，要么在其划分为4个象限后，满足：

1、右上角象限中的所有元素都小于右下角象限中的所有元素

2、右下角象限中的所有元素都小于左下角象限中的所有元素

3、左下角象限中的所有元素都小于左上角象限中的所有元素

4、每个象限也都是一个特殊网格

对于题目对于特殊网格的描述中，最后一点，每个象限也都是特殊网格，预示着本题使用递归求解是很合适的。基于前三条的限制，那么对于一个(2^n) \* (2^n)的网格，只需将其中填充的元素0到2^(2n) - 1这些元素按从小到大的顺序划分为4份，依次递归填充到右上、右下、左下、左上这四个象限中即可。停止的条件为n为0，此时网格中只有一个元素。

除了递归外，本题反过来写递推也是可行的。

以样例3为例，首先在答案矩阵的右上角填充0，接下来对于当前已有的1 \* 1的网格，将其加1、加2、加3的结果按照顺时针的顺序填充满答案矩阵右上角2 \* 2的网格，即

|  |  | 0 + 3 | 0 |
| --- | --- | --- | --- |
|  |  | 0 + 2 | 0 + 1 |
|  |  |  |  |
|  |  |  |  |

接下来，对于当前已有的2 \* 2的网格，将其中所有元素加4、加8、加12的结果按照顺时针的顺序填充满答案矩阵右上角4 \* 4的网格，即

| 3 + 12 | 0 + 12 | 3 | 0 |
| --- | --- | --- | --- |
| 2 + 12 | 1 + 12 | 2 | 1 |
| 3 + 8 | 0 + 8 | 3 + 4 | 0 + 4 |
| 2 + 8 | 1 + 8 | 2 + 4 | 1 + 4 |

更一般的，对于当前已经填充的(2^k) \* (2^k)的网格，其中一共有2^(2k)个元素，因此只需将这个网格中所有的元素加上2^(2k)、2 \* 2^(2k)、3 \* 2^(2k)的结果按顺时针的顺序填充满答案矩阵右上角(2^(k + 1)) \* (2^(k + 1))的网格，直到填充完整个(2^n) \* (2^n)的网格为止。

在具体实现上，可以通过网格的边长来确定接下来待填充网格的右上角坐标，然后枚举已填充网格中的元素，加上差值后再填充到对应的位置上。

最后附上python代码：

```python
class Solution(object):
    def specialGrid(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """
        
        m = 1 << n
        res = [[None] * m for _ in range(m)]
        res[0][m - 1] = 0

        def fill(rx, ry, length, diff):
            for i in range(length):
                for j in range(length):
                    res[rx + i][ry - j] = res[i][m - 1 - j] + diff

        part_length = 1
        diff = 1
        for index in range(n):
            fill(part_length, m - 1, part_length, diff)
            fill(part_length, m - 1 - part_length, part_length, diff * 2)
            fill(0, m - 1 - part_length, part_length, diff * 3)

            part_length <<= 1
            diff <<= 2
        
        return res
```
