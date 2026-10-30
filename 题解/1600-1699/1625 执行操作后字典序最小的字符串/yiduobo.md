---
title: "1625. 执行操作后字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 1625.执行操作后字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/字符串", "题单/数学算法/一-数论", "题单/字符串/五-最小表示法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/436928457"
zhihu_id: "436928457"
zhihu_title: "yiduobo的每日leetcode 1625.执行操作后字典序最小的字符串"
question_id: "1625"
question: "执行操作后字典序最小的字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-applying-operations/"
difficulty: "Medium"
rating: 1992
created: "2021-11-24T00:03:19+08:00"
updated: "2021-11-24T00:03:19+08:00"
upvotes: 0
comments: 0
---

# 1625. 执行操作后字典序最小的字符串

> **[yiduobo的每日leetcode 1625.执行操作后字典序最小的字符串](https://zhuanlan.zhihu.com/p/436928457) · 知乎 · 2021-11-24 · 赞同 0**
> 力扣：[1625. 执行操作后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-applying-operations/) · Medium · 灵茶山艾府：[枚举轮转到最左边的下标 + 裴蜀定理（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1625.执行操作后字典序最小的字符串

[力扣](https://leetcode-cn.com/problems/lexicographically-smallest-string-after-applying-operations/)

首先分析一下这两种操作，首先是加操作。

对于加操作而言，由于题目只能对奇数位上的数进行操作，又因为原始字符串的长度为偶数，那么首先可以得出一个结论是，当b为奇数时，经过一次轮转之后，在原始字符串中各个位置的奇偶性就互换了，也就是说在原始字符串中位于奇数位和偶数位上的数都可能被操作；反过来，当b为偶数时，无论怎么操作，在原始字符串中各个位置的奇偶性都不会产生变化，因此只有在原始字符串中处于奇数位上的数可能被操作。

又因为每次操作是对所有奇数位上的数同时执行，因此为了使得字典序最小，实际上只需要考虑让最高位上的数最小即可。

综合这两点可以得出结论，对某个字符串而言，当b为奇数时，需要分别操作将当前字符串的偶数位和奇数位，使得第0位和第1位变得最小，反过来当b为偶数时，则只需要操作当前字符串的奇数位，将第1位变得最小。

接下来分析轮转操作。

设字符串长度为n，执行完x次轮转操作之后字符串变回原始字符串，那么就有

n \* y \= b \* x

这里的x是满足等式的最小正整数。在这里可以求出n和b的最大公约数，然后x的值就等于n除以这个最大公约数。换言之，在极限情况下，最多n轮轮转之后字符串也会变为原始字符串。由于这里n的规模并不大，因此完全可以直接枚举每一种轮转的情况，然后对当前情况执行加操作得到这种情况下的最小字符串，其中字典序最小的就是最终答案了。

除此之外，在已经得知a的情况下，可以先将每个数字执行加操作变得最小的操作轮次提前预处理出来供轮转时执行加操作使用。

最后附上python代码：

```python
class Solution(object):
    def findLexSmallestString(self, s, a, b):
        """
        :type s: str
        :type a: int
        :type b: int
        :rtype: str
        """

        rnd = [0] * 10
        for num in range(10):
            now = num
            min_num = num
            min_rnd = 0
            now_rnd = 0
            while True:
                now = (now + a) % 10
                if now == num:
                    break
                now_rnd += 1
                if now < min_num:
                    min_num = now
                    min_rnd = now_rnd
            
            rnd[num] = min_rnd
        
        offset = 0
        now_list = [int(x) for x in list(s)]
        res = now_list[:]
        n = len(s)
        while True:
            tmp = now_list[:]
            if b & 1:
                self.adjust(tmp, 0, n, a, rnd)
            self.adjust(tmp, 1, n, a, rnd)

            flag = False
            for index in range(n):
                if tmp[index] != res[index]:
                    flag = tmp[index] < res[index]
                    break

            if flag:
                res = tmp[:]
            
            offset = (offset + b) % n
            if offset == 0:
                break
            
            tmp = [0] * n
            for index in range(n):
                tmp[(index + b) % n] = now_list[index]
            now_list = tmp[:]
        
        return ''.join(str(x) for x in res)
    
    def adjust(self, tmp, start_pos, n, a, rnd):
        add_rnd = rnd[tmp[start_pos]]
        for index in range(start_pos, n, 2):
            tmp[index] = (tmp[index] + a * add_rnd) % 10
```
