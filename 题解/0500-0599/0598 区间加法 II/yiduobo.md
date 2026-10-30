---
title: "598. 范围求和"
aliases: ["yiduobo的每日leetcode 598.范围求和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268420632"
zhihu_id: "268420632"
zhihu_title: "yiduobo的每日leetcode 598.范围求和"
question_id: "598"
question: "区间加法 II"
problem_url: "https://leetcode.cn/problems/range-addition-ii/"
difficulty: "Easy"
rating: 1400
created: "2020-10-24T21:22:30+08:00"
updated: "2020-10-24T21:22:30+08:00"
upvotes: 0
comments: 0
---

# 598. 范围求和

> **[yiduobo的每日leetcode 598.范围求和](https://zhuanlan.zhihu.com/p/268420632) · 知乎 · 2020-10-24 · 赞同 0**
> 力扣：[598. 区间加法 II](https://leetcode.cn/problems/range-addition-ii/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

598.范围求和<https://leetcode-cn.com/problems/range-addition-ii/>

注意到题目里面的矩阵都是从左上角开始的，因此每次操作的矩形都必然有部分重合，只要找出所有矩形都重合的部分就是最终答案。

由于这里所有的矩形左上角都重合，那么对于任意两个矩形，不妨设它们的右下角坐标分别为(x1, y1)和(x2, y2)，那么二者重叠的部分左上角不变，右下角为(min(x1, x2), min(y1, y2))。

对于所有矩形的重叠部分，我们可以认为求前k个矩形的重叠部分就是求前k - 1个矩形的重叠部分，和第k个矩形形成的重叠部分是什么，于是一趟遍历，求出x和y的最小值即可。

最后附上python代码：

```
class Solution(object):
    def maxCount(self, m, n, ops):
        """
        :type m: int
        :type n: int
        :type ops: List[List[int]]
        :rtype: int
        """

        for x, y in ops:
            m = min(m, x)
            n = min(n, y)
        
        return m * n
```
