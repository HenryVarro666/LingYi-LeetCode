---
title: "500. 键盘行"
aliases: ["yiduobo的每日leetcode 500.键盘行"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/258108421"
zhihu_id: "258108421"
zhihu_title: "yiduobo的每日leetcode 500.键盘行"
question_id: "500"
question: "键盘行"
problem_url: "https://leetcode.cn/problems/keyboard-row/"
created: "2020-09-22T21:13:09+08:00"
updated: "2020-09-22T21:13:09+08:00"
upvotes: 0
comments: 0
---

# 500. 键盘行

> **[yiduobo的每日leetcode 500.键盘行](https://zhuanlan.zhihu.com/p/258108421) · 知乎 · 2020-09-22 · 赞同 0**
> 力扣：[500. 键盘行](https://leetcode.cn/problems/keyboard-row/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

500.键盘行<https://leetcode-cn.com/problems/keyboard-row/>

比较基础的题目，对于每个单词遍历每个字符，判断字符其所在的行。若只使用了同一行中字符则将单词加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def findWords(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """

        set1 = set(['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 
                   'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'])
        set2 = set(['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                   'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'])

        res = []
        for word in words:
            flag1 = flag2 = flag3 = 0
            for char in word:
                if char in set1:
                    flag1 = 1
                elif char in set2:
                    flag2 = 1
                else:
                    flag3 = 1

            if flag1 + flag2 + flag3 == 1:
                res.append(word)

        return res
```
