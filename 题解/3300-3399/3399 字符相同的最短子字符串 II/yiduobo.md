---
title: "3398. 字符相同的最短子字符串I & 3399. 字符相同的最短子字符串II"
aliases: ["yiduobo的每日leetcode 3398.字符相同的最短子字符串I && 3399.字符相同的最短子字符串II", "3398. 字符相同的最短子字符串I", "3399. 字符相同的最短子字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "leetcode/heap-priority-queue", "leetcode/array", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30864730359"
zhihu_id: "30864730359"
zhihu_title: "yiduobo的每日leetcode 3398.字符相同的最短子字符串I && 3399.字符相同的最短子字符串II"
question_id: ["3398", "3399"]
question: ["字符相同的最短子字符串 I", "字符相同的最短子字符串 II"]
problem_url: ["https://leetcode.cn/problems/smallest-substring-with-identical-characters-i/", "https://leetcode.cn/problems/smallest-substring-with-identical-characters-ii/"]
difficulty: "Hard"
rating: 2376
created: "2025-03-17T23:59:23+08:00"
updated: "2025-03-17T23:59:23+08:00"
upvotes: 1
comments: 0
---

# 3398. 字符相同的最短子字符串I & 3399. 字符相同的最短子字符串II

> **[yiduobo的每日leetcode 3398.字符相同的最短子字符串I && 3399.字符相同的最短子字符串II](https://zhuanlan.zhihu.com/p/30864730359) · 知乎 · 2025-03-17 · 赞同 1**
> 力扣：[3398. 字符相同的最短子字符串 I](https://leetcode.cn/problems/smallest-substring-with-identical-characters-i/) · Hard · 灵茶山艾府：[两种非暴力做法：二分答案/最大堆（Python/Java/C++/Go）](../3398%20字符相同的最短子字符串%20I/灵茶山艾府.md)
> 力扣：[3399. 字符相同的最短子字符串 II](https://leetcode.cn/problems/smallest-substring-with-identical-characters-ii/) · Hard · 灵茶山艾府：[两种方法：二分答案/最大堆+分桶优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3398.字符相同的最短子字符串I

[3398. 字符相同的最短子字符串 I - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-substring-with-identical-characters-i/description/)

3399.字符相同的最短子字符串II

[3399. 字符相同的最短子字符串 II - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-substring-with-identical-characters-ii/description/)

题目给出一个长度为n的二进制字符串s，以及一个整数numOps。现在可以对s执行操作，每次操作可以从s中任选一个下标i，将对应的s[i]翻转，即如果s[i]为'1'，那么就将其置为0，反之亦然。

问如果最多可以执行numOps次操作，那么s中最长的相同子字符串的最小长度是多少。相同子字符串指的是子串中的所有字符都一样。

两题的题设一样，第二题的数据规模较大，s的长度可达10^6。

对于这类最大化某个最小值，或者最小化某个最大值的问题，一种常见的处理方法是二分答案，然后检测当前的二分值能否达成。对于本题，可以二分答案mid，接下来的问题就是检测能否在numOps操作内将nums中最长的相同子串的长度小于等于mid。

不妨设现在有一段长度为length的相同子串，那么在这里就需要按照mid + 1一组将这个子串切分成若干组，这个mid + 1的含义是包含mid个相同字符，然后紧接着1个翻转后的字符。这样一来，经过length // (mid + 1)次操作就可以保证相同子串的长度都不超过mid。

这样一来，就可以使用两个指针p和q互相迭代，分离出原始s中所有的相同子串，然后对于每个子串，根据其长度length计算需要翻转多少个字符，然后根据需要翻转的字符的总数与numOps的大小关系来修正二分的边界。

另外需要特别注意的是，上面的划分的方法有一个缺陷：对于length刚是mid倍数的子串，最后这一组的mid + 1个字符不能按照上面的mid个相同字符再紧接着1个翻转后的字符这样处理，因为最后这个翻转后的字符将与下一个字符相同。

一种可行的处理方案是将翻转后的字符放置到这mid个字符的中间，但是这样就要求mid必须大于等于2才有中间这个概念，而对于mid \= 1的情况，依然是无法处理的。

不过好在mid \= 1的情况是很方便特殊处理的。对于mid \= 1的情况，最终的s要么是'101010...'，要么是'010101...'。那么要使得s变为'101010...'，需要将所有偶数位上的0以及所有奇数位上的1进行翻转，而如果要使得s变为'010101...'，则需要将所有偶数位上的1以及所有奇数位上的0进行翻转。

于是可以在二分答案mid之前先一趟遍历，分别计算偶数下标位上1的数量与奇数下标位上0的数量之和cnt1，以及偶数下标位上0的数量与奇数下标位上1的数量之和cnt2，若二者的较小值小于等于numOps，说明可以得到一个01交替出现的s，此时答案就应该为1。若不满足，再按最开始的处理方法执行二分。

最后附上python代码：

```python
class Solution(object):
    def minLength(self, s, numOps):
        """
        :type s: str
        :type numOps: int
        :rtype: int
        """
        
        cnt1 = 0
        cnt2 = 0

        for index, char in enumerate(s):
            if index % 2 == 0:
                cnt1 += int(char)
                cnt2 += 1 - int(char)
            else:
                cnt1 += 1 - int(char)
                cnt2 += int(char)
        
        if min(cnt1, cnt2) <= numOps:
            return 1
        
        left = 2
        right = len(s)
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            p = 0
            while p < len(s):
                q = p + 1
                while q < len(s) and s[q] == s[p]:
                    q += 1
                
                length = q - p
                cnt += length // (mid + 1)
                p = q

            if cnt <= numOps:
                right = mid
            else:
                left = mid + 1
        
        return left
```
