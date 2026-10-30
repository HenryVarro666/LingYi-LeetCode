---
title: "3821. 二进制中恰好K个1的第N小整数"
aliases: ["yiduobo的每日leetcode 3821.二进制中恰好K个1的第N小整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1998881518173569613"
zhihu_id: "1998881518173569613"
zhihu_title: "yiduobo的每日leetcode 3821.二进制中恰好K个1的第N小整数"
question_id: "3821"
question: "二进制中恰好K个1的第N小整数"
problem_url: "https://leetcode.cn/problems/find-nth-smallest-integer-with-k-one-bits/"
difficulty: "Hard"
rating: 2069
created: "2026-01-26T23:12:03+08:00"
updated: "2026-01-26T23:12:07+08:00"
upvotes: 0
comments: 2
---

# 3821. 二进制中恰好K个1的第N小整数

> **[yiduobo的每日leetcode 3821.二进制中恰好K个1的第N小整数](https://zhuanlan.zhihu.com/p/1998881518173569613) · 知乎 · 2026-01-26 · 赞同 0**
> 力扣：[3821. 二进制中恰好K个1的第N小整数](https://leetcode.cn/problems/find-nth-smallest-integer-with-k-one-bits/) · Hard · 灵茶山艾府：[试填法 + 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3821.二进制中恰好K个1的第N小整数

<https://leetcode.cn/problems/find-nth-smallest-integer-with-k-one-bits/>

题目给出两个整数n和k，n的取值范围在1到2^50之间，k在1到50之间。

现在要求找出二进制表示中恰好包含k个1的第n小的正整数。题目保证答案小于2^50。

首先，越长的二进制数就越大，题目需要找出恰好是第n小的数，因此在这里可以先想办法确定答案的长度。

由于这个数中必须包含恰好k个1，因此其长度至少为k。当长度为k时，仅有一种合法的数，就是k个1。

接下来，当长度为k + 1时，有k个1和1个0。由于最高位上必须为1，在这里就相当于剩下的k个数位中，有k - 1个1，以及1个0，也就是说，一共有C(k, 1)种合法的数。

接下来，当长度为k + 2时，相当于剩下的k + 1个数位中，有k - 1个1，以及2个0，也就是说，一共有C(k + 1, 2)种合法的数。

更进一步的，当长度为length时，相当于剩下的length - 1个数位中，有k - 1个1，length - k个0，一共有C(length - 1, length - k)种合法的数。

注意到题目保证了答案不超过2^50，那么在这里就可以从k开始向上枚举答案的长度length。对于当前的length，先计算其中0的数目zero \= length - k，然后利用C(length - 1, zero)计算当前length可以构造出来的合法二进制数的数量comb。另一方面，使用一个变量tot记录所有长度小于等于length的合法二进制数数目。若tot + comb大于等于n，说明答案的长度就是当前的length，否则将comb累加到tot中然后继续考察下一个length。

按照以上的方法找出答案的长度length后，可以先将n减去tot，此时问题就转化成了对于所有长度为length，且其中恰好包含k个1的二进制数，其中第n小的数是多少。

对于这个问题，则可以从高位开始逐位进行填充。由于最高位必然为1，在这里就可以从第length - 2位开始向下填充，对于当前填充的第index位：

1、若此时剩余0的数目zero为0，那么这一位显然只能填充1

2、若此时zero > 0，但是C(index，zero - 1)小于n，那么这一位也应该填充1。

这里的理由是如果这一位填充的是0，那么对于剩下的第0到第index - 1位这一共index位，其中有zero - 1个0，因此一共有C(index, zero - 1)种填充方案，也就是说对于最后这index + 1位，以0开头的有C(index, zero - 1)个数。现在需要计算的是第n小的，若n大于这个数，就说明答案的这一位只能为1，除此之外，还需要将n减去C(index, zero - 1)，表示最后这index + 1位中的第n小，就相当于第index填充1，然后最后index位中的第n - C(index, zero - 1)小。

3、若以上两点都不满足，则说明这一位应该填充0，此时不需要修改n，但是需要将zero减去1，表示剩下的0的数目少了一个。

最后附上python代码：

```python
class Solution(object):
    def nthSmallest(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        tot = 0
        for length in range(k, 51):
            zero = length - k
            if zero == 0:
                comb = 1
            else:
                comb = comb * (length - 1) // zero

            if tot + comb >= n:
                break
            tot += comb

        c = [[-1] * length for _ in range(length)]
        c[0][0] = 1
        for m in range(1, length):
            c[m][0] = 1
            c[m][m] = 1
            for t in range(1, m):
                c[m][t] = c[m - 1][t] + c[m - 1][t - 1]

        n -= tot
        res = 1 << (length - 1)
        for index in range(length - 2, -1, -1):
            if zero == 0 or c[index][zero - 1] < n:
                res |= 1 << index
                if zero > 0:
                    n -= c[index][zero - 1]
            else:
                zero -= 1
        
        return res
```
