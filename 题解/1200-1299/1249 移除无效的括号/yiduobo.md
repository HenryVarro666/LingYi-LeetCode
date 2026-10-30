---
title: "1249. 移除无效的括号"
aliases: ["yiduobo的每日leetcode 1249.移除无效的括号"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/385851337"
zhihu_id: "385851337"
zhihu_title: "yiduobo的每日leetcode 1249.移除无效的括号"
question_id: "1249"
question: "移除无效的括号"
problem_url: "https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/"
difficulty: "Medium"
rating: 1657
created: "2021-07-01T22:41:54+08:00"
updated: "2021-07-01T22:41:54+08:00"
upvotes: 0
comments: 0
---

# 1249. 移除无效的括号

> **[yiduobo的每日leetcode 1249.移除无效的括号](https://zhuanlan.zhihu.com/p/385851337) · 知乎 · 2021-07-01 · 赞同 0**
> 力扣：[1249. 移除无效的括号](https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/) · Medium · 灵茶山艾府：[用栈记录未匹配的左括号（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1249.移除无效的括号

[力扣](https://leetcode-cn.com/problems/minimum-remove-to-make-valid-parentheses/)

题目的需求只跟括号有关，因此我们可以忽略掉所有的字母。题目中的有效括号字符串，实际上可以用经典的栈来进行判别。当出现非法的括号时，将其删去即可。

具体来说就是从头开始向后进行扫描，对于当前字符：

1、若该字符为左括号，那么将其加入到栈中

2、若该字符为右括号，那么需要判断此时栈中是否有左括号。若有，则这两个括号就是一对，于是需要将栈顶的括号弹出，否则说明当前括号是非法的，需要将其移除

3、其他情况，直接忽略掉然后继续向后扫描即可

扫描完成后，若栈不为空，说明栈中有若干多余的非法左括号，因此也需要将这些括号移除

最后附上python代码：

```python
class Solution(object):
    def minRemoveToMakeValid(self, s):
        """
        :type s: str
        :rtype: str
        """

        stack = []
        invalid_set = set()
        for index, char in enumerate(s):
            if char == '(':
                stack.append(index)
            elif char == ')':
                if stack:
                    stack.pop()
                else:
                    invalid_set.add(index)
        
        while stack:
            invalid_set.add(stack.pop())
        
        res = ''
        for index, char in enumerate(s):
            if index not in invalid_set:
                res += char
        
        return res
```
