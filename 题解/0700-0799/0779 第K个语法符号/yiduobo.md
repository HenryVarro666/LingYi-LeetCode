---
title: "779. 第K个语法符号"
aliases: ["yiduobo的每日leetcode 779.第K个语法符号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/340227820"
zhihu_id: "340227820"
zhihu_title: "yiduobo的每日leetcode 779.第K个语法符号"
question_id: "779"
question: "第K个语法符号"
problem_url: "https://leetcode.cn/problems/k-th-symbol-in-grammar/"
created: "2020-12-28T23:40:45+08:00"
updated: "2020-12-28T23:40:45+08:00"
upvotes: 0
comments: 0
---

# 779. 第K个语法符号

> **[yiduobo的每日leetcode 779.第K个语法符号](https://zhuanlan.zhihu.com/p/340227820) · 知乎 · 2020-12-28 · 赞同 0**
> 力扣：[779. 第K个语法符号](https://leetcode.cn/problems/k-th-symbol-in-grammar/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

779.第K个语法符号

[力扣](https://leetcode-cn.com/problems/k-th-symbol-in-grammar/)

很有意思的题目，想起当时搞竞赛的时候接触到的分形之类的东西了。

首先，可以发现每一行的字符串就是将上一行复制一遍，然后逐位取反一遍再拼接在一起，那么第n行的第k个字符与第n - 1行的第k个字符必然是一样的，当然有个前提是第n - 1行有第k个字符。

为了更契合二进制，我们从0开始计数，即对于题目给出的k，先执行k \= k - 1。

接下来对于k，设其有p位，由之前提到的逐位取反可得，该串的第0位到第2^(p - 1) - 1位这一段，与第2^(p - 1)到2^p - 1这一段是逐位相反的。

对于串中的第k位，其应当与串中的第k - 2^(p - 1)位相反。例如样例中的k \= 5，我们先执行k \= k - 1，得到k \= 4，二进制表示为100，此时有p \= 3。于是对于字符串01101001，其第0到3位为0110，而其第4到7位为1001，对于k \= 4这一位，其实际上与字符串的第0位相反。

注意到，k - 2^(p - 1)这个操作实际上就是剥离k最高位上的1，而每次进行这个剥离操作之后，其字符都会取反，于是可以从高位开始逐位剥离k最高位上的1，每次剥离之后对答案取反直到k \= 0。进一步的，注意到这里实际上就是统计k中1的个数，并不一定要从最高位开始，于是可以通过k \= k & (k - 1)这个操作逐个分离k最低位的1，统计分离的次数。若最终分离了偶数次，那么就相当于没有翻转，于是返回0，否则返回1。

对于这类带复制性质的问题，通过递归或者类递归的方法找状态之间的关系总是好使的。最后附上python代码：

```python
class Solution(object):
    def kthGrammar(self, N, K):
        """
        :type N: int
        :type K: int
        :rtype: int
        """

        cnt = 0
        K -= 1
        while K:
            K &= K - 1
            cnt += 1
        
        return cnt % 2
```
