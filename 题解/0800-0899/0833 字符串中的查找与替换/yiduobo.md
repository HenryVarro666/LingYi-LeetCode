---
title: "833. 字符串中的查找与替换"
aliases: ["yiduobo的每日leetcode 833.字符串中的查找与替换"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/345277254"
zhihu_id: "345277254"
zhihu_title: "yiduobo的每日leetcode 833.字符串中的查找与替换"
question_id: "833"
question: "字符串中的查找与替换"
problem_url: "https://leetcode.cn/problems/find-and-replace-in-string/"
difficulty: "Medium"
created: "2021-01-23T16:21:14+08:00"
updated: "2021-01-23T16:21:14+08:00"
upvotes: 0
comments: 0
---

# 833. 字符串中的查找与替换

> **[yiduobo的每日leetcode 833.字符串中的查找与替换](https://zhuanlan.zhihu.com/p/345277254) · 知乎 · 2021-01-23 · 赞同 0**
> 力扣：[833. 字符串中的查找与替换](https://leetcode.cn/problems/find-and-replace-in-string/) · Medium · 灵茶山艾府：[线性做法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

833.字符串中的查找与替换

[力扣](https://leetcode-cn.com/problems/find-and-replace-in-string/)

由于题目给出的查找替换的组数以及长度都比较小，因此可以直接按题目意思进行模拟。

首先将source和target按indexes从小到大进行排序，然后维护一个变量now表示当前处理到S中now这个位置。

接下来遍历排好序的indexes，设当前遍历到的为pos。那么从now到pos - 1这一段必然是不会形成替换的，因此先将这一段加入到答案当中。接下来判断从pos开始的前几个字符是否能与对应的source匹配上。若能匹配，那么将对应的target加入到答案中，同时将now移动到替换后的下一个位置；若不能匹配，那么将S[now]加入到答案当中，然后将now加一。

最后在遍历完indexes之后，还需要将now到S末尾这一段加入到答案当中。

最后附上python代码：

```python
class Solution(object):
    def findReplaceString(self, S, indexes, sources, targets):
        """
        :type S: str
        :type indexes: List[int]
        :type sources: List[str]
        :type targets: List[str]
        :rtype: str
        """

        res = ''
        now = 0
        for pos, source, target in sorted(zip(indexes, sources, targets), key=lambda d:d[0]):
            res += S[now:pos]
            flag = True
            for index, char in enumerate(source):
                if S[pos + index] != char:
                    flag = False
                    break
            
            if flag:
                res += target
                now = pos + index + 1
            else:
                now = pos
        
        res += S[now:]
        return res
```
