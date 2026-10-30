---
title: "1252. 奇数值单元格的数目"
aliases: ["yiduobo的每日leetcode 1252.奇数值单元格的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386157051"
zhihu_id: "386157051"
zhihu_title: "yiduobo的每日leetcode 1252.奇数值单元格的数目"
question_id: "1252"
question: "奇数值单元格的数目"
problem_url: "https://leetcode.cn/problems/cells-with-odd-values-in-a-matrix/"
created: "2021-07-02T21:31:00+08:00"
updated: "2021-07-02T21:31:00+08:00"
upvotes: 0
comments: 0
---

# 1252. 奇数值单元格的数目

> **[yiduobo的每日leetcode 1252.奇数值单元格的数目](https://zhuanlan.zhihu.com/p/386157051) · 知乎 · 2021-07-02 · 赞同 0**
> 力扣：[1252. 奇数值单元格的数目](https://leetcode.cn/problems/cells-with-odd-values-in-a-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1252.奇数值单元格的数目

[力扣](https://leetcode-cn.com/problems/cells-with-odd-values-in-a-matrix/)

首先，由于题目中每次都是对于一行或者一列进行操作，因此我们可以统计对每一行和每一列最终的操作次数，分别记为r_cnt和c_cnt。

我们先抛开列不看，只看行操作。对于第x行，其被操作过了r_cnt[x]次。若操作次数为奇数，那么最终行中的数就都是奇数，否则都是偶数。因此我们可以统计r_cnt[x]中奇数的数目，记为r，那么最终会有r \* n个奇数的单元格。

同样地，抛开行不看，只看列操作，设c为c_cnt[x]中奇数的数目，那么最终会有c \* m个奇数的单元格。

这么看来最终就有r \* n + c \* m个奇数的单元格，但是其中有部分单元格是同时被行列操作过的，这些单元格一共有r \* c个，同时由于这些单元格在行上被操作了r次，在列上被操作了c次，因此一共操作了r + c次，因此这些单元格最终为偶数，于是最终答案应该就是

r \* n + c \* m - 2 \* r \* c

最后附上python代码：

```python
class Solution(object):
    def oddCells(self, m, n, indices):
        """
        :type m: int
        :type n: int
        :type indices: List[List[int]]
        :rtype: int
        """

        r_cnt = [0] * m
        c_cnt = [0] * n
        for x, y in indices:
            r_cnt[x] += 1
            c_cnt[y] += 1
        
        r = c = 0
        for index in range(m):
            if r_cnt[index] % 2 == 1:
                r += 1
        
        for index in range(n):
            if c_cnt[index] % 2 == 1:
                c += 1
        
        return r * n + c * m - 2 * r * c
```
