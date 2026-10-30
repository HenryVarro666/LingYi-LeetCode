---
title: "1706. 球会落何处"
aliases: ["yiduobo的每日leetcode 1706.球会落何处"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/449198642"
zhihu_id: "449198642"
zhihu_title: "yiduobo的每日leetcode 1706.球会落何处"
question_id: "1706"
question: "球会落何处"
problem_url: "https://leetcode.cn/problems/where-will-the-ball-fall/"
difficulty: "Medium"
created: "2021-12-24T00:23:51+08:00"
updated: "2021-12-24T00:23:51+08:00"
upvotes: 1
comments: 0
---

# 1706. 球会落何处

> **[yiduobo的每日leetcode 1706.球会落何处](https://zhuanlan.zhihu.com/p/449198642) · 知乎 · 2021-12-24 · 赞同 1**
> 力扣：[1706. 球会落何处](https://leetcode.cn/problems/where-will-the-ball-fall/) · Medium · 灵茶山艾府：[模拟每列球的移动（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1706.球会落何处

[力扣](https://leetcode-cn.com/problems/where-will-the-ball-fall/)

题目看上去很复杂的样子，但是实际上仔细分析可以发现，对于行中的某个位置p，只有两种可能可以让上一行到达p这个位置的球有机会落到下一行而不是被卡住。

若p这个格子是右挡板，那么此时p不能是最右侧的格子，同时p的右边那个格子必须也是右挡板。此时小球就会从p这个位置下落到下一行的p + 1这个位置。

若p这个格子是左挡板，那么此时p不能是最左侧的格子，同时p的左边那个格子必须也是左挡板。此时小球就会从p这个位置下落到下一行的p - 1这个位置。

其他情况下，小球都会被卡住。

有了上面的结论，就可以从最上面开始逐行计算每个球落到了当前行的哪个位置。当然，对于已经被卡住了的球就无须再进行计算了。

最后附上python代码：

```python
class Solution(object):
    def findBall(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[int]
        """

        n = len(grid[0])
        res = range(n)
        for line in grid:
            for index in range(n):
                if res[index] != -1:
                    p = res[index]
                    if line[p] == 1:
                        if p != n - 1 and line[p + 1] == 1:
                            res[index] = p + 1
                        else:
                            res[index] = - 1
                    else:
                        if p != 0 and line[p - 1] == -1:
                            res[index] = p - 1
                        else:
                            res[index] = -1
        
        return res
```
