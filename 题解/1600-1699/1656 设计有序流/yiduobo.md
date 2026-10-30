---
title: "1656. 设计有序流"
aliases: ["yiduobo的每日leetcode 1656.设计有序流"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/design", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/441256457"
zhihu_id: "441256457"
zhihu_title: "yiduobo的每日leetcode 1656.设计有序流"
question_id: "1656"
question: "设计有序流"
problem_url: "https://leetcode.cn/problems/design-an-ordered-stream/"
difficulty: "Easy"
created: "2021-12-04T19:44:47+08:00"
updated: "2021-12-04T19:44:47+08:00"
upvotes: 0
comments: 0
---

# 1656. 设计有序流

> **[yiduobo的每日leetcode 1656.设计有序流](https://zhuanlan.zhihu.com/p/441256457) · 知乎 · 2021-12-04 · 赞同 0**
> 力扣：[1656. 设计有序流](https://leetcode.cn/problems/design-an-ordered-stream/) · Easy · 灵茶山艾府：[阅读理解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1656.设计有序流

[力扣](https://leetcode-cn.com/problems/design-an-ordered-stream/)

比较基础的题目，只需要通过dict记录下当前有值的位置，然后对于每次insert操作而言，若当前ptr对应的位置有值，那么将这个值加入到答案中，并将ptr向后移动，直到ptr对应的位置没有值为止。

最后附上python代码：

```python
class OrderedStream(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.char_dict = {}
        self.pos = 1

    def insert(self, idKey, value):
        """
        :type idKey: int
        :type value: str
        :rtype: List[str]
        """
        self.char_dict[idKey] = value
        res = []
        while self.pos in self.char_dict:
            res.append(self.char_dict[self.pos])
            self.pos += 1
        
        return res

# Your OrderedStream object will be instantiated and called as such:
# obj = OrderedStream(n)
# param_1 = obj.insert(idKey,value)
```
