---
title: "1003. 检查替换后的词是否有效"
aliases: ["yiduobo的每日leetcode 1003.检查替换后的词是否有效"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/366182919"
zhihu_id: "366182919"
zhihu_title: "yiduobo的每日leetcode 1003.检查替换后的词是否有效"
question_id: "1003"
question: "检查替换后的词是否有效"
problem_url: "https://leetcode.cn/problems/check-if-word-is-valid-after-substitutions/"
difficulty: "Medium"
rating: 1427
created: "2021-04-19T23:49:50+08:00"
updated: "2021-04-19T23:49:50+08:00"
upvotes: 0
comments: 0
---

# 1003. 检查替换后的词是否有效

> **[yiduobo的每日leetcode 1003.检查替换后的词是否有效](https://zhuanlan.zhihu.com/p/366182919) · 知乎 · 2021-04-19 · 赞同 0**
> 力扣：[1003. 检查替换后的词是否有效](https://leetcode.cn/problems/check-if-word-is-valid-after-substitutions/) · Medium · 灵茶山艾府：[栈+简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1003.检查替换后的词是否有效

[力扣](https://leetcode-cn.com/problems/check-if-word-is-valid-after-substitutions/)

比较另类的括号匹配问题，由于这里有三个字符，因此不能再使用简单的计数法，而需要使用栈来帮忙。

回顾一下使用栈来解决括号匹配问题的方法，从左向右一趟扫描：

1、若当前字符为左括号，则将其压入栈中

2、若当前字符为右括号：

2-1）栈为空或栈顶元素为右括号：此时为非法情况

2-2）栈顶元素为左括号：此时当前的右括号与栈顶形成匹配，于是需要将栈顶元素弹出

遍历完成后，若栈为空，说明括号串有效，否则栈中还有遗留的左括号，那么括号串无效

我们可以借鉴上面的做法，也是从左向右一趟扫描：

1、当前栈为空：

此时只有当前字符为a时才合法，因为合法的子串必须是a起头的

2、栈顶元素为a：

若当前字符为a，是有可能出现的，例如aabcbc这种情况中的前两个a，于是将a压入栈中

若当前元素为b，显然是可能出现的，于是将b压入栈中

若当前元素为c，那么产生了非法情况，返回false

3、栈顶元素为b：

若当前字符为a，是有可能出现的，例如ababcc这种情况中第1个b和第2个a，于是将a压入栈中

若当前字符为b，那么产生了非法情况，返回false

若当前字符为c，那么根据上面的结论，栈顶元素为b，合法情况下栈顶的下一个元素必然是a，那么此时出现了一组abc，于是此时应该将栈顶以及栈顶的下一个元素弹出

遍历完成后，若栈为空，那么返回true，否则说明栈中必然存在未匹配的a，因此返回false。

最后附上python代码：

```python
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """

        stack = []
        for char in s:
            if not stack:
                if char != 'a':
                    return False
                else:
                    stack.append(char)
            else:
                if stack[-1] == 'a':
                    if char == 'c':
                        return False
                    else:
                        stack.append(char)
                elif stack[-1] == 'b':
                    if char == 'c':
                        stack.pop()
                        stack.pop()
                    elif char == 'a':
                        stack.append(char)
                    else:
                        return False
        
        return not stack
```
