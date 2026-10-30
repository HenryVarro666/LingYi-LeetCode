---
title: "2296. 设计一个文本编辑器"
aliases: ["yiduobo的每日leetcode 2296.设计一个文本编辑器"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/tree", "leetcode/design", "leetcode/simulation", "leetcode/ping-heng-shu", "题单/常用数据结构", "题单/常用数据结构/三-栈", "题单/常用数据结构/九-伸展树-Splay-树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/553763672"
zhihu_id: "553763672"
zhihu_title: "yiduobo的每日leetcode 2296.设计一个文本编辑器"
question_id: "2296"
question: "设计一个文本编辑器"
problem_url: "https://leetcode.cn/problems/design-a-text-editor/"
difficulty: "Hard"
rating: 1912
created: "2022-08-15T00:23:37+08:00"
updated: "2022-08-15T00:23:37+08:00"
upvotes: 1
comments: 0
---

# 2296. 设计一个文本编辑器

> **[yiduobo的每日leetcode 2296.设计一个文本编辑器](https://zhuanlan.zhihu.com/p/553763672) · 知乎 · 2022-08-15 · 赞同 1**
> 力扣：[2296. 设计一个文本编辑器](https://leetcode.cn/problems/design-a-text-editor/) · Hard · 灵茶山艾府：[对顶栈 / Splay 树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2296.设计一个文本编辑器

[力扣](https://leetcode.cn/problems/design-a-text-editor/)

带有区间操作的问题，通常的做法是使用块状链表或者伸展树，但是在这里题目需要的操作比较简单，因此也可以想办法简化。

题目需要实现：

1、在光标处插入若干个字符

2、在光标处回退若干个字符，并返回实际删除的字符数量

3、向左或向右移动光标，返回从当前光标位置开始的倒数10个字符

可以发现，操作1和操作2都是对光标左侧的数据进行操作，而操作3则是在调整光标左侧和右侧的数据构成，因此一个自然的想法就是分别维护当前光标左右两侧的数据。

只考虑操作1和操作2的话，可以发现这里的插入删除操作是很明显的后进先出的结构，那么使用一个栈来维护光标左侧的字符是顺理成章的事情。

而对于操作3来说，光标的左移相当于将左侧栈顶的字符移出，然后加入到右侧的数据结构中。而在光标右移时，这些数据又必须按照先出后进的顺序重新加入到左侧栈顶，也就是说右侧的数据结构也必须满足后进先出，那么也使用一个栈来维护右侧的数据就可以达成操作3了。

最后附上python代码：

```python
class TextEditor(object):

    def __init__(self):
        self.left_part = []
        self.right_part = []

    def addText(self, text):
        """
        :type text: str
        :rtype: None
        """
        for char in text:
            self.left_part.append(char)

    def deleteText(self, k):
        """
        :type k: int
        :rtype: int
        """
        cnt = 0
        while k and self.left_part:
            self.left_part.pop()
            k -= 1
            cnt += 1

        return cnt

    def cursorLeft(self, k):
        """
        :type k: int
        :rtype: str
        """
        while k and self.left_part:
            self.right_part.append(self.left_part.pop())
            k -= 1

        if len(self.left_part) >= 10:
            return ''.join(self.left_part[-10:])
        else:
            return ''.join(self.left_part)

    def cursorRight(self, k):
        """
        :type k: int
        :rtype: str
        """
        while k and self.right_part:
            self.left_part.append(self.right_part.pop())
            k -= 1

        if len(self.left_part) >= 10:
            return ''.join(self.left_part[-10:])
        else:
            return ''.join(self.left_part)

# Your TextEditor object will be instantiated and called as such:
# obj = TextEditor()
# obj.addText(text)
# param_2 = obj.deleteText(k)
# param_3 = obj.cursorLeft(k)
# param_4 = obj.cursorRight(k)
```
