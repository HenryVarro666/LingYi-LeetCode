---
title: "4022. 无限字符串里的第K个数字"
aliases: ["yiduobo的每日leetcode 4022.无限字符串里的第K个数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2073220663230329186"
zhihu_id: "2073220663230329186"
zhihu_title: "yiduobo的每日leetcode 4022.无限字符串里的第K个数字"
question_id: "4022"
question: "无限字符串里第 K 个数字"
problem_url: "https://leetcode.cn/problems/k-th-digit-in-infinite-string/"
difficulty: "Medium"
rating: 1915
created: "2026-08-19T01:43:36+08:00"
updated: "2026-08-19T01:43:43+08:00"
upvotes: 1
comments: 0
---

# 4022. 无限字符串里的第K个数字

> **[yiduobo的每日leetcode 4022.无限字符串里的第K个数字](https://zhuanlan.zhihu.com/p/2073220663230329186) · 知乎 · 2026-08-19 · 赞同 1**
> 力扣：[4022. 无限字符串里第 K 个数字](https://leetcode.cn/problems/k-th-digit-in-infinite-string/) · Medium · 灵茶山艾府：[数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4022.无限字符串里的第K个数字

<https://leetcode.cn/problems/k-th-digit-in-infinite-string/description/>

题目给出一个整数k，大小不超过10^15。

现在先将所有正整数的十进制表示不添加任何分隔符拼接而成的字符串。

对于每个非负整数b，块b包含从10 \* b到10 \* b + 9的正整数。若b为偶数，那么按照递增的顺序附加整数，否则按照递减的顺序附加整数。也就是说，字符串会按照1到9，然后是19到10，然后是20到29，接着是39到30，依此类推。

问字符串中第k个数字是什么(下标从1开始)。

题目中k的规模极大，因此必须找规律高效计算。

一个直观的思路是先按照数字的位数进行讨论，因为相同位数的数字是连续的。

- 对于一位数，是1-9共9个。
- 对于两位数，是10到99共90个。
- 对于三位数，是100到999共900个。
- ...

可以发现，对于长度为length的数，其范围就是10^(length - 1)到10^length - 1，一共10^(length - 1) \* 9个，而这些数字全部填充进字符串，一共会占据10^(length - 1) \* 9 \* length位。

基于这一点，就可以从小到大枚举length，若当前的k大于10^(length - 1) \* 9 \* length，那么就让k减去这个值，然后将length加上1。这样一来，就确定了最终答案所在数字的位数。

接下来，由于位数已经确定了，那么就可以通过k除以位数来确定最终答案所在的数字，是位数为length的数字中的第几个，从而最终确定这是字符串中的第几个数字x。

需要注意的是，由于题目有按照b的奇偶性选择正序还是逆序的要求，因此在这里还需要通过x除以10找出块号b。若b为偶数，那么字符串中的第x个数字就是x自身，反之，则需要将x的最低位变为对称的数字，即使用9减去这个最低位。

得到最终的具体数字x后，其中的第(k - 1) % length位数字即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def kthDigit(self, k):
        """
        :type k: int
        :rtype: int
        """
        
        p10 = 1
        length = 1

        while k > p10 * 9 * length:
            k -= p10 * 9 * length
            p10 *= 10
            length += 1

        x = (k - 1) // length + p10
        b = x // 10
        if b % 2 == 1:
            x = x + 9 - (x % 10) * 2
        return int(str(x)[(k - 1) % length])
```
