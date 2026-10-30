---
title: "604. 迭代压缩字符串"
aliases: ["yiduobo的每日leetcode 604.迭代压缩字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601813541"
zhihu_id: "601813541"
zhihu_title: "yiduobo的每日leetcode 604.迭代压缩字符串"
question_id: "604"
question: "迭代压缩字符串"
problem_url: "https://leetcode.cn/problems/design-compressed-string-iterator/"
created: "2023-01-30T01:06:34+08:00"
updated: "2023-01-31T00:03:39+08:00"
upvotes: 0
comments: 0
---

# 604. 迭代压缩字符串

> **[yiduobo的每日leetcode 604.迭代压缩字符串](https://zhuanlan.zhihu.com/p/601813541) · 知乎 · 2023-01-30 · 赞同 0**
> 力扣：[604. 迭代压缩字符串](https://leetcode.cn/problems/design-compressed-string-iterator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

604.迭代压缩字符串

[力扣](https://leetcode.cn/problems/design-compressed-string-iterator/)

将压缩字符串中的字符和数量拆开，形成两个数组char_list和cnt_list，并使用两个变量char_pos和cnt分别记录当前使用到的字符的下标以及该字符已经使用了几个。接下来：

1、hasNext操作：

当char_pos没有来到char_list的末尾，就说明还有字符可用，此时返回true，否则返回false

2、next操作：

若hasNext为false，那么返回空格，否则返回char_list[char_pos]，同时将cnt加上1。若此时cnt等于cnt_list[char_pos]，那么就将char_pos向后移动一位，并将cnt重置为0。

最后附上python代码：

```python
class StringIterator(object):

    def __init__(self, compressedString):
        """
        :type compressedString: str
        """

        self.char_list = []
        self.cnt_list = []

        p = 0
        while p < len(compressedString):
            self.char_list.append(compressedString[p])
            p += 1
            now = 0
            while p < len(compressedString) and compressedString[p] >= '0' and compressedString[p] <= '9':
                now = now * 10 + int(compressedString[p])
                p += 1
            
            self.cnt_list.append(now)

        self.char_pos = 0
        self.cnt = 0

    def next(self):
        """
        :rtype: str
        """
        if self.hasNext():
            res = self.char_list[self.char_pos]
            self.cnt += 1
            if self.cnt == self.cnt_list[self.char_pos]:
                self.cnt = 0
                self.char_pos += 1
            
        else:
            res = ' '
        
        return res

    def hasNext(self):
        """
        :rtype: bool
        """

        return self.char_pos != len(self.char_list)

# Your StringIterator object will be instantiated and called as such:
# obj = StringIterator(compressedString)
# param_1 = obj.next()
# param_2 = obj.hasNext()
```
