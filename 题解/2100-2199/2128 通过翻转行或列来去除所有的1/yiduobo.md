---
title: "2128. 通过翻转行或列来去除所有的1"
aliases: ["yiduobo的每日leetcode 2128.通过翻转行或列来去除所有的1"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626502403"
zhihu_id: "626502403"
zhihu_title: "yiduobo的每日leetcode 2128.通过翻转行或列来去除所有的1"
question_id: "2128"
question: "通过翻转行或列来去除所有的1"
problem_url: "https://leetcode.cn/problems/remove-all-ones-with-row-and-column-flips/"
created: "2023-05-03T21:07:40+08:00"
updated: "2023-05-03T21:07:40+08:00"
upvotes: 0
comments: 0
---

# 2128. 通过翻转行或列来去除所有的1

> **[yiduobo的每日leetcode 2128.通过翻转行或列来去除所有的1](https://zhuanlan.zhihu.com/p/626502403) · 知乎 · 2023-05-03 · 赞同 0**
> 力扣：[2128. 通过翻转行或列来去除所有的1](https://leetcode.cn/problems/remove-all-ones-with-row-and-column-flips/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2128.通过翻转行或列来去除所有的1

[力扣](https://leetcode.cn/problems/remove-all-ones-with-row-and-column-flips/)

由于题目每次只能翻转一整行或者一整列，那么同一行内的0和1就只能通过翻转对应的列来进行调整，于是翻转的目标就变成了选择矩阵中的若干列进行翻转，使得矩阵中每一行都满足整行全是1或者整行全是0。另一方面，当为了某一行翻转了某些列之后，就不能再翻转其他的列，因为这样会再次打乱这一行，这也就意味着每行需要翻转的列必须都一样，也就是各行要么完全相同，要么完全不同。

根据上面的结论，只需从第二行开始向后遍历，检测每一行是否与第一行完全相同或者完全不同。若每行都满足，那么答案就是true，否则就是false。

最后附上python代码：

```python
class Solution(object):
    def removeOnes(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])
        for i in range(1, m):
            flag1 = flag2 = True
            for j in range(n):
                if grid[i][j] == grid[0][j]:
                    flag1 = False
                if grid[i][j] != grid[0][j]:
                    flag2 = False
            
            if not flag1 and not flag2:
                return False
        
        return True
```
