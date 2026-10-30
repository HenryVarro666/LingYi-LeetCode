---
title: "824. 山羊拉丁文"
aliases: ["yiduobo的每日leetcode 824.山羊拉丁文"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344117087"
zhihu_id: "344117087"
zhihu_title: "yiduobo的每日leetcode 824.山羊拉丁文"
question_id: "824"
question: "山羊拉丁文"
problem_url: "https://leetcode.cn/problems/goat-latin/"
created: "2021-01-19T23:12:58+08:00"
updated: "2021-01-19T23:12:58+08:00"
upvotes: 0
comments: 0
---

# 824. 山羊拉丁文

> **[yiduobo的每日leetcode 824.山羊拉丁文](https://zhuanlan.zhihu.com/p/344117087) · 知乎 · 2021-01-19 · 赞同 0**
> 力扣：[824. 山羊拉丁文](https://leetcode.cn/problems/goat-latin/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

824.山羊拉丁文

[力扣](https://leetcode-cn.com/problems/goat-latin/)

比较基础的题目，直接按照题目要求进行字符串变换即可。在这里不得不感叹在不考虑性能的情况下python是真香啊。

最后附上python代码：

```python
class Solution(object):
    def toGoatLatin(self, S):
        """
        :type S: str
        :rtype: str
        """

        words = S.split(' ')
        res = []
        for index, word in enumerate(words):
            if word[0] in ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'):
                res.append(word + 'ma' + 'a' * (index + 1))
            else:
                res.append(word[1:] + word[0] + 'ma' + 'a' * (index + 1))
        
        return ' '.join(res)
```
