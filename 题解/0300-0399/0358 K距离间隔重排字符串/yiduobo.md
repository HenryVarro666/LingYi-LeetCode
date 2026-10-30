---
title: "358. K距离间隔重排字符串"
aliases: ["yiduobo的每日leetcode 358.K距离间隔重排字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597514996"
zhihu_id: "597514996"
zhihu_title: "yiduobo的每日leetcode 358.K距离间隔重排字符串"
question_id: "358"
question: "K距离间隔重排字符串"
problem_url: "https://leetcode.cn/problems/rearrange-string-k-distance-apart/"
created: "2023-01-08T18:29:39+08:00"
updated: "2023-01-08T18:29:39+08:00"
upvotes: 0
comments: 0
---

# 358. K距离间隔重排字符串

> **[yiduobo的每日leetcode 358.K距离间隔重排字符串](https://zhuanlan.zhihu.com/p/597514996) · 知乎 · 2023-01-08 · 赞同 0**
> 力扣：[358. K距离间隔重排字符串](https://leetcode.cn/problems/rearrange-string-k-distance-apart/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

358.K距离间隔重排字符串

[力扣](https://leetcode.cn/problems/rearrange-string-k-distance-apart/)

印象中之前应该遇到过一个类似的问题，具体的题号不太记得了，但是做法还是类似的，可以使用贪心法。

利用哈希表统计每种字符出现的次数，然后从头开始遍历答案字符串中的所有位置。对于每个位置都应该填充当前剩余数量最多，且上一次出现位置在k个字符之前的字符。为了高效取出剩余次数最多的字符，可以使用一个堆来维护当前每种字符串剩余的次数。另外还需要使用一个哈希表来记录每种字符上一次使用的下标位置，用来判断间隔为k这个限制。

最后附上python代码：

```python
class Solution(object):
    def rearrangeString(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        cnt_dict = {}
        for char in s:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        heap = []
        for char, cnt in cnt_dict.items():
            heapq.heappush(heap, [-cnt, char])

        res = []
        last_pos = {}
        for index in range(len(s)):
            tmp = []
            while heap and (heap[0][1] in last_pos and index - last_pos[heap[0][1]] < k):
                tmp.append(heapq.heappop(heap))
            
            if not heap:
                return ""

            cnt, char = heapq.heappop(heap)
            res.append(char)
            last_pos[char] = index
            if cnt + 1 != 0:
                heapq.heappush(heap, [cnt + 1, char])
            

            for cnt, char in tmp:
                heapq.heappush(heap, [cnt, char])

        return "".join(res)
```
