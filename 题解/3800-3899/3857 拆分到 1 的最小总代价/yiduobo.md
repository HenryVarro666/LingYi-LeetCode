---
title: "3857. 拆分到1的最小总代价"
aliases: ["yiduobo的每日leetcode 3857.拆分到1的最小总代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2013642660959777510"
zhihu_id: "2013642660959777510"
zhihu_title: "yiduobo的每日leetcode 3857.拆分到1的最小总代价"
question_id: "3857"
question: "拆分到 1 的最小总代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-split-into-ones/"
difficulty: "Medium"
created: "2026-03-07T15:58:58+08:00"
updated: "2026-03-07T15:58:58+08:00"
upvotes: 0
comments: 1
---

# 3857. 拆分到1的最小总代价

> **[yiduobo的每日leetcode 3857.拆分到1的最小总代价](https://zhuanlan.zhihu.com/p/2013642660959777510) · 知乎 · 2026-03-07 · 赞同 0**
> 力扣：[3857. 拆分到 1 的最小总代价](https://leetcode.cn/problems/minimum-cost-to-split-into-ones/) · Medium · 灵茶山艾府：[等价转化，O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3857.拆分到1的最小总代价

<https://leetcode.cn/problems/minimum-cost-to-split-into-ones/description/>

题目给出一个整数n，其大小在1到500之间。

在每次操作中，可以将一个整数x，拆分为两个正整数a和b，满足a + b \= x，此次操作的代价为a \* b。

问将n拆分为n个1所需的最小总代价。

由于n的取值范围不大，因此可以使用动态规划进行求解。令f[x]表示将x拆分为x个1所需的最小总代价，那么对于f[x]，就有f[x] \= min(f[y] + f[x - y] + x \* y)，其中1 \<\= y \< x。计算完成后，f[n]即为最终答案。

另外，对于上面这个式子，直接观察比较难找出规律，但是如果先计算n较小的情况，可以发现

f[1] \= 0

f[2] \= 1 \= 2 \* (2 - 1) // 2

f[3] \= 3 \= 3 \* (3 - 1) // 2

...

更进一步的，若对于1到n - 1之间的所有x，都满足f[x] \= x \* (x - 1) // 2，那么对于f[n]，不妨设其第一步的最优做法是拆分为a和b，那么就有

f[n] \= f[a] + f[b] + a \* b \= a \* (a - 1) // 2 + b \* (b - 1) // 2 + a \* b

将其中的a^2 // 2 + b^2 // 2 + a \* b合并到一起，就是(a + b)^2 // 2，即n^2 // 2，而对于剩下的-a // 2 - b // 2，恰好就是-n // 2，于是就有

f[n] \= (n^2 - n) // 2 \= n \* (n - 1) // 2

也就是说，本题的答案就是n \* (n - 1) // 2

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        return n * (n - 1) // 2
```
