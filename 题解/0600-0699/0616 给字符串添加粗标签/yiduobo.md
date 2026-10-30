---
title: "616. 给字符串添加粗标签"
aliases: ["yiduobo的每日leetcode 616.给字符串添加粗标签"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602097003"
zhihu_id: "602097003"
zhihu_title: "yiduobo的每日leetcode 616.给字符串添加粗标签"
question_id: "616"
question: "给字符串添加粗标签"
problem_url: "https://leetcode.cn/problems/add-bold-tag-in-string/"
created: "2023-01-31T00:08:07+08:00"
updated: "2023-01-31T00:08:07+08:00"
upvotes: 0
comments: 0
---

# 616. 给字符串添加粗标签

> **[yiduobo的每日leetcode 616.给字符串添加粗标签](https://zhuanlan.zhihu.com/p/602097003) · 知乎 · 2023-01-31 · 赞同 0**
> 力扣：[616. 给字符串添加粗标签](https://leetcode.cn/problems/add-bold-tag-in-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

616.给字符串添加粗标签

[力扣](https://leetcode.cn/problems/add-bold-tag-in-string/)

题目要求找出s中所有出现在words中的子串，并在这些子串形成的连续区间两侧加上加粗符号。

注意到题目的数据规模并不大，因此使用暴力法也是可行的。

直接遍历words中的所有单词，使用字符串的find函数找出其出现的所有位置，并将对应的区间记录下来。遍历完成后，就得到了所有需要加粗的区间。接下来，将这些区间按起点从小到大排序后进行合并，在合并过程中将确定下来的区间所对应的字符串，配上加粗符号之后加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def addBoldTag(self, s, words):
        """
        :type s: str
        :type words: List[str]
        :rtype: str
        """

        n = len(s)
        intervals = []

        for word in words:
            start_pos = 0
            while True:
                p = s.find(word, start_pos)
                if p == -1:
                    break
                
                intervals.append([p, p + len(word) - 1])
                start_pos = p + 1
        
        if not intervals:
            return s

        intervals.sort(key = lambda d:d[0])
        lastx, lasty = intervals[0]
        res = []
        p = 0
        for x, y in intervals[1:]:
            if x <= lasty + 1:
                lasty = max(y, lasty)
            else:
                res.append(s[p : lastx])
                res.append('<b>')
                res.append(s[lastx : lasty + 1])
                res.append('</b>')
                p = lasty + 1
                lastx, lasty = x, y

        res.append(s[p : lastx])
        res.append('<b>')
        res.append(s[lastx : lasty + 1])
        res.append('</b>')
        res.append(s[lasty + 1:])
        return ''.join(res)
```
