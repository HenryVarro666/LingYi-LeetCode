---
title: "2452. 距离字典两次编辑以内的单词"
aliases: ["yiduobo的每日leetcode 2452.距离字典两次编辑以内的单词"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/585538178"
zhihu_id: "585538178"
zhihu_title: "yiduobo的每日leetcode 2452.距离字典两次编辑以内的单词"
question_id: "2452"
question: "距离字典两次编辑以内的单词"
problem_url: "https://leetcode.cn/problems/words-within-two-edits-of-dictionary/"
difficulty: "Medium"
created: "2022-11-22T01:52:40+08:00"
updated: "2022-11-22T01:52:40+08:00"
upvotes: 0
comments: 0
---

# 2452. 距离字典两次编辑以内的单词

> **[yiduobo的每日leetcode 2452.距离字典两次编辑以内的单词](https://zhuanlan.zhihu.com/p/585538178) · 知乎 · 2022-11-22 · 赞同 0**
> 力扣：[2452. 距离字典两次编辑以内的单词](https://leetcode.cn/problems/words-within-two-edits-of-dictionary/) · Medium · 灵茶山艾府：[暴力（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2452.距离字典两次编辑以内的单词

[力扣](https://leetcode.cn/problems/words-within-two-edits-of-dictionary/description/)

没想到什么特别好的做法，不过本题的数据规模较小，直接暴力枚举然后比较是完全可行的。两两枚举queries和dictionary中的单词对，统计其中不同字母的数目。若不超过两个，那么这个query对应的答案就是true，否则就是false。

```python
class Solution(object):
    def twoEditWords(self, queries, dictionary):
        """
        :type queries: List[str]
        :type dictionary: List[str]
        :rtype: List[str]
        """

        res = []
        for query in queries:
            flag = False
            for word in dictionary:
                cnt = 0
                for index in range(len(query)):
                    if query[index] != word[index]:
                        cnt += 1
                    if cnt > 2:
                        break
                
                if cnt <= 2:
                    flag = True
                    break
            
            if flag:
                res.append(query)
        
        return res
```
