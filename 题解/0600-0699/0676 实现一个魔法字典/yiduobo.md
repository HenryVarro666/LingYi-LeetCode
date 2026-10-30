---
title: "676. 实现一个魔法字典"
aliases: ["yiduobo的每日leetcode 676.实现一个魔法字典"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/298451309"
zhihu_id: "298451309"
zhihu_title: "yiduobo的每日leetcode 676.实现一个魔法字典"
question_id: "676"
question: "实现一个魔法字典"
problem_url: "https://leetcode.cn/problems/implement-magic-dictionary/"
created: "2020-11-17T22:37:18+08:00"
updated: "2020-11-17T22:37:18+08:00"
upvotes: 1
comments: 0
---

# 676. 实现一个魔法字典

> **[yiduobo的每日leetcode 676.实现一个魔法字典](https://zhuanlan.zhihu.com/p/298451309) · 知乎 · 2020-11-17 · 赞同 1**
> 力扣：[676. 实现一个魔法字典](https://leetcode.cn/problems/implement-magic-dictionary/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

676.实现一个魔法字典

[力扣](https://leetcode-cn.com/problems/implement-magic-dictionary/)

印象中之前也有一个题目涉及到了替换一个字符之后进行字符串匹配的问题，但是不记得具体是哪一题了。具体做法则还是一样，对于每个单词，我们逐个将其中的字符替换成特殊字符，然后将所有替换后的结果加入到dict中。接下来对于要search的单词，我们也是逐个将其中的字符替换为特殊字符，然后在查找替换结果在dict中出现的次数。若这个次数大于这个单词本身在原始词表中出现的次数，那么说明至少有一个其他单词可以进行替换。

例如hello和hhllo，替换结果分别为

\*ello，h\*llo，he\*lo，hel\*o，hell\*

\*hllo，h\*llo，hh\*lo，hhl\*o，hhll\*

那么如果我们要在里面查找hello，其每个替换结果分别出现了1、2、1、1、1次，而hello在原始词表中出现了一次，说明hello可以通过替换掉e这个位置上的字符变成词表中的其他词。

最后附上python代码：

```python
class MagicDictionary(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.word_dict = {}
        self.change_word_dict = {}

    def buildDict(self, dictionary):
        """
        :type dictionary: List[str]
        :rtype: None
        """
        for word in dictionary:
            self.word_dict[word] = 1
            for index in range(len(word)):
                tmp = word[:index] + ' ' + word[index + 1:]
                self.change_word_dict[tmp] = self.change_word_dict.get(tmp, 0) + 1
        
    def search(self, searchWord):
        """
        :type searchWord: str
        :rtype: bool
        """
        for index in range(len(searchWord)):
            tmp = searchWord[:index] + ' ' + searchWord[index + 1:]
            if self.change_word_dict.get(tmp, 0) - self.word_dict.get(searchWord, 0) > 0:
                return True

        return False

# Your MagicDictionary object will be instantiated and called as such:
# obj = MagicDictionary()
# obj.buildDict(dictionary)
# param_2 = obj.search(searchWord)
```
