---
title: "953. 验证外星语词典"
aliases: ["yiduobo的每日leetcode 953.验证外星语词典"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359964053"
zhihu_id: "359964053"
zhihu_title: "yiduobo的每日leetcode 953.验证外星语词典"
question_id: "953"
question: "验证外星语词典"
problem_url: "https://leetcode.cn/problems/verifying-an-alien-dictionary/"
created: "2021-03-25T23:53:16+08:00"
updated: "2021-03-25T23:53:16+08:00"
upvotes: 0
comments: 0
---

# 953. 验证外星语词典

> **[yiduobo的每日leetcode 953.验证外星语词典](https://zhuanlan.zhihu.com/p/359964053) · 知乎 · 2021-03-25 · 赞同 0**
> 力扣：[953. 验证外星语词典](https://leetcode.cn/problems/verifying-an-alien-dictionary/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

953.验证外星语词典

[力扣](https://leetcode-cn.com/problems/verifying-an-alien-dictionary/)

将外星语词典与a到z建立一对一的映射，然后将words中的单词根据这个映射转化为最终的单词，然后一趟遍历比较相邻两个单词的大小关系是否符合要求即可。

最后附上python代码：

```python
class Solution(object):
    def isAlienSorted(self, words, order):
        """
        :type words: List[str]
        :type order: str
        :rtype: bool
        """

        char_dict = {}
        for index, char in enumerate(order):
            char_dict[char] = chr(index + 97)

        real_word = []
        for word in words:
            real_word.append(''.join([char_dict[x] for x in word]))
        
        for index in range(len(real_word) - 1):
            if real_word[index] > real_word[index + 1]:
                return False

        return True
```
