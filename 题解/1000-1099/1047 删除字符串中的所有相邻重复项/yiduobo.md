---
title: "1047. 删除字符串中的所有相邻重复项"
aliases: ["yiduobo的每日leetcode 1047.删除字符串中的所有相邻重复项"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/371236571"
zhihu_id: "371236571"
zhihu_title: "yiduobo的每日leetcode 1047.删除字符串中的所有相邻重复项"
question_id: "1047"
question: "删除字符串中的所有相邻重复项"
problem_url: "https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/"
difficulty: "Easy"
rating: 1286
created: "2021-05-10T21:52:42+08:00"
updated: "2021-05-10T21:52:42+08:00"
upvotes: 0
comments: 0
---

# 1047. 删除字符串中的所有相邻重复项

> **[yiduobo的每日leetcode 1047.删除字符串中的所有相邻重复项](https://zhuanlan.zhihu.com/p/371236571) · 知乎 · 2021-05-10 · 赞同 0**
> 力扣：[1047. 删除字符串中的所有相邻重复项](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/) · Easy · 灵茶山艾府：[【套路】邻项消除问题，附题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1047.删除字符串中的所有相邻重复项

[力扣](https://leetcode-cn.com/problems/remove-all-adjacent-duplicates-in-string/)

首先，很容易想到的一种做法是从头向后一趟扫描，若当前的S[index]等于S[index + 1]，那么就将这两个字符移除，同时需要继续对比index之前最后一个幸存的字符以及index + 1的下一个字符也就是S[index + 2]。对于S[index + 2]，下一个扫描的选项就是该字符，而对于index之前最后一个幸存的字符则需要想办法储存起来，于是很自然想到利用栈来维护当前留下的字符。

那么现在的做法就是使用一个栈stack来储存留下来的字符，接下来从头开始向后进行扫描。对于当前的S[index]，若其与栈顶字符相同，那么就将栈顶字符弹出，否则将S[index]压入栈中。扫描完成后，栈中的字符就是最终的答案。

最后附上python代码：

```python
class Solution(object):
    def removeDuplicates(self, S):
        """
        :type S: str
        :rtype: str
        """

        stack = []
        for char in S:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)
        
        return ''.join(stack)
```
