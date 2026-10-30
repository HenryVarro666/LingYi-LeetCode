---
title: "1768. 交替合并字符串"
aliases: ["yiduobo的每日leetcode 1768.交替合并字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460804457"
zhihu_id: "460804457"
zhihu_title: "yiduobo的每日leetcode 1768.交替合并字符串"
question_id: "1768"
question: "交替合并字符串"
problem_url: "https://leetcode.cn/problems/merge-strings-alternately/"
difficulty: "Easy"
created: "2022-01-22T22:34:45+08:00"
updated: "2022-01-22T22:34:46+08:00"
upvotes: 0
comments: 0
---

# 1768. 交替合并字符串

> **[yiduobo的每日leetcode 1768.交替合并字符串](https://zhuanlan.zhihu.com/p/460804457) · 知乎 · 2022-01-22 · 赞同 0**
> 力扣：[1768. 交替合并字符串](https://leetcode.cn/problems/merge-strings-alternately/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1768.交替合并字符串

[力扣](https://leetcode-cn.com/problems/merge-strings-alternately/)

比较基础的题目，使用两个指针分别从两个字符串的头部开始向后扫，按照先1后2的顺序进行合并。当某一个指针当前字符串末尾时则停止，然后将合并的结果与剩下的另一个字符串组合后返回即可。

最后附上python代码：

```python
class Solution(object):
    def mergeAlternately(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """

        p1 = p2 = 0
        l1 = len(word1)
        l2 = len(word2)
        res = []
        while p1 < l1 and p2 < l2:
            res.append(word1[p1])
            res.append(word2[p2])
            p1 += 1
            p2 += 1
        
        if p1 < l1:
            return ''.join(res) + word1[p1:]
        else:
            return ''.join(res) + word2[p2:]
```
