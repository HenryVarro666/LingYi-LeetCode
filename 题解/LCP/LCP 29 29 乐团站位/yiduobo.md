---
title: "LCP 29. 乐团站位"
aliases: ["yiduobo的每日leetcode LCP29.乐团站位"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574009577"
zhihu_id: "574009577"
zhihu_title: "yiduobo的每日leetcode LCP29.乐团站位"
question_id: "LCP 29"
question: "乐团站位"
created: "2022-10-16T00:56:34+08:00"
updated: "2022-10-16T00:56:34+08:00"
upvotes: 0
comments: 0
---

# LCP 29. 乐团站位

> **[yiduobo的每日leetcode LCP29.乐团站位](https://zhuanlan.zhihu.com/p/574009577) · 知乎 · 2022-10-16 · 赞同 0**
> 力扣：LCP 29. 乐团站位

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP29.乐团站位

[力扣](https://leetcode.cn/problems/SNJvJP/)

经典的螺旋矩阵问题，在这里要求的是实际上是(xPos, yPos)这个单元格在螺旋矩阵中是第几个被访问到的。由于本题的数据规模很大，因此不能直接模拟，需要找找规律。

题目给出的是一个规整的正方形，那么就可以尝试从外向内一层一层来拨开，每一层都是按照题目要求的顺时针方向在行进。对于第k层，其四个角上的坐标分别为(k, k), (k, n - 1 - k), (n - 1 - k, n - 1 - k), (n - 1 - k, k)，那么总共的行进长度就是4 \* (n - 2k - 1)。

对于题目要找的位置(xPos, yPos)，可以通过其到正方形四条边的距离来计算出其位于那一层，即

level \= min(xPos, yPos, n - 1 - xPos, n - 1 - yPos)

接下来，第0层的路径长度为4 \* (n - 1)，第1层的路径长度为4 \* (n - 3)，依次类推，一直累加到第level - 1层的4 \* (n - 2 \* (level - 1) - 1) \= 4 \* (n - 2 \* level + 1)

那么在到达第level层之前，总的路径长度就是

tot \= 4 \* ((n - 1) + (n - 3) + ... + (n - 2 \* level + 1)) \= 4 \* level \* (n - level）

接下来还需要计算从(xPos, yPos)处在level层的第几个位置上。

首先可以通过判断xPos和yPos与level以及n - 1 - level的关系确定(xPos, yPos)位于level层的哪一条边上。

1、若xPos等于level，说明(xPos, yPos)位于level层的上边。由于level层上边的起点为(level, level)，那么当前的(xPos, yPos)就是level层的第yPos - level + 1个数，将其加入到tot中

2、若yPos等于n - 1 - level，说明(xPos, yPos)位于level层的右边。右边的起点为(level, n - 1 - level)，那么(xPos, yPos)就是右边的第xPos - level + 1个数。另外，还需要将上边的数也计算进来，因此需要将(n - level \* 2 - 1) + xPos - level + 1累加到tot中

3、若xPos等于n - 1 - level，说明(xPos, yPos)位于level层的下边。下边的起点为(n - 1 - level, n - 1 - level)，那么(xPos, yPos)就是下边的第n - 1 - level - yPos + 1个数。同样的，在这里还需要将上边和右边的数也计算进来，因此需要将(n - level \* 2 - 1) \* 2 + n - 1 - level - yPos + 1累加到tot中

4、最后一种可能，就是(xPos, yPos)位于level层的左边。左边的起点为(n - 1 - level, level)，那么(xPos, yPos)就是左边的第n - 1 - level - xPos + 1个数，再加上另外三条边上的数，此时就应该将(n - level \* 2 - 1) \* 3 + n - 1 - level - xPos + 1累加到tot中

到了这里，就得到了(xPos, yPos)是螺旋矩阵中的第几个数了，此时只需要模9就能得到最终答案。需要注意，当tot是9的倍数时，答案应该是9而不是0。

最后附上python代码：

```python
class Solution(object):
    def orchestraLayout(self, num, xPos, yPos):
        """
        :type num: int
        :type xPos: int
        :type yPos: int
        :rtype: int
        """

        level = min(xPos, num - 1 - xPos, yPos, num - 1 - yPos)
        tot = 4 * (num - level) * level % 9
        
        if xPos == level:
            tot += yPos - level + 1
        elif yPos == num - 1 - level:
            tot += (num - level * 2 - 1) + xPos - level + 1
        elif xPos == num - 1 - level:
            tot += 2 * (num - level * 2 - 1) + num - 1 - level - yPos + 1
        else:
            tot += 3 * (num - level * 2 - 1) + num - 1 - level - xPos + 1
        return (tot - 1) % 9 + 1
```
