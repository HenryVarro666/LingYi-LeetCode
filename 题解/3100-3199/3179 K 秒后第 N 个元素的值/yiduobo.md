---
title: "3179. K秒后第N个元素的值"
aliases: ["yiduobo的每日leetcode 3179.K秒后第N个元素的值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705855939"
zhihu_id: "705855939"
zhihu_title: "yiduobo的每日leetcode 3179.K秒后第N个元素的值"
question_id: "3179"
question: "K 秒后第 N 个元素的值"
problem_url: "https://leetcode.cn/problems/find-the-n-th-value-after-k-seconds/"
difficulty: "Medium"
created: "2024-06-28T00:10:43+08:00"
updated: "2024-06-28T00:10:43+08:00"
upvotes: 1
comments: 0
---

# 3179. K秒后第N个元素的值

> **[yiduobo的每日leetcode 3179.K秒后第N个元素的值](https://zhuanlan.zhihu.com/p/705855939) · 知乎 · 2024-06-28 · 赞同 1**
> 力扣：[3179. K 秒后第 N 个元素的值](https://leetcode.cn/problems/find-the-n-th-value-after-k-seconds/) · Medium · 灵茶山艾府：[组合数学 O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3179.K秒后第N个元素的值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-n-th-value-after-k-seconds/)

题目给出两个整数n和k，初始情况下有一个长度为n的数组a，其中元素的值都为1。接下来每一秒，数组中的每个元素a[i]将在同一时刻更新为上一秒的a[0] + a[1] + ... + a[i]，问k秒后数组中的最后一个元素是多少。

令f[i][j]表示第i秒时数组中的第j个元素等于多少，那么对于f[i][j]，就有

f[i][j] \= f[i - 1][0] + f[i - 1][1] + ... + f[i - 1][j - 1] + f[i - 1][j]

另一方面，又有

f[i][j - 1] \= f[i - 1][0] + f[i - 1][1] + ... + f[i - 1][j - 1]

那么就有

f[i][j] \= f[i][j - 1] + f[i - 1][j]

于是只需一趟遍历，计算f[n][k + 1]就可以了。

另外观察其中的数字可以发现数组值是很明显的组合数，其中f[i][j] \= C(i + j - 1, i)，因此也可以直接配合乘法逆元计算组合数，时间复杂度会更好。

最后附上python代码：

```python
class Solution(object):
    def valueAfterKSeconds(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        f = [[0] * n for _ in range(k + 1)]
        for i in range(n):
            f[0][i] = 1
        for i in range(1, k + 1):
            f[i][0] = 1
            for j in range(1, n):
                f[i][j] = f[i][j - 1] + f[i - 1][j]
                if f[i][j] >= mod:
                    f[i][j] -= mod
        
        return f[-1][-1]
```
