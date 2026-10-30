---
title: "2434. 使用机器人打印字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 2434.使用机器人打印字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/greedy", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/三-栈", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/583129574"
zhihu_id: "583129574"
zhihu_title: "yiduobo的每日leetcode 2434.使用机器人打印字典序最小的字符串"
question_id: "2434"
question: "使用机器人打印字典序最小的字符串"
problem_url: "https://leetcode.cn/problems/using-a-robot-to-print-the-lexicographically-smallest-string/"
difficulty: "Medium"
rating: 1953
created: "2022-11-14T01:01:32+08:00"
updated: "2022-11-14T01:01:32+08:00"
upvotes: 0
comments: 0
---

# 2434. 使用机器人打印字典序最小的字符串

> **[yiduobo的每日leetcode 2434.使用机器人打印字典序最小的字符串](https://zhuanlan.zhihu.com/p/583129574) · 知乎 · 2022-11-14 · 赞同 0**
> 力扣：[2434. 使用机器人打印字典序最小的字符串](https://leetcode.cn/problems/using-a-robot-to-print-the-lexicographically-smallest-string/) · Medium · 灵茶山艾府：[贪心 + 栈（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2434.使用机器人打印字典序最小的字符串

[力扣](https://leetcode.cn/problems/using-a-robot-to-print-the-lexicographically-smallest-string/)

题目中的机器人实际上是起到了一个栈的作用。

设原始字符串中字典序最小的字符为target，那么在第一轮操作时就应该将最左侧target左边的所有字符压入栈中，然后将target加入到答案，接下来将剩余字符串中最左侧target左边的所有字符压入栈中，然后将第二个target加入到答案，这样依次类推，直到最后一个target加入到答案为止。

接下来，可以选择target在ascii码表中的下一个字符作为新的target，但是需要注意的是，此时不能完全照搬第一轮的操作，因为此时栈顶的元素可能小于等于target。例如字符串bacb，在第一轮target \= 'a'时，b被压入了栈中，那么在第二轮的操作中，应该首先将栈中的b弹出，然后再考虑剩下的字符串cb。

简单来说，后续的轮次必须先判断当前栈顶元素是否小于等于target，然后再执行第一轮的操作。又由于进行第一轮操作前栈必然是空的，那么可以将判断栈顶元素这个步骤也加入到第一轮中。

需要注意的是，当字符串中的字符都被处理掉之后，可能出现栈非空的情况，此时需要记得将栈中的字符倒出来加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def robotWithString(self, s):
        """
        :type s: str
        :rtype: str
        """

        stack = []
        char_cnt = {}
        for char in s:
            char_cnt[char] = char_cnt.get(char, 0) + 1

        target = 'a'
        p = 0
        n = len(s)
        res = []
        while p < n:
            while stack and stack[-1] <= target:
                res.append(stack[-1])
                stack.pop()
            
            while char_cnt.get(target, 0) > 0:
                if s[p] == target:
                    res.append(target)
                else:
                    stack.append(s[p])

                char_cnt[s[p]] -= 1
                p += 1
            
            target = chr(ord(target) + 1)
        
        while stack:
            res.append(stack[-1])
            stack.pop()
        
        return ''.join(res)
```
