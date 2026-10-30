---
title: "3193. 统计逆序对的数目"
aliases: ["yiduobo的每日leetcode 3193.统计逆序对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "leetcode/di-tui", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/动态规划/十一-优化-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706709879"
zhihu_id: "706709879"
zhihu_title: "yiduobo的每日leetcode 3193.统计逆序对的数目"
question_id: "3193"
question: "统计逆序对的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-inversions/"
difficulty: "Hard"
rating: 2266
created: "2024-07-03T02:52:52+08:00"
updated: "2024-07-03T02:52:52+08:00"
upvotes: 2
comments: 0
---

# 3193. 统计逆序对的数目

> **[yiduobo的每日leetcode 3193.统计逆序对的数目](https://zhuanlan.zhihu.com/p/706709879) · 知乎 · 2024-07-03 · 赞同 2**
> 力扣：[3193. 统计逆序对的数目](https://leetcode.cn/problems/count-the-number-of-inversions/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到终极优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3193.统计逆序对的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-inversions/description/)

题目给出一个整数n以及一个二维数组requirements，其中requirements\[i\] \= \[end\[i\], cnt\[i\]\]。现在要求找出由0到n - 1构成的排列perm，满足对于所有的perm\[0\]到perm\[end\[i\]\]构成的序列中恰好有cnt\[i\]个逆序对，问有多少个合法的排列。

题目中n最大可达300，cnt可达400。

由于n的规模并不小，那么在这里使用暴力法肯定是不行的，只能考虑组合数学或者动态规划。我没有想到组合数学的方法，所以老老实实用动态规划来求解。

令f[i][j]表示由i个数构成，且有j组逆序对的排列的数量，那么对于f[i][j]，考虑最后这个元素应该怎么选择。如果选择这i个数中最大的数，那么无论前i - 1个元素怎么排，都不会与最后这个元素形成逆序对，那么就有f[i][j] +\= f[i - 1][j]。接下来，如果选择次大的数，那么无论前i - 1个元素怎么排，其中的最大值都会与最后这个元素形成逆序对，而其他的元素则都不会产生影响，因此就有f[i][j] +\= f[i - 1][j - 1]。以此类推，就有

f[i][j] \= f[i - 1][j] + f[i - 1][j - 1] + ... + f[i - 1][max(0, j - i + 1)]

最后一项中的j - i + 1是当将这i个数中的最小值放在最后时，将与前面的排列形成i - 1组逆序对，因此就是f[i - 1][j - (i - 1)]，但是逆序对数量不可能为负数，因此要与0取max。

这样一来，就可以遍历i和j，若当前的i与requirements中的某个end相等，那么就只需要计算其对应的cnt，否则就需要计算所有可行的j。

上面算法的时间复杂度为O(n^2 \* max(cnt))，就本题的数据规模来看是比较微妙的，最好还是想办法优化一下。

观察状态转移的式子，这是一个区间和，那么就可以用前缀和来进行优化。

令s[i][j] \= s[i][0] + s[i][1] + ... + s[i][j]，那么对于f[i][j]：

1、若j \<\= i - 1，就有f[i][j] \= f[i - 1][j] + f[i - 1][j - 1] + ... + f[i - 1][0]，即f[i][j] \= s[i - 1][j]

2、若j > i - 1，就有f[i][j] \= f[i - 1][j] + f[i - 1][j - 1] + ... + f[i - 1][j - i + 1] \= s[i - 1][j] - s[i - 1][j - i]

计算完f[i][j]后，还需要通过s[i][j - 1] + f[i][j]来更新s[i][j]

这样一来，时间复杂度就优化到了O(n \* max(cnt))。

另外注意到f的更新只取决于s上一轮的结果，因此可以省去i这一维，先用s更新f，然后再用f更新s。

最后附上python代码：

```python
class Solution(object):
    def numberOfPermutations(self, n, requirements):
        """
        :type n: int
        :type requirements: List[List[int]]
        :rtype: int
        """

        req_dict = {}
        for end, cnt in requirements:
            req_dict[end] = cnt
            if end == 0 and cnt != 0:
                return 0

        mod = 10 ** 9 + 7
        f = [0] * (req_dict[n - 1] + 1)
        f[0] = 1
        s = [1] * (req_dict[n - 1] + 1)
        for i in range(2, n + 1):
            if i - 1 in req_dict:
                start = end = req_dict[i - 1]
            else:
                start, end = 0, req_dict[n - 1]

            for j in range(req_dict[n - 1] + 1):
                if start <= j <= end:
                    if j <= i - 1:
                        f[j] = s[j]
                    else:
                        f[j] = (s[j] - s[j - i] + mod) % mod
                else:
                    f[j] = 0

            s[0] = f[0]
            for j in range(1, req_dict[n - 1] + 1):
                s[j] = (s[j - 1] + f[j]) % mod

        return f[-1]
```
