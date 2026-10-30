---
title: "992. K个不同整数的子数组"
aliases: ["yiduobo的每日leetcode 992.K个不同整数的子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/364928283"
zhihu_id: "364928283"
zhihu_title: "yiduobo的每日leetcode 992.K个不同整数的子数组"
question_id: "992"
question: "K个不同整数的子数组"
problem_url: "https://leetcode.cn/problems/subarrays-with-k-different-integers/"
created: "2021-04-14T23:24:32+08:00"
updated: "2021-04-14T23:24:32+08:00"
upvotes: 0
comments: 0
---

# 992. K个不同整数的子数组

> **[yiduobo的每日leetcode 992.K个不同整数的子数组](https://zhuanlan.zhihu.com/p/364928283) · 知乎 · 2021-04-14 · 赞同 0**
> 力扣：[992. K个不同整数的子数组](https://leetcode.cn/problems/subarrays-with-k-different-integers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

992.K个不同整数的子数组

[力扣](https://leetcode-cn.com/problems/subarrays-with-k-different-integers/)

经典的滑动窗口问题。对于一个固定的左边界start_pos而言，我们定义最小右边界l以及最大右边界r。l表示从start_pos开始的所有具有K个不同证书的子数组中，右边界的最小值；r则表示右边界的最大值。那么从start_pos开始的有K个不同整数的子数组一共有r - l + 1个。

在给定start_pos的情况下，l和r也很容求得。具体做法为l先从start_pos开始向后扫描，直到某一时刻start_pos到l中有K个不同整数时停下。接下来r从l开始向后扫描，直到A[r + 1]未出现在start_pos到r之间时停下。统计不同整数个数则可以使用一个cnt_dict，其key为数组中的整数，value为整数出现的次数。那么当len(cnt_dict)等于K时，说明子数组中已经有K个不同整数了。

接下来，我们需要尝试将start_pos向右移动，当start_pos向后移动变为start_pos’ \= start_pos + 1时，子数组减少了一个A[start_pos]，我们就可以根据cnt_dict判断l和r应当如何调整：

1、当cnt_dict\[A\[start_pos\]\]等于1时，将start_pos向后移动变为start_pos’之后，以start_pos'开头，r结尾的子数组中由于已经没有了A\[start_pos\]，就只剩下只有K - 1个不同整数了。恰好此时的A\[r + 1\]是没有出现在start_pos到r之间的，因此只需将A\[r + 1\]加入进来，就得到了以start_pos’开头的最短的合法子数组，因此此时应该更新l为r + 1。接下来，还需要让r从r + 1开始向后扫描，直到A\[r + 1\]未出现在start_pos’到r之间时停下。

2、当cnt_dict\[A\[start_pos\]\]大于1时，将start_pos向后移动变为start_pos’之后，以start_pos'开头，r结尾的子数组中还有了A\[start_pos\]，因此依然有K个不同的整数，此时的r不需要变动，但还需要调整l的位置。A\[start_pos\]在start_pos之后下一次出现的位置next_pos显然是小于等于r的，那么若这个位置小于等于l，那么l也不需要变动，否则就应当将l移动到next_pos，这样以start_pos’开头的子数组中才会有A\[start_pos\]。

对于这里的next_pos，也可以先通过一趟扫描预处理出来提高运算效率。

由于start_pos、l、r都只会遍历A一次，因此实际上这是个O(n)的做法。

最后附上python代码：

```python
class Solution(object):
    def subarraysWithKDistinct(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        n = len(A)
        last_pos = {A[-1] : n - 1}
        next_pos = [-1] * n
        for index in range(n - 1, -1, -1):
            if A[index] in last_pos:
                next_pos[index] = last_pos[A[index]]
            last_pos[A[index]] = index
        
        start_pos = 0
        l = -1
        n = len(A)
        cnt_dict = {}
        while l + 1 < n and len(cnt_dict) < K:
            cnt_dict[A[l + 1]] = cnt_dict.get(A[l + 1], 0) + 1
            l += 1
        
        if len(cnt_dict) < K:
            return 0

        r = l
        while r + 1 < n and A[r + 1] in cnt_dict:
            cnt_dict[A[r + 1]] += 1
            r += 1
        
        res = r - l + 1

        while start_pos + 1 < n:
            if cnt_dict[A[start_pos]] > 1:
                cnt_dict[A[start_pos]] -= 1
                l = max(l, next_pos[start_pos])
            else:
                cnt_dict.pop(A[start_pos])
                l = r + 1
                if l == n:
                    break
                cnt_dict[A[l]] = cnt_dict.get(A[l], 0) + 1
                r = l
                while r + 1 < n and A[r + 1] in cnt_dict:
                    cnt_dict[A[r + 1]] += 1
                    r += 1
            
            res += r - l + 1
            start_pos += 1
        
        return res
```
