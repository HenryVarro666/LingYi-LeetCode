---
title: "3561. 移除相邻字符"
aliases: ["yiduobo的每日leetcode 3561.移除相邻字符"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1910522795395363623"
zhihu_id: "1910522795395363623"
zhihu_title: "yiduobo的每日leetcode 3561.移除相邻字符"
question_id: "3561"
question: "移除相邻字符"
problem_url: "https://leetcode.cn/problems/resulting-string-after-adjacent-removals/"
difficulty: "Medium"
rating: 1397
created: "2025-05-28T22:52:37+08:00"
updated: "2025-05-28T22:52:37+08:00"
upvotes: 1
comments: 0
---

# 3561. 移除相邻字符

> **[yiduobo的每日leetcode 3561.移除相邻字符](https://zhuanlan.zhihu.com/p/1910522795395363623) · 知乎 · 2025-05-28 · 赞同 1**
> 力扣：[3561. 移除相邻字符](https://leetcode.cn/problems/resulting-string-after-adjacent-removals/) · Medium · 灵茶山艾府：[栈+邻项消除，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3561.移除相邻字符

[3561. 移除相邻字符 - 力扣（LeetCode）](https://leetcode.cn/problems/resulting-string-after-adjacent-removals/description/)

题目给出一个由小写字符组成的字符串s，若s中存在两个相邻的连续字符，就需要将s中最左侧的一对相邻连续字符从s中移除，然后将剩下的字符向左移动填补空隙。问最终得到的字符串是什么。

连续字符指的是字母表中相邻的两个字符，不管是正序或者是逆序。另外'a'和'z'也算是连续字符。

一趟遍历，对于当前遍历到的字符，需要先检测其与之前处理完的字符串中的最后一个字符是否连续，若连续，则需要消除这两个字符，也就是将之前字符串的最后一个删去，若不连续，则需要将当前字符加入到处理完的字符串的末尾。

可以发现这是一个后进先出的场景，于是可以使用一个栈来储存处理完的字符串，然后对于当前字符，将其与栈顶字符进行比较，若连续，则弹出栈顶字符，否则将当前字符加入到栈中。遍历完成后，栈中字符形成的字符串即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def resultingString(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        stack = []
        for char in s:
            if stack and (abs(ord(char) - ord(stack[-1])) == 1 or abs(ord(char) - ord(stack[-1])) == 25):
                stack.pop()
            else:
                stack.append(char)
        
        return ''.join(stack)
```
