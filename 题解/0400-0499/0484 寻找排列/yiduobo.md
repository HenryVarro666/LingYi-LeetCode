---
title: "484. 寻找排列"
aliases: ["yiduobo的每日leetcode 484.寻找排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600154236"
zhihu_id: "600154236"
zhihu_title: "yiduobo的每日leetcode 484.寻找排列"
question_id: "484"
question: "寻找排列"
problem_url: "https://leetcode.cn/problems/find-permutation/"
created: "2023-01-19T23:59:49+08:00"
updated: "2023-01-19T23:59:49+08:00"
upvotes: 0
comments: 0
---

# 484. 寻找排列

> **[yiduobo的每日leetcode 484.寻找排列](https://zhuanlan.zhihu.com/p/600154236) · 知乎 · 2023-01-19 · 赞同 0**
> 力扣：[484. 寻找排列](https://leetcode.cn/problems/find-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

484.寻找排列

[力扣](https://leetcode.cn/problems/find-permutation/)

题目要求最后构造出来的排列字典序最小，那么就应该优先使用还未使用的最小的正整数来填充这个排列，不过需要注意的是，由于D的存在，在某些情况下需要预留出一些缓冲空间，例如样例2中，由于第一个D的存在，因此排列只能以2开头而不是1。更一般的，不妨设下一个填充的数字为now，若接下来连续出现了cnt个D，那么就需要从now + cnt开始逆序填充到now。而对于I，则只需要按照正常顺序填充就行了。

到了这里就得到了一种算法。轮流寻找连续的D和I，对于D，设存在cnt个连续的D，那么就将now + cnt到now逆序填充到答案中。而对于I，先跳过第一个I，然后对于后续的I，不断将当前的now填充到答案中，并将now加上1。在这里跳过第一个I的原因是这种做法相当于将D和I的序列切分开了，因此当I后方紧接着D这种情况出现时，最后一个I需要填充的数值实际上会通过后续的D来填充，因此在这里不需要考虑最后一个I。方便起见，在这里就改成了不考虑第一个I。

需要特别注意的是，若s是以I结尾的，那么这里就不能省略最后一个I，因此当I结尾时，还需要将now填充到答案的末尾。

最后附上python代码：

```python
class Solution(object):
    def findPermutation(self, s):
        """
        :type s: str
        :rtype: List[int]
        """

        res = []
        now = 1
        p = 0
        n = len(s)
        while p < n:
            cnt = 0
            while p < n and s[p] == 'D':
                cnt += 1
                p += 1
            
            res.extend(range(now + cnt, now - 1, -1))
            now += cnt + 1
            p += 1

            while p < n and s[p] == 'I':
                res.append(now)
                now += 1
                p += 1
        
        if s[-1] == 'I':
            res.append(now)
        return res
```
