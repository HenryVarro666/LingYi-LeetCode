---
title: "471. 编码最短长度的字符串"
aliases: ["yiduobo的每日leetcode 471.编码最短长度的字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600149831"
zhihu_id: "600149831"
zhihu_title: "yiduobo的每日leetcode 471.编码最短长度的字符串"
question_id: "471"
question: "编码最短长度的字符串"
problem_url: "https://leetcode.cn/problems/encode-string-with-shortest-length/"
created: "2023-01-19T22:58:47+08:00"
updated: "2023-01-19T22:58:47+08:00"
upvotes: 0
comments: 0
---

# 471. 编码最短长度的字符串

> **[yiduobo的每日leetcode 471.编码最短长度的字符串](https://zhuanlan.zhihu.com/p/600149831) · 知乎 · 2023-01-19 · 赞同 0**
> 力扣：[471. 编码最短长度的字符串](https://leetcode.cn/problems/encode-string-with-shortest-length/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

471.编码最短长度的字符串

[力扣](https://leetcode.cn/problems/encode-string-with-shortest-length/)

经典的动态规划问题，由于数据规模不大，因此不需要考虑进行太多优化。

令f[start][end]表示s中从start到end这一段子串编码后的最短长度是多少，那么对于f[start][end]：

1、不进行任何操作：

此时就有f[start][end] \= end - start + 1

2、执行重复子串压缩：

这种情况下，需要枚举压缩前缀的长度t，当子串长度length \= end - start + 1是t的倍数，且子串可以通过s[start : start + t]重复若干次得到，那么就可以进行重复子串压缩，在压缩后的子串长度就是

f[start][start + t - 1] + len(str(length / t)) + 2

一共有三个部分，分别是s[start : start + t]需要占据的空间、压缩次数这个数字需要占据的空间，以及左右两个括号需要占据的空间。在这里需要特别注意，s[start : start + t]占据的空间一定要用f[start][start + t - 1]来表示，因此可能出现嵌套压缩的情况。

这种情况下，就有

f[start][end] \= min(f[start][end], f[start][start + t - 1] + len(str(length / t)) + 2)

其中length % t \= 0且s[start : end + 1]可以由s[start : start + t]重复length / t次得到

另外，在这里判断s[start : end + 1]能否由s[start : start + t]重复若干次得到这个问题，如果直接枚举对比复杂度较高，需要进行一些预处理。比较简单的预处理方式就是先两两枚举s中的所有下标位置对(i, j)，计算s[i:]和s[j:]的最长公共前缀的长度，并将其储存在数组g当中。

接下来在判断s[start : end + 1]能否由s[start :start + t]重复若干次得到时，就可以依次枚举start + t、start + 2t、start +3t等位置，通过g[start][start + t]、g[start][start + 2t]等公共前缀的长度是否都大于等于t。

3、执行切分：

这种情况下，可以枚举切分的位置cut_pos，那么就有

f[start][end] \= min(f[start][end], f[start][cut_pos] + f[cut_pos + 1][end])

表示将子串切分成两个部分分别进行压缩

动态规划完成后，f[0][n - 1]就是最短的压缩长度，其中n是s的长度。

在写完代码之后，才发现题目要求的是压缩后的具体字符串，那么在这里需要额外添加两个数组cut和method，其中cut[start][end]用来记录f[start][end]在进行压缩是是否采用了切分的方式。若cut[start][end]为true，那么method[start][end]记录的就是f[start][end]的切分点cut_pos，若cut[start][end]为false，那么method[start][end]记录的就是f[start][end]执行重复子串压缩的前缀长度，当method[start][end]为0时表示不压缩。

当f[start][end]在进行状态转移时，同步更新cut[start][end]以及method[start][end]。当动态规划完成后，就可以通过cut和method，从状态[0][n - 1]出发倒推出整个构造的过程了。

最后附上python代码：

```python
class Solution(object):
    def encode(self, s):
        """
        :type s: str
        :rtype: str
        """

        n = len(s)
        g = [[0] * n for _ in range(n)]
        for j in range(n - 1, 0, -1):
            for i in range(j - 1, -1, -1):
                if s[i] == s[j]:
                    if j == n - 1:
                        g[i][j] = 1
                    else:
                        g[i][j] = g[i + 1][j + 1] + 1
        
        f = [[None] * n for _ in range(n)]
        cut = [[False] * n for _ in range(n)]
        method = [[0] * n for _ in range(n)]
        for length in range(1, n + 1):
            for start in range(n - length + 1):
                end = start + length - 1
                f[start][end] = length
                if start == end:
                    continue
                for t in range(1, length):
                    if length % t == 0:
                        flag = True
                        for p in range(start + t, end + 1, t):
                            if g[start][p] < t:
                                flag = False
                                break
                        if flag:
                            abbr_len = f[start][start + t - 1] + len(str(length / t)) + 2
                            if f[start][end] > abbr_len:
                                f[start][end] = abbr_len
                                method[start][end] = t

                for cut_pos in range(start, end):
                    if f[start][cut_pos] + f[cut_pos + 1][end] < f[start][end]:
                        cut[start][end] = True
                        method[start][end] = cut_pos
                        f[start][end] = f[start][cut_pos] + f[cut_pos + 1][end]

        def generate(start, end):
            if cut[start][end]:
                return generate(start, method[start][end]) + generate(method[start][end] + 1, end)
            elif method[start][end] > 0:
                return str((end - start + 1) / method[start][end]) + '[' + generate(start, start + method[start][end] - 1)+ ']'
            else:
                return s[start : end + 1]

        return generate(0, n - 1)
```
