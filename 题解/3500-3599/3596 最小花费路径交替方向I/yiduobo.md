---
title: "3596. 最小花费路径交替方向I"
aliases: ["yiduobo的每日leetcode 3596.最小花费路径交替方向I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1940602284661806369"
zhihu_id: "1940602284661806369"
zhihu_title: "yiduobo的每日leetcode 3596.最小花费路径交替方向I"
question_id: "3596"
question: "最小花费路径交替方向I"
problem_url: "https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-i/"
created: "2025-08-18T02:53:20+08:00"
updated: "2025-08-18T02:53:20+08:00"
upvotes: 0
comments: 0
---

# 3596. 最小花费路径交替方向I

> **[yiduobo的每日leetcode 3596.最小花费路径交替方向I](https://zhuanlan.zhihu.com/p/1940602284661806369) · 知乎 · 2025-08-18 · 赞同 0**
> 力扣：[3596. 最小花费路径交替方向I](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3596.最小花费路径交替方向I

[3596. 最小花费路径交替方向 I - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-i/description/)

给出两个整数m和n，表示一个网格的行数和列数。定义进入单元格(i, j)的花费为(i + 1) \* (j + 1)。路径的第一步始终是进入单元格(0, 0)并支付入场花费，在接下来的每一步中，如果是第奇数次移动，必须向右侧或者下方移动到相邻的单元格，反之如果是第偶数次移动，则必须向左侧或者上方移动到相邻的单元格。

问到达(m - 1, n - 1)的最小总花费。若无法到达，则返回-1。

第一次见到要求反正走的题目。可以发现，在奇数次移动后，与终点的曼哈顿距离将减少1，反之在偶数次移动后，与终点的曼哈顿距离将增加1。换言之，除了一开始就在终点的情况之外，一旦无法一步到位，那么就永远走不到终点了。于是只需判断n和m是否属于(1, 1)，(1, 2)，(2, 1)这三种情况之一，如果属于，则返回1或者3，反之直接返回-1即可。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """
        
        if m == 1 and n == 1:
            return 1
        if m == 2 and n == 1:
            return 3
        if m == 1 and n == 2:
            return 3
        
        return -1
```
