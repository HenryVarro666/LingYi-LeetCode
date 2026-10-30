---
title: "2033. 获取单值网格的最小操作数"
aliases: ["yiduobo的每日leetcode 2033.获取单值网格的最小操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/quickselect", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/508485950"
zhihu_id: "508485950"
zhihu_title: "yiduobo的每日leetcode 2033.获取单值网格的最小操作数"
question_id: "2033"
question: "获取单值网格的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-a-uni-value-grid/"
difficulty: "Medium"
rating: 1672
created: "2022-05-02T18:25:38+08:00"
updated: "2022-05-02T18:25:38+08:00"
upvotes: 0
comments: 0
---

# 2033. 获取单值网格的最小操作数

> **[yiduobo的每日leetcode 2033.获取单值网格的最小操作数](https://zhuanlan.zhihu.com/p/508485950) · 知乎 · 2022-05-02 · 赞同 0**
> 力扣：[2033. 获取单值网格的最小操作数](https://leetcode.cn/problems/minimum-operations-to-make-a-uni-value-grid/) · Medium · 灵茶山艾府：[中位数贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2033.获取单值网格的最小操作数

[力扣](https://leetcode-cn.com/problems/minimum-operations-to-make-a-uni-value-grid/)

首先需要判断能否将网格变为单值网络。题目中的每次操作只能让某个数加上x或者减去x，这也就意味着无论怎么操作，网格中的每个数对x的余数是不会变的，那么就需要先检测网格中每个数对x取模的余数是否一致，如果不一致，那么直接返回-1。

接下来考虑如何进行变换。先将网格中的每个数都写成ax + b的形式，由于这里的b都一样所以无需考虑，只需将每个位置的a都变为一致即可。

到了这里，问题就转化成了给出一个数组，每次可以让数组中的数加1或者减1，问最少需要多少次操作让数组中的数变为一致。这个问题之前也遇到过，最优的做法就是将所有数都变为数组的中位数。另外，当数组长度为偶数时，无需计算二者的平均值作为中位数，而是可以任选最中间两个数中的一个。接下来证明这个结论的正确性：

先将数组从小到大进行排序，然后从两侧向中间两两一组进行考察。对于当前考察的两个数mi和ma，设mi \<\= ma，那么对于最终选定的值target，有三种情况：

1、target \< mi：

此时的操作次数为ma - target + mi - target \= (mi - target) \* 2 + (ma - mi)

2、mi \<\= target \<\= ma：

此时的操作次数为ma - target + target - mi \= ma - mi

3、ma \< target：

此时的操作次数为target - ma + target - mi \= (target - ma) \* 2 + (ma - mi)

可以发现，情况2所需的操作次数是最少的，因此最优的处理方法就是选择数组的中位数作为target。

回到原问题。得到数组后，同样是从小到大排序找出数组的中位数，然后一趟遍历，将每个数与中位数差的绝对值累加起来即为最终答案。

当然，在这里使用快速选择算法来找中位数是更好的解法，可以将最终的时间复杂度由O(mn \* log(mn))优化到O(mn)。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, grid, x):
        """
        :type grid: List[List[int]]
        :type x: int
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        r = grid[0][0] % x
        num_list = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] % x != r:
                    return -1
                num_list.append(grid[i][j] / x)
        
        num_list = sorted(num_list)
        target = num_list[len(num_list) / 2]
        res = 0
        for num in num_list:
            res += abs(num - target)
        
        return res
```
