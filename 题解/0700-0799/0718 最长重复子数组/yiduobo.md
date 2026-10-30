---
title: "718. 最长重复子数组"
aliases: ["yiduobo的每日leetcode 718.最长重复子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/suffix-array", "题单/动态规划", "题单/字符串", "题单/动态规划/四-经典线性-DP", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/331760529"
zhihu_id: "331760529"
zhihu_title: "yiduobo的每日leetcode 718.最长重复子数组"
question_id: "718"
question: "最长重复子数组"
problem_url: "https://leetcode.cn/problems/maximum-length-of-repeated-subarray/"
difficulty: "Medium"
created: "2020-12-05T17:32:36+08:00"
updated: "2020-12-05T17:32:36+08:00"
upvotes: 0
comments: 0
---

# 718. 最长重复子数组

> **[yiduobo的每日leetcode 718.最长重复子数组](https://zhuanlan.zhihu.com/p/331760529) · 知乎 · 2020-12-05 · 赞同 0**
> 力扣：[718. 最长重复子数组](https://leetcode.cn/problems/maximum-length-of-repeated-subarray/) · Medium · 灵茶山艾府：[动态规划，附后缀数组 O(n+m) 做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

718.最长重复子数组

[力扣](https://leetcode-cn.com/problems/maximum-length-of-repeated-subarray/)

最长公共子串问题，经典做法是O(n^2)的动态规划，令f[i][j]表示以A[i - 1]以及B[j - 1]结尾的子串最长能匹配的长度，若A[i - 1] \= B[j - 1]，f[i][j] \= f[i - 1][j - 1] + 1，否则f[i][j] \= 0。

更好的做法是后缀数组，例如样例中的

1 2 3 2 1

3 2 1 4 7

我们先用分隔符将A和B拼起来，得到

1 2 3 2 1 \# 3 2 1 4 7

这个新串有若干个后缀字符串，分别为

7

4 7

1 4 7

2 1 4 7

3 2 1 4 7

\# 3 2 1 4 7

1 \# 3 2 1 4 7

2 1 \# 3 2 1 4 7

3 2 1 \# 3 2 1 4 7

2 3 2 1 \# 3 2 1 4 7

1 2 3 2 1 \# 3 2 1 4 7

那么现在的问题就变成了找出其中两个后缀，要求其中一个包含\#号，一个不包含\#号，且二者的**最长公共前缀**最长。

在这里，找到的两个后缀为

3 2 1 4 7

3 2 1 \# 3 2 1 4 7

最长公共前缀为3 2 1，就是最终答案

那么找这个最长公共前缀，可以先将这些后缀进行排序，在这里可以使用O(nlogn)的倍增算法或者O(n)的dc3算法。完成排序之后，直接一趟扫描，利用前缀的性质就能找出这个最长的公共前缀。具体的算法和证明在这里就不展开了。

我最后实现的还是经典的动态规划算法，因为实现难度相比后缀数组容易多了：

```python
class Solution(object):
    def findLength(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: int
        """

        n = len(A)
        m = len(B)
        f = [[0] * (m + 1) for _ in range(n + 1)]
        res = 0
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if A[i - 1] == B[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    res = max(res, f[i][j])
                
        return res
```
