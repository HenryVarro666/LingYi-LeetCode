---
title: "1975. 最大方阵和"
aliases: ["yiduobo的每日leetcode 1975.最大方阵和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/496285324"
zhihu_id: "496285324"
zhihu_title: "yiduobo的每日leetcode 1975.最大方阵和"
question_id: "1975"
question: "最大方阵和"
problem_url: "https://leetcode.cn/problems/maximum-matrix-sum/"
difficulty: "Medium"
rating: 1648
created: "2022-04-11T00:09:04+08:00"
updated: "2022-04-11T00:09:04+08:00"
upvotes: 0
comments: 0
---

# 1975. 最大方阵和

> **[yiduobo的每日leetcode 1975.最大方阵和](https://zhuanlan.zhihu.com/p/496285324) · 知乎 · 2022-04-11 · 赞同 0**
> 力扣：[1975. 最大方阵和](https://leetcode.cn/problems/maximum-matrix-sum/) · Medium · 灵茶山艾府：[脑筋急转弯 + 分类讨论（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1975.最大方阵和

[力扣](https://leetcode-cn.com/problems/maximum-matrix-sum/)

题目可以操作相邻的两个方格，且可以操作无数次，那么就可以通过若干次操作将某个格子上的符号转移到其他任意格子上。具体证明也很简单，只需要随意画出一条从起始位置到结束位置的路径，然后延路径两两翻转相邻的格子，就能让起始位置的负号转移到结束位置了。

题目要求方阵和最大，那么就要使得负号尽可能少，因此一个自然的想法就是将所有负号都转移到同一个格子上，利用负负得正消去负号。

若原始矩阵中负号的个数为偶数，那么最终可以消去全部负号，答案就是矩阵中的数值之和；若负号的个数为奇数，那么最终会遗留下一个负号。很明显，应该将其分配给数值绝对值最小的格子。记这个格子数值的绝对值为mi，答案就是矩阵中的数值之和减去两倍的mi。

最后附上python代码：

```python
class Solution(object):
    def maxMatrixSum(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """

        cnt = 0
        mi = 100001
        s = 0
        for line in matrix:
            for num in line:
                if abs(num) < mi:
                    mi = abs(num)
                if num < 0:
                    cnt += 1
                    s -= num
                else:
                    s += num

        if cnt % 2 == 1:
            s -= mi + mi
        
        return s
```
