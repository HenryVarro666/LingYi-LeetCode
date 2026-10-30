---
title: "1428. 至少有一个1的最左端列"
aliases: ["yiduobo的每日leetcode 1428.至少有一个1的最左端列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/616228680"
zhihu_id: "616228680"
zhihu_title: "yiduobo的每日leetcode 1428.至少有一个1的最左端列"
question_id: "1428"
question: "至少有一个1的最左端列"
problem_url: "https://leetcode.cn/problems/leftmost-column-with-at-least-a-one/"
created: "2023-03-22T23:15:29+08:00"
updated: "2023-03-22T23:15:29+08:00"
upvotes: 0
comments: 0
---

# 1428. 至少有一个1的最左端列

> **[yiduobo的每日leetcode 1428.至少有一个1的最左端列](https://zhuanlan.zhihu.com/p/616228680) · 知乎 · 2023-03-22 · 赞同 0**
> 力扣：[1428. 至少有一个1的最左端列](https://leetcode.cn/problems/leftmost-column-with-at-least-a-one/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1428.至少有一个1的最左端列

[力扣](https://leetcode.cn/problems/leftmost-column-with-at-least-a-one/)

按照题目的描述，行与行之间并没有任何关联，因此在这里需要从上到下枚举每一行，然后找出当前行最左侧1所在的列，而其中最左侧的列即为最终答案。

对于单一的一行，题目保证了1全部集中在右侧，因此在这里可以使用二分法来找出最左侧的1。对于每一轮处理的mid，通过get确认当前行的mid这一列是否为1，若为1，说明最左侧的1在left到mid，此时应该更新right为mid，否则说明最左侧的1在mid + 1到right之间，此时应该更新left为mid + 1。

最后附上python代码：

```python
# """
# This is BinaryMatrix's API interface.
# You should not implement it, or speculate about its implementation
# """
#class BinaryMatrix(object):
#    def get(self, row, col):
#        """
#        :type row : int, col : int
#        :rtype int
#        """
#
#    def dimensions:
#        """
#        :rtype list[]
#        """

class Solution(object):
    def leftMostColumnWithOne(self, binaryMatrix):
        """
        :type binaryMatrix: BinaryMatrix
        :rtype: int
        """

        rows, cols = binaryMatrix.dimensions()

        res = cols
        for r in range(rows):
            if binaryMatrix.get(r, res - 1) == 1:
                left = 0
                right = res - 1
                while left < right:
                    mid = (left + right) / 2
                    if binaryMatrix.get(r, mid) == 1:
                        right = mid
                    else:
                        left = mid + 1
                
                res = right
                if res == 0:
                    return 0
        
        if res == cols:
            return -1
        
        return res
```
