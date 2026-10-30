---
title: "1955. 统计特殊子序列的数目"
aliases: ["yiduobo的每日leetcode 1955.统计特殊子序列的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/492771152"
zhihu_id: "492771152"
zhihu_title: "yiduobo的每日leetcode 1955.统计特殊子序列的数目"
question_id: "1955"
question: "统计特殊子序列的数目"
problem_url: "https://leetcode.cn/problems/count-number-of-special-subsequences/"
difficulty: "Hard"
rating: 2125
created: "2022-04-04T00:20:24+08:00"
updated: "2022-04-04T00:20:25+08:00"
upvotes: 0
comments: 0
---

# 1955. 统计特殊子序列的数目

> **[yiduobo的每日leetcode 1955.统计特殊子序列的数目](https://zhuanlan.zhihu.com/p/492771152) · 知乎 · 2022-04-04 · 赞同 0**
> 力扣：[1955. 统计特殊子序列的数目](https://leetcode.cn/problems/count-number-of-special-subsequences/) · Hard · 灵茶山艾府：[动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1955.统计特殊子序列的数目

[力扣](https://leetcode-cn.com/problems/count-number-of-special-subsequences/)

经典的动态规划问题。令f[i][0]表示s[0]到s[i]这一段中，全部为0的子序列的数目。f[i][1]表示s[0]到s[i]这一段中，形如00...011...1的子序列的数目。f[i][2]表示s[0]到s[i]这一段中，题目要求的特殊子序列的数目。

对于f[i][j]：

1、若s[i]为0：

首先就有f[i][1] \= f[i - 1][1]，f[i][2] \= f[i - 1][2]

接下来考虑f[i][0]。在这里可以不将s[i]加入到子序列中，那么就有f[i - 1][0]个子序列保底。而对于这f[i - 1][0]个子序列，将s[i]加入到这些子序列的末尾都是合法的答案，因此还可以再提供f[i - 1][0]个合法的子序列。除此之外，将s[i]单独拎出来当做一个子序列也是一种合法的情况，因此就有

f[i][0] \= f[i - 1][0] + f[i - 1][0] + 1

2、若s[i]为1：

首先就有f[i][0] \= f[i - 1][0]，f[i][2] \= f[i - 1][2]

接下来考虑f[i][1]。在这里同样是三种情况：不将s[i]加入到子序列中、将s[i]加入到f[i - 1][1]中所有子序列的末尾，以及将s[i]加入到f[i - 1][0]中所有子序列的末尾，因此就有

f[i][1] \= f[i - 1][1] + f[i - 1][1] + f[i - 1][0]

3、若s[i]为2：

首先就有f[i][0] \= f[i - 1][0]，f[i][1] \= f[i - 1][1]

接下来考虑f[i][2]。也是三种情况：不将s[i]加入到子序列中、将s[i]加入到f[i - 1][2]中所有子序列的末尾，以及将s[i]加入到f[i - 1][1]中所有子序列的末尾，因此就有

f[i][2] \= f[i - 1][2] + f[i - 1][2] + f[i - 1][1]

全部计算完成后，f[n - 1][2]就是最终答案。

注意到f每一轮只与上一轮有关，因此在这里可以使用变量迭代替换数组。

最后附上python代码：

```python
class Solution(object):
    def countSpecialSubsequences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        zero_cnt = 0
        one_cnt = 0
        res = 0
        mod = 10 ** 9 + 7
        for num in nums:
            if num == 0:
                zero_cnt += zero_cnt + 1
                zero_cnt %= mod
            elif num == 1:
                one_cnt += one_cnt + zero_cnt
                one_cnt %= mod
            else:
                res += res + one_cnt
                res %= mod

        return res
```
