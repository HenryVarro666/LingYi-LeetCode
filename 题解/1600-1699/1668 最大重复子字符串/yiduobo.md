---
title: "1668. 最大重复子字符串"
aliases: ["yiduobo的每日leetcode 1668.最大重复子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/442962108"
zhihu_id: "442962108"
zhihu_title: "yiduobo的每日leetcode 1668.最大重复子字符串"
question_id: "1668"
question: "最大重复子字符串"
problem_url: "https://leetcode.cn/problems/maximum-repeating-substring/"
created: "2021-12-09T00:04:54+08:00"
updated: "2021-12-09T00:04:54+08:00"
upvotes: 0
comments: 0
---

# 1668. 最大重复子字符串

> **[yiduobo的每日leetcode 1668.最大重复子字符串](https://zhuanlan.zhihu.com/p/442962108) · 知乎 · 2021-12-09 · 赞同 0**
> 力扣：[1668. 最大重复子字符串](https://leetcode.cn/problems/maximum-repeating-substring/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1668.最大重复子字符串

[力扣](https://leetcode-cn.com/problems/maximum-repeating-substring/)

本题是easy题的原因是数据规模很小，实际上本题是存在O(n)的做法的。

首先这里的最大重复子字符串必然是由连续出现的word组成的，那么就可以先将word不断重复扩展到sequence的长度，那么对于这两个字符串的某个公共子串而言，只要这个公共子串的结尾恰好对应了word的结尾，那么说明这个公共子串的后缀就是由word复制若干遍得到的，于是可以根据这个公共子串的长度以及word的长度求出重复的次数。那么在这里只需要找出一个长度最长，且结尾对应了word的结尾的公共子串即可。

对于两个字符串的最长公共子串问题，则可以使用后缀数组在O(n)的时间复杂度内求出来。

当然实现是非常复杂的，我在这里偷懒用了常规的O(n^2)的动态规划。

在这里再简单解释一下为什么需要公共子串的结尾与word的结尾对齐。例如word为abc，那么重复3次之后就是abcabcabc。此时找出了一个最长公共子串为bcabca，这个子串的长度为6，直接按长度计算就会认为是重复了两次，但是实际上这里面只有一个abc。对于结尾与word结尾对其的子串而言则不会有这个问题，因此在计算最终答案时需要进行这样一个判断，若当前公共子串的结尾与word的结尾没有对齐，那么答案需要减去1。

最后附上python代码：

```python
class Solution(object):
    def maxRepeating(self, sequence, word):
        """
        :type sequence: str
        :type word: str
        :rtype: int
        """

        m = len(sequence)
        n = len(word)
        p = m / n
        f = [[0] * (n * p) for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n * p):
                if sequence[i] == word[j % n]:
                    f[i][j] = 1
                    if i > 0 and j > 0:
                        f[i][j] += f[i - 1][j - 1]
                
                res = max(res, f[i][j] / n - (1 if j % n != n - 1 else 0))

        return res
```
