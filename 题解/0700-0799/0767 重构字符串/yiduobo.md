---
title: "767. 重构字符串"
aliases: ["yiduobo的每日leetcode 767.重构字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/sorting", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339369472"
zhihu_id: "339369472"
zhihu_title: "yiduobo的每日leetcode 767.重构字符串"
question_id: "767"
question: "重构字符串"
problem_url: "https://leetcode.cn/problems/reorganize-string/"
difficulty: "Medium"
rating: 1681
created: "2020-12-24T22:51:55+08:00"
updated: "2020-12-24T22:51:55+08:00"
upvotes: 0
comments: 0
---

# 767. 重构字符串

> **[yiduobo的每日leetcode 767.重构字符串](https://zhuanlan.zhihu.com/p/339369472) · 知乎 · 2020-12-24 · 赞同 0**
> 力扣：[767. 重构字符串](https://leetcode.cn/problems/reorganize-string/) · Medium · 灵茶山艾府：[结论+构造，排序/不排序两种写法，附相似题目（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

767.重构字符串

[力扣](https://leetcode-cn.com/problems/reorganize-string/)

首先可以明确的是，若某个字符出现的次数超过所有字符数量的一半，那么就肯定构造不出来。这里的一半对于字符数量为奇数的情况应该向上取整。

接下里，应该是存在某种构造的解法的，但我这里使用的是比较暴力的做法。使用一个堆来维护当前每个字符出现的个数。每一轮，从堆中选取出现最多以及第二多的两个字符，将其加入到答案中，然后将这两字符的数量分别减一再重新加入到堆中。

这样做的一个原理是设第k轮中出现最多的两个字母分别出现了a次和b次，此时有a >\= b，那么在第k + 1轮中，就依然有a - 1 >\= b - 1，那么如果在构造堆时选择使用字母序作为第二排序条件，那么第k + 1轮中出现a - 1次的字母顺位依然比出现b - 1次的要高，保证了第k轮出现次数第二多的数与第k + 1轮出现次数最多的数不同，从而达成题目的要求。

最后附上python代码：

```python
import heapq

class Solution(object):
    def reorganizeString(self, S):
        """
        :type S: str
        :rtype: str
        """

        count_dict = {}
        for char in S:
            count_dict[char] = count_dict.get(char, 0) + 1
        
        if max(count_dict.values()) > (len(S) + 1) / 2:
            return ''

        heap = []
        for key, value in count_dict.items():
            heapq.heappush(heap, (-value, key))
        
        res = []
        while heap:
            cnt1, char1 = heapq.heappop(heap)
            cnt1 += 1
            res.append(char1)

            if heap:
                cnt2, char2 = heapq.heappop(heap)
                cnt2 += 1
                res.append(char2)
            
            if cnt1:
                heapq.heappush(heap, (cnt1, char1))
                if cnt2:
                    heapq.heappush(heap, (cnt2, char2))
            
        return ''.join(res)
```
