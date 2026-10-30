---
title: "91. 解码方法"
aliases: ["yiduobo的每日leetcode 91.解码方法"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/136536408"
zhihu_id: "136536408"
zhihu_title: "yiduobo的每日leetcode 91.解码方法"
question_id: "91"
question: "解码方法"
problem_url: "https://leetcode.cn/problems/decode-ways/"
created: "2020-04-26T21:58:51+08:00"
updated: "2020-04-26T21:58:51+08:00"
upvotes: 1
comments: 0
---

# 91. 解码方法

> **[yiduobo的每日leetcode 91.解码方法](https://zhuanlan.zhihu.com/p/136536408) · 知乎 · 2020-04-26 · 赞同 1**
> 力扣：[91. 解码方法](https://leetcode.cn/problems/decode-ways/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

91.解码方法<https://leetcode-cn.com/problems/decode-ways/submissions/>

动态规划的题目。

f[i]表示前i位一共有多少种解码方式，那么：

1、f[i]初始值为0。

2、如果s[i - 1]在0到9之间，那么可以将s[i - 1]单独解码，此时f[i] +\= f[i - 1]。

3、如果s[i - 2]与s[i - 1]组合起来在10到26之间，那么可以将s[i - 2]与s[i - 1]放在一起解码，此时f[i] +\= f[i - 2]。

由于f[i]的值只受f[i - 1]与f[i - 2]影响，因此无需维护f数组，只需要通过三个变量倒一倒就行了。另外，还需要注意i为1和2时的边界情况。

一趟扫描就能得到答案，因此最终的时间复杂度为O(n)。由于这里状态转移的不确定性，因此不能使用矩阵乘法进行加速。

最后附上python代码：

```python
class Solution(object):
    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """

        a = 0
        if int(s[0]) >= 1 and int(s[0]) <= 9:
            a = 1
        if len(s) == 1:
            return a

        b = 0
        if int(s[1]) >= 1 and int(s[1]) <= 9:
            b = a
        if int(s[0:2]) >= 10 and int(s[0:2]) <= 26:
            b += 1

        c = 0
        for index in range(2, len(s)):
            if int(s[index]) >= 1 and int(s[index]) <= 9:
                c += b
            if int(s[index - 1 : index + 1]) >= 10 and int(s[index - 1 : index + 1]) <= 26:
                c += a
            a = b
            b = c
            c = 0

        return b
```
