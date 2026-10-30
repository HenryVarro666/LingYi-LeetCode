---
title: "288. 单词的唯一缩写"
aliases: ["yiduobo的每日leetcode 288.单词的唯一缩写"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594787115"
zhihu_id: "594787115"
zhihu_title: "yiduobo的每日leetcode 288.单词的唯一缩写"
question_id: "288"
question: "单词的唯一缩写"
problem_url: "https://leetcode.cn/problems/unique-word-abbreviation/"
created: "2022-12-27T22:29:28+08:00"
updated: "2022-12-27T22:29:28+08:00"
upvotes: 0
comments: 0
---

# 288. 单词的唯一缩写

> **[yiduobo的每日leetcode 288.单词的唯一缩写](https://zhuanlan.zhihu.com/p/594787115) · 知乎 · 2022-12-27 · 赞同 0**
> 力扣：[288. 单词的唯一缩写](https://leetcode.cn/problems/unique-word-abbreviation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

288.单词的唯一缩写

[力扣](https://leetcode.cn/problems/unique-word-abbreviation/)

直接根据题目意思计算dictionary中每个单词的缩写，然后使用哈希表将这些单词缩写对给储存起来。接下来对于每一组询问，只需要按照同样的方法计算缩写并判断对应的单词与询问的单词是否相同即可。

需要注意的是，若dictionary中有多个单词的缩写一致，那么这个缩写对应的所有单词都不是唯一的。

最后附上python代码：

```python
class ValidWordAbbr(object):

    def __init__(self, dictionary):
        """
        :type dictionary: List[str]
        """
        self.dict = {}
        self.multi_key = set()
        for s in dictionary:
            if len(s) > 2:
                key = s[0] + str(len(s) - 2) + s[-1]
            else:
                key = s
        
            if key in self.dict and self.dict[key] != s:
                self.multi_key.add(key)
            else:
                self.dict[key] = s

    def isUnique(self, word):
        """
        :type word: str
        :rtype: bool
        """

        if len(word) > 2:
            key = word[0] + str(len(word) - 2) + word[-1]
        else:
            key = word
        
        if key in self.multi_key:
            return False

        return self.dict.get(key, word) == word

# Your ValidWordAbbr object will be instantiated and called as such:
# obj = ValidWordAbbr(dictionary)
# param_1 = obj.isUnique(word)
```
