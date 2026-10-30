---
title: "3747. 统计移除零后不同整数的数目"
aliases: ["yiduobo的每日leetcode 3747.统计移除零后不同整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/brainteaser", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1973429668288929861"
zhihu_id: "1973429668288929861"
zhihu_title: "yiduobo的每日leetcode 3747.统计移除零后不同整数的数目"
question_id: "3747"
question: "统计移除零后不同整数的数目"
problem_url: "https://leetcode.cn/problems/count-distinct-integers-after-removing-zeros/"
difficulty: "Medium"
rating: 1848
created: "2025-11-17T20:03:17+08:00"
updated: "2025-11-17T20:03:21+08:00"
upvotes: 2
comments: 0
---

# 3747. 统计移除零后不同整数的数目

> **[yiduobo的每日leetcode 3747.统计移除零后不同整数的数目](https://zhuanlan.zhihu.com/p/1973429668288929861) · 知乎 · 2025-11-17 · 赞同 2**
> 力扣：[3747. 统计移除零后不同整数的数目](https://leetcode.cn/problems/count-distinct-integers-after-removing-zeros/) · Medium · 灵茶山艾府：[统计不含 0 的整数个数，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3747.统计移除零后不同整数的数目

[3747. 统计移除零后不同整数的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-distinct-integers-after-removing-zeros/description/)

题目给出一个正整数n，其取值范围可达10^15。

对于1到n之间的每个整数x，记下通过移除x的十进制表示中所有的零之后得到的整数。问这些整数中不同整数的数量有多少个。

由于n的规模较大，不能直接使用暴力算法计算，需要另想办法。

不妨设这个n的位数为m，那么最终答案就可以分为两个部分，分别为：

1、长度在1到m - 1之间的，仅由1到9组成的数的个数

2、长度为m，仅由1到9组成，且大小不超过n的数的个数

其中第一个部分是比较好计算的。长度为k时，每位上可用的元素都是1到9，因此一共有9^k个合法的k位数，那么长度为1到m - 1之间仅由1到9组成的数一共就有9 + 9^2 + 9^3 + ... + 9^(m - 1)个。

对于第二个部分，则需要逐位进行拆解。

不妨设这个n从高位到低位分别为a[0]、a[1]、a[2]、...、a[m - 1]，那么就可以从高位向低位进行逐位填充：

当最高位取1到a[0] - 1时，后续数位可以任意取1到9之间的数，因此一共有(a[0] - 1) \* 9^(m - 1)种合法的数

当最高位取a[0]，且次高位取1到a[1] - 1时，一共有(a[1] - 1) \* 9^(m - 2)种可行的方案

当最高位取a[0]、次高位取a[1]、第三高位取1到a[2] - 1时，有(a[2] - 1) \* 9^(m - 3)种可行的方案

...

当除了最低位之外的位分别取a[0]、a[1]、a[2]、...、a[m - 2]，最低位取1到a[m - 1] - 1时，有(a[m - 1] - 1) \* 9^0种可行的方案

不过需要注意的是，以上的算法有两个遗漏的地方，需要进行修正。

首先是n的数位，也就是a[0]到a[m - 1]中可能包含有0。不妨设其中最高位的0对应的位为a[k]，那么不仅(a[k] - 1) \* 9^(m - k - 1)这个式子不成立，从a[k + 1]到a[m - 1]的所有式子都不应该被计入答案，因为这些式子都是基于这一位上的取值为a[k]时计算的，当a[k]取0时就已经不合法了。

另外，对于n自身，如果其中不包含0，那么n也应该被计入答案，但是以上的计算方法没有考虑到所有高位取a[0]到a[m - 2]，且最低位取a[m - 1]的情况。也就是说，当n中不包含0时，答案需要额外加上1。

到了这里，就得到了完整的算法。

从低位开始，通过模10除以10逐位分离n的所有数位，同时使用两个变量full和p9分别记录第二部分合法的数的个数以及9的幂。

对于当前的数位d，若d > 0，则将(d - 1) \* p9累加到full中；反之若d为0，则说明遇到了值为0的数位，之前低位上计算得到的full是无效的，此时应该将full置为0，同时标记n中有0。

接下来，将n除以10，同时将p9乘以9。若此时的n非0，则还需要将p9累加到答案中，对应的是第一部分中数的个数。

重复以上过程，直到n为0为止。除此之外，还需要通过标记判断n中是否有0，若没有，则还需将full加上1。

最后，将full累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def countDistinct(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        p9 = 1
        res = 0
        full = 0
        zero = False
        while n:
            d = n % 10
            if d > 0:
                full += (d - 1) * p9
            else:
                full = 0
                zero = True

            p9 *= 9
            n //= 10
            if n > 0:
                res += p9
        
        if not zero:
            full += 1
        return res + full
```
