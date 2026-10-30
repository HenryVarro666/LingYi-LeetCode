---
title: "2507. 使用质因数之和替换后可以取到的最小值"
aliases: ["yiduobo的每日leetcode 2507.使用质因数之和替换后可以取到的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634310604"
zhihu_id: "634310604"
zhihu_title: "yiduobo的每日leetcode 2507.使用质因数之和替换后可以取到的最小值"
question_id: "2507"
question: "使用质因数之和替换后可以取到的最小值"
problem_url: "https://leetcode.cn/problems/smallest-value-after-replacing-with-sum-of-prime-factors/"
difficulty: "Medium"
rating: 1500
created: "2023-06-04T01:00:29+08:00"
updated: "2023-06-04T01:00:29+08:00"
upvotes: 0
comments: 0
---

# 2507. 使用质因数之和替换后可以取到的最小值

> **[yiduobo的每日leetcode 2507.使用质因数之和替换后可以取到的最小值](https://zhuanlan.zhihu.com/p/634310604) · 知乎 · 2023-06-04 · 赞同 0**
> 力扣：[2507. 使用质因数之和替换后可以取到的最小值](https://leetcode.cn/problems/smallest-value-after-replacing-with-sum-of-prime-factors/) · Medium · 灵茶山艾府：[暴力](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2507.使用质因数之和替换后可以取到的最小值

[力扣](https://leetcode.cn/problems/smallest-value-after-replacing-with-sum-of-prime-factors/)

由于题目的数据规模大，因此直接使用暴力法就行了。另外如果本题有多组询问，则可以先通过筛法找出每个数最大的质因子，然后通过这个质因子做分解质因数后形成类似并查集的结构，查询时则直接套用路径压缩查找即可。

最后附上python代码：

```python
class Solution(object):
    def smallestValue(self, n):
        """
        :type n: int
        :rtype: int
        """

        f = range(n + 1)
        x = 2
        while x * x <= n:
            if f[x] == x:
                now = x + x
                while now <= n:
                    f[now] = x
                    now += x
            x += 1

        now = n
        while True:
            pre = now
            s = 0
            while f[now] != now:
                s += f[now]
                now /= f[now]
            
            s += now
            now = s
            if s == pre:
                break

        return now
```
