---
title: "1592. 重新排列单词间的空格"
aliases: ["yiduobo的每日leetcode 1592.重新排列单词间的空格"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/431862394"
zhihu_id: "431862394"
zhihu_title: "yiduobo的每日leetcode 1592.重新排列单词间的空格"
question_id: "1592"
question: "重新排列单词间的空格"
problem_url: "https://leetcode.cn/problems/rearrange-spaces-between-words/"
created: "2021-11-10T23:31:29+08:00"
updated: "2021-11-10T23:31:29+08:00"
upvotes: 0
comments: 0
---

# 1592. 重新排列单词间的空格

> **[yiduobo的每日leetcode 1592.重新排列单词间的空格](https://zhuanlan.zhihu.com/p/431862394) · 知乎 · 2021-11-10 · 赞同 0**
> 力扣：[1592. 重新排列单词间的空格](https://leetcode.cn/problems/rearrange-spaces-between-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1592.重新排列单词间的空格

[力扣](https://leetcode-cn.com/problems/rearrange-spaces-between-words/)

直接一趟扫描，将各个单词分离出来，并统计空格的总数，最后按题目要求的分配空格之后输出即可。统计时需要注意不要漏掉最后的空格，同时对于仅有一个单词的情况也需要注意特殊处理。

最后附上python代码：

```python
class Solution(object):
    def reorderSpaces(self, text):
        """
        :type text: str
        :rtype: str
        """

        cnt = 0
        word_list = []
        now = ''
        for char in text:
            if char == ' ':
                if now != '':
                    word_list.append(now)
                    now = ''
                cnt += 1
            else:
                now += char
        
        if now != '':
            word_list.append(now)
        
        if len(word_list) == 1:
            return word_list[0] + ' ' * cnt
        
        n = len(word_list) - 1 
        return (' ' * (cnt / n)).join(word_list) + ' ' * (cnt % n)
```
