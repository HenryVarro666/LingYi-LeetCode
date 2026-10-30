---
title: "1987. 不同的好子序列数目"
aliases: ["yiduobo的每日leetcode 1987.不同的好子序列数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/499431433"
zhihu_id: "499431433"
zhihu_title: "yiduobo的每日leetcode 1987.不同的好子序列数目"
question_id: "1987"
question: "不同的好子序列数目"
problem_url: "https://leetcode.cn/problems/number-of-unique-good-subsequences/"
difficulty: "Hard"
rating: 2422
created: "2022-04-16T01:05:57+08:00"
updated: "2022-04-16T01:05:57+08:00"
upvotes: 0
comments: 0
---

# 1987. 不同的好子序列数目

> **[yiduobo的每日leetcode 1987.不同的好子序列数目](https://zhuanlan.zhihu.com/p/499431433) · 知乎 · 2022-04-16 · 赞同 0**
> 力扣：[1987. 不同的好子序列数目](https://leetcode.cn/problems/number-of-unique-good-subsequences/) · Hard · 灵茶山艾府：[倒序动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1987.不同的好子序列数目

[力扣](https://leetcode-cn.com/problems/number-of-unique-good-subsequences/)

经典的动态规划问题，之前也遇到过类似的题目，不过本题还有两个额外限制，一个是不能重复，另一个是不能有前导0。

对于去重，可以在动态规划的过程中通过状态转移方程来实现，而对于前导0，有一种常见的技巧是反向计算。令f[i][j]表示倒数i个字符，以j为结尾时的合法子序列数目。

从后向前一趟遍历，对于当前字符char，无论是0还是1，都有

f[i][char] \= f[i - 1][0] + f[i - 1][1] + 1

表示将char接下来字符的末尾。由于f[i - 1][0]和f[i - 1][1]中的子序列都是互不相同的，因此在这些子序列末尾再加上一个1，得到的也是不同的子序列。而最后这个单独的1，则表示将当前char单独拎出来作为一个子序列。

这样又有一个问题：对于f[i][char]，是否会丢失掉f[i - 1][char]中的某些子序列？答案是不会。因为f[i - 1][char]中的子序列也是由char和char更前方的子序列构成的，那么使用当前的char替代f[i - 1][char]中最后一个char就会得到相同的字符串，因此不会丢失掉f[i - 1][char]中的子序列。

计算得到所有f之后，由于本题不能出现前导0，也就意味着f中以0结尾的子序列都是不可用的。当然，这里有一种特殊情况需要考虑，就是一个单独的0也是合法的，因此若字符串中有0，答案就是f[-1][1] + 1，否则答案就是f[-1][1]。

最后附上python代码：

```python
class Solution(object):
    def numberOfUniqueGoodSubsequences(self, binary):
        """
        :type binary: str
        :rtype: int
        """

        zero_cnt = 0
        one_cnt = 0
        mod = 10 ** 9 + 7
        zero_flag = False
        for char in binary[::-1]:
            if char == '0':
                zero_cnt += one_cnt + 1
                if zero_cnt >= mod:
                    zero_cnt -= mod
                zero_flag = True
            else:
                one_cnt += zero_cnt + 1
                if one_cnt >= mod:
                    one_cnt -= mod
        
        res = one_cnt
        if zero_flag:
            res += 1
            if res >= mod:
                res -= mod
        return res
```
