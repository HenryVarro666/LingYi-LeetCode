---
title: "634. 寻找数组的错位排列"
aliases: ["yiduobo的每日leetcode 634.寻找数组的错位排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602708437"
zhihu_id: "602708437"
zhihu_title: "yiduobo的每日leetcode 634.寻找数组的错位排列"
question_id: "634"
question: "寻找数组的错位排列"
problem_url: "https://leetcode.cn/problems/find-the-derangement-of-an-array/"
created: "2023-02-02T00:24:11+08:00"
updated: "2023-02-02T00:24:11+08:00"
upvotes: 1
comments: 0
---

# 634. 寻找数组的错位排列

> **[yiduobo的每日leetcode 634.寻找数组的错位排列](https://zhuanlan.zhihu.com/p/602708437) · 知乎 · 2023-02-02 · 赞同 1**
> 力扣：[634. 寻找数组的错位排列](https://leetcode.cn/problems/find-the-derangement-of-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

634.寻找数组的错位排列

[力扣](https://leetcode.cn/problems/find-the-derangement-of-an-array/)

非常经典的错排问题。先上递推式：

当n \= 1时，f[n] \= 0

当n \= 2时，f[n] \= 1

当n >\= 3时，f[n] \= (n - 1) \* (f[n - 1] + f[n - 2])

关于最后这里的f[n] \= (n - 1) \* (f[n - 1] + f[n - 2])，一个简单的理解是考虑n的位置。n只能在1到n - 1中选一个位置来放置，不妨设放置在了位置k上。

接下来，若k恰好放置在位置n上，那么剩下的1到k - 1以及k + 1到n - 1，这一共n - 2个数可以形成的错排数量就是f[n - 2]。

若k没有放置在位置n上，那么在这里可以将位置n认为是k的正确位置，而接下来需要将1到n - 1这一共n - 1个数错位放置在1到k - 1以及k + 1到n这一共n - 1个位置上，那么可以形成的错排数量就是f[n - 1]。

综合起来，就是(f[n - 1] + f[n - 2])。由于1到n - 1中谁来当这个k都是等价的，因此总的情况数量还需要乘以n - 1，于是就有f[n] \= (n - 1) \* (f[n - 1] + f[n - 2])

根据上面的递推式，一趟遍历计算结果最终的f[n]就行了。

另外注意到递推式只涉及到前两项，因此可以使用两个变量迭代来节省数组的空间。由于在递推式中存在一项变量，因此在这里不太适合使用矩阵乘法来进行加速。

最后附上python代码：

```python
class Solution(object):
    def findDerangement(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 0
        
        if n == 2:
            return 1
        
        a, b = 0, 1
        mod = 10 ** 9 + 7
        for index in range(3, n + 1):
            a, b = b, (index - 1) * (b + a) % mod
        
        return b
```
