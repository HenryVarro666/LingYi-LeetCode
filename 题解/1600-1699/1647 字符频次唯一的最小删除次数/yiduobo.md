---
title: "1647. 字符频次唯一的最小删除次数"
aliases: ["yiduobo的每日leetcode 1647.字符频次唯一的最小删除次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/440157616"
zhihu_id: "440157616"
zhihu_title: "yiduobo的每日leetcode 1647.字符频次唯一的最小删除次数"
question_id: "1647"
question: "字符频次唯一的最小删除次数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-character-frequencies-unique/"
created: "2021-12-01T22:56:45+08:00"
updated: "2021-12-01T22:56:45+08:00"
upvotes: 0
comments: 0
---

# 1647. 字符频次唯一的最小删除次数

> **[yiduobo的每日leetcode 1647.字符频次唯一的最小删除次数](https://zhuanlan.zhihu.com/p/440157616) · 知乎 · 2021-12-01 · 赞同 0**
> 力扣：[1647. 字符频次唯一的最小删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-character-frequencies-unique/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1647.字符频次唯一的最小删除次数

[力扣](https://leetcode-cn.com/problems/minimum-deletions-to-make-character-frequencies-unique/)

由于题目只支持删除操作，那么对于出现统一频次的字符而言，最好的做法就是保留一种字符不动，其他的字符出现次数全部减一。当然，这里的减一可能会出现新的同频次字符，因此需要不断重复这个过程直到处理完所有字符位置。

由于必须先处理出现频次较高的字符，那么一个自然的想法就是统计每种字符出现次数，记为cnt，然后按这个次数从大到小进行排序。接下来首先考虑的自然是cnt[0]，记当前处理的cnt为now，而这个cnt出现的次数为mul，接下来从p \= 1开始向后考虑。

若当前的now等于cnt[p]，那么说明还有其他字符也出现了now次，于是此时应该将mul加1，并将p向后移动一位。重复这个过程直到p到达数组末尾或者now不等于cnt[p]。

接下里对于此时的now有两种情况：

1、mul大于1。此时说明出现次数等于now的字符有多个，那么按照最开始的结论，应该保留一种字符不动，其他字符都需要删去一个，于是此时需要删去mul - 1种字符各一个，那么将答案加上mul - 1。同时，由于cnt后续的次数必然都小于now，因此now在这里无需再考虑，转而应该考虑由于这次删除操作变成的mul - 1中出现now - 1次的字符，因此还需要将now更新为now - 1，将mul更新为mul - 1，然后继续考虑这里新的now与cnt[p]的大小。

2、mul等于1。此时无需对出现now次的字符进行处理，因此直接将now更新为cnt[p]，然后将p加上1，继续考察now和cnt[p]的大小。

需要特别注意的是，当p到达末尾后，此时的mul还是有可能大于0的，也就是此时出现now的字符依然有mul种，那么就需要不断执行删去操作，将mul - 1种字符各删去一个。那么就应该将答案加上mul - 1，同时更新now为now - 1，mul为mul - 1。重复这个过程直到now等于0或者mul等于1为止。

最后附上python代码：

```python
class Solution(object):
    def minDeletions(self, s):
        """
        :type s: str
        :rtype: int
        """

        char_cnt = {}
        for char in s:
            char_cnt[char] = char_cnt.get(char, 0) + 1
        
        cnt_list = sorted(char_cnt.values(), reverse=True)
        res = 0
        now = cnt_list[0]
        mul = 1
        p = 1
        while p < len(cnt_list):
            while p < len(cnt_list) and now == cnt_list[p]:
                mul += 1
                p += 1
            
            if mul > 1:
                res += mul - 1
                now -= 1
                mul -= 1
            else:
                now = cnt_list[p]
                p += 1
        
        while mul > 1 and now > 0:
            res += mul - 1
            now -= 1
            mul -= 1
        
        return res
```
