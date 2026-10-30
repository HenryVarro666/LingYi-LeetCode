---
title: "1405. 最长快乐字符串"
aliases: ["yiduobo的每日leetcode 1405.最长快乐字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/405567672"
zhihu_id: "405567672"
zhihu_title: "yiduobo的每日leetcode 1405.最长快乐字符串"
question_id: "1405"
question: "最长快乐字符串"
problem_url: "https://leetcode.cn/problems/longest-happy-string/"
created: "2021-08-31T23:27:57+08:00"
updated: "2021-08-31T23:27:57+08:00"
upvotes: 0
comments: 0
---

# 1405. 最长快乐字符串

> **[yiduobo的每日leetcode 1405.最长快乐字符串](https://zhuanlan.zhihu.com/p/405567672) · 知乎 · 2021-08-31 · 赞同 0**
> 力扣：[1405. 最长快乐字符串](https://leetcode.cn/problems/longest-happy-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1405.最长快乐字符串

[力扣](https://leetcode-cn.com/problems/longest-happy-string/)

题目要求不能出现连续三个相同的字符，为了使得答案尽可能地长，那么一个自然的想法就是每次都使用两个当前余下最多的那种字符f，然后选择次多的字符s作为间隔。当出现f与s出现的次数一致时，这里的间隔使用两个s，否则使用一个s。

这样一来，就可以尽快拉平各种字符出现的次数。当然，这样的做法是没有考虑到出现次数最少的字符t的，不过极限情况下也就是f、s、t出现次数都一样，那么按上面的做法处理完后得到的字符串末尾为ffss，而此时的t相比f和s都多两个，因此也可以通过上面的做法消化掉多出来的t。

不断重复这个过程，直到用完所有字符，或者当前只剩下一种字符为止。

最后附上python代码：

```python
class Solution(object):
    def longestDiverseString(self, a, b, c):
        """
        :type a: int
        :type b: int
        :type c: int
        :rtype: str
        """

        res = []
        heap = []
        if a > 0:
            heapq.heappush(heap, [-a, 'a'])
        if b > 0:
            heapq.heappush(heap, [-b, 'b'])
        if c > 0:
            heapq.heappush(heap, [-c, 'c'])
        while heap:
            if len(heap) == 1:
                cnt, char = heap[0]
                res.append(char)
                if cnt <= -2:
                    res.append(char)
                
                break
            
            else:
                cnt1, char1 = heapq.heappop(heap)
                cnt2, char2 = heapq.heappop(heap)
                if cnt1 == cnt2:
                    res.append(char1)
                    res.append(char2)
                    if cnt1 <= -2:
                        res.append(char1)
                        res.append(char2)
                        cnt1 += 1
                        cnt2 += 1
                    cnt1 += 1
                    cnt2 += 1
                else:
                    res.append(char1)
                    if cnt1 <= -2:
                        res.append(char1)
                        cnt1 += 1
                    cnt1 += 1
                    res.append(char2)
                    cnt2 += 1
        
                if cnt1 < 0:
                    heapq.heappush(heap, [cnt1, char1])
                if cnt2 < 0:
                    heapq.heappush(heap, [cnt2, char2])
            

        return ''.join(res)
```
