---
title: "533. 孤独像素II"
aliases: ["yiduobo的每日leetcode 533.孤独像素II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600681273"
zhihu_id: "600681273"
zhihu_title: "yiduobo的每日leetcode 533.孤独像素II"
question_id: "533"
question: "孤独像素II"
problem_url: "https://leetcode.cn/problems/lonely-pixel-ii/"
created: "2023-01-24T01:40:51+08:00"
updated: "2023-01-24T01:40:51+08:00"
upvotes: 0
comments: 0
---

# 533. 孤独像素II

> **[yiduobo的每日leetcode 533.孤独像素II](https://zhuanlan.zhihu.com/p/600681273) · 知乎 · 2023-01-24 · 赞同 0**
> 力扣：[533. 孤独像素II](https://leetcode.cn/problems/lonely-pixel-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

533.孤独像素II

[力扣](https://leetcode.cn/problems/lonely-pixel-ii/)

本题与之前的孤独像素I类似，但是关于孤独像素的定义多出了一个条件，就是其所在列中，所有黑色像素所在的行必须完全一致，那么在这里就需要有方法可以高效地判断两行是否相同。

注意到本题数据规模不大，那么可以先两两枚举所有行的组合，然后一趟遍历检测枚举的两行是否相同。在这里使用哈希来判断是更好的做法，不过前提是需要设计出优秀的哈希函数。我在这里采用的是暴力法，这一步预处理的时间复杂度为O(n^3)。

接下来，同样是遍历整个图片，不过统计的是图片中每一行的黑色像素数目，以及每一列中有哪些行是黑色像素。这里记录哪些行是黑色像素的理由是方便后续判断行是否相同。接下来，枚举每一列，若当前列中黑色像素的数目等于target，那么就从这一列中是黑色像素的行中选出一个基准行first，然后再判断first这一行中黑色像素的数目是否等于target，同时利用预处理出来的数组判断当前列中其他黑色像素的行是否与first相同，若都相同，那么说明当前列中所有的黑色像素都是孤独像素，此时就应该用当前列中黑色像素的数目，也就是target来更新答案。

最后附上python代码：

```python
class Solution(object):
    def findBlackPixel(self, picture, target):
        """
        :type picture: List[List[str]]
        :type target: int
        :rtype: int
        """

        m = len(picture)
        n = len(picture[0])

        same = [[True] * m for _ in range(m)]

        for i in range(m - 1):
            for j in range(i + 1, m):
                for k in range(n):
                    if picture[i][k] != picture[j][k]:
                        same[i][j] = same[j][i] = False
                        break

        row = [0] * m
        col = [[] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                if picture[i][j] == 'B':
                    row[i] += 1
                    col[j].append(i)
        
        res = 0
        for j in range(n):
            if len(col[j]) == target:
                first = col[j][0]
                if row[first] == target:
                    flag = True
                    for other in col[j][1:]:
                        if not same[first][other]:
                            flag = False
                            break
                    
                    if flag:
                        res += target
        
        return res
```
