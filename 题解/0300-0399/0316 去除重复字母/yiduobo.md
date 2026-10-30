---
title: "316. 去除重复字母"
aliases: ["yiduobo的每日leetcoede 316.去除重复字母"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/四-最小字典序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/159213709"
zhihu_id: "159213709"
zhihu_title: "yiduobo的每日leetcoede 316.去除重复字母"
question_id: "316"
question: "去除重复字母"
problem_url: "https://leetcode.cn/problems/remove-duplicate-letters/"
difficulty: "Medium"
rating: 2185
created: "2020-07-13T21:58:51+08:00"
updated: "2020-07-13T21:58:51+08:00"
upvotes: 0
comments: 1
---

# 316. 去除重复字母

> **[yiduobo的每日leetcoede 316.去除重复字母](https://zhuanlan.zhihu.com/p/159213709) · 知乎 · 2020-07-13 · 赞同 0**
> 力扣：[316. 去除重复字母](https://leetcode.cn/problems/remove-duplicate-letters/) · Medium · 灵茶山艾府：[跟着我过一遍示例 2，你就明白怎么做了（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

316.去除重复字母<https://leetcode-cn.com/problems/remove-duplicate-letters/>

经典的贪心题目。

注意到题目要求的是字典序最小，那么对于一个字符串，若其中某个字符p的左边一位字符q满足q > p，且q在p右侧再次出现过，那么此时p左侧的q必然是要删除的。

于是可以通过维护一个栈来实现，具体为从左往右一趟扫描，若当前字符不在栈中：

1、若当前字符小于栈顶字符，且栈顶字符在当前字符右侧还出现过，那么将栈顶字符弹出，直至栈为空或者栈顶字符小于当前字符。

2、将当前字符压入栈中。

这样一来，就一定能保证栈中保留了所有的字符各一个，且字典序最小。

最后附上python代码：

```python
class Solution(object):
    def removeDuplicateLetters(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_counts = {}
        for char in s:
            char_counts[char] = char_counts.get(char, 0) + 1

        res = []
        in_stack = set()

        for char in s:
            if char not in in_stack:
                while res and char_counts[res[-1]] > 0 and res[-1] > char:
                    in_stack.remove(res.pop())
                res.append(char)
                in_stack.add(char)
            char_counts[char] -= 1

        return ''.join(res)
```
