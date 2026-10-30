---
title: "2500. 删除每行中的最大值"
aliases: ["yiduobo的每日leetcode 2500.删除每行中的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/633785637"
zhihu_id: "633785637"
zhihu_title: "yiduobo的每日leetcode 2500.删除每行中的最大值"
question_id: "2500"
question: "删除每行中的最大值"
problem_url: "https://leetcode.cn/problems/delete-greatest-value-in-each-row/"
difficulty: "Easy"
created: "2023-06-01T02:19:12+08:00"
updated: "2023-06-01T02:19:12+08:00"
upvotes: 0
comments: 0
---

# 2500. 删除每行中的最大值

> **[yiduobo的每日leetcode 2500.删除每行中的最大值](https://zhuanlan.zhihu.com/p/633785637) · 知乎 · 2023-06-01 · 赞同 0**
> 力扣：[2500. 删除每行中的最大值](https://leetcode.cn/problems/delete-greatest-value-in-each-row/) · Easy · 灵茶山艾府：[无需模拟，排序即可（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2500.删除每行中的最大值

[力扣](https://leetcode.cn/problems/delete-greatest-value-in-each-row/)

题目的数据规模很小，因此只需遍历每行，先进行排序然后一趟遍历，使用当前位置上的数值更新其所在列的最大值，最后将每一列的最大值求和即为最终的答案。

最后附上python代码：

```python
class Solution(object):
    def deleteGreatestValue(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        n = len(grid[0])
        max_list = [0] * n
        for line in grid:
            for index, v in enumerate(sorted(line)):
                max_list[index] = max(max_list[index], v)
        
        return sum(max_list)
```
