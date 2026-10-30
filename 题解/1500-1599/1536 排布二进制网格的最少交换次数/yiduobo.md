---
title: "1536. 排布二进制网格的最少交换次数"
aliases: ["yiduobo的每日leetcode 1536.排布二进制网格的最少交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/423821727"
zhihu_id: "423821727"
zhihu_title: "yiduobo的每日leetcode 1536.排布二进制网格的最少交换次数"
question_id: "1536"
question: "排布二进制网格的最少交换次数"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-arrange-a-binary-grid/"
difficulty: "Medium"
rating: 1881
created: "2021-10-20T23:52:57+08:00"
updated: "2021-10-20T23:52:57+08:00"
upvotes: 0
comments: 0
---

# 1536. 排布二进制网格的最少交换次数

> **[yiduobo的每日leetcode 1536.排布二进制网格的最少交换次数](https://zhuanlan.zhihu.com/p/423821727) · 知乎 · 2021-10-20 · 赞同 0**
> 力扣：[1536. 排布二进制网格的最少交换次数](https://leetcode.cn/problems/minimum-swaps-to-arrange-a-binary-grid/) · Medium · 灵茶山艾府：[冒泡排序（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1536.排布二进制网格的最少交换次数

[力扣](https://leetcode-cn.com/problems/minimum-swaps-to-arrange-a-binary-grid/)

题目要求排布后主对角线以上的数都为0，也就是说对于排布后的矩阵，其中第k行最后一个1出现的位置必须要在位置k之前。那么可以先对于每一行找出当前行最后一个1的位置，那么就会得到一个数组，而题目要求就转化成了以最少的次数交换数组中相邻的数字，使得数组中的每个数a[k]满足a[k] \<\= k。

对于这个问题，可以使用贪心法来处理，若当前位置上的值不满足要求，那么往后找到最近的一个满足条件的位置，然后通过两两交换逐位将满足条件的位置交换到当前位置即可。另外由于计算最后一个1的预处理的时间复杂度为O(n^2)，因此在这里也可以直接两重循环进行交换而没有必要再使用数据结构进行优化。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        pos_list = []
        n = len(grid)
        for i in range(n):
            pos_list.append(0)
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 1:
                    pos_list[-1] = j
                    break
        
        res = 0
        for i in range(n):
            if pos_list[i] <= i:
                continue
            
            now = pos_list[i]
            pos_list[i] = None
            for j in range(i + 1, n):
                pos_list[j], now = now, pos_list[j]
                res += 1
                if now <= i:
                    pos_list[i] = now
                    break
            
            if pos_list[i] is None:
                return -1
        
        return res
```
