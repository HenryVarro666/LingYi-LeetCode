---
title: "3853. 合并靠近字符"
aliases: ["yiduobo的每日leetcode 3853.合并靠近字符"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011513748242846695"
zhihu_id: "2011513748242846695"
zhihu_title: "yiduobo的每日leetcode 3853.合并靠近字符"
question_id: "3853"
question: "合并靠近字符"
problem_url: "https://leetcode.cn/problems/merge-close-characters/"
difficulty: "Medium"
rating: 1472
created: "2026-03-06T01:43:51+08:00"
updated: "2026-03-06T01:43:52+08:00"
upvotes: 1
comments: 0
---

# 3853. 合并靠近字符

> **[yiduobo的每日leetcode 3853.合并靠近字符](https://zhuanlan.zhihu.com/p/2011513748242846695) · 知乎 · 2026-03-06 · 赞同 1**
> 力扣：[3853. 合并靠近字符](https://leetcode.cn/problems/merge-close-characters/) · Medium · 灵茶山艾府：[O(n) 简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3853.合并靠近字符

<https://leetcode.cn/problems/merge-close-characters/description/>

题目给出一个由小写英文字母组成的字符串s，以及一个整数k。

若当前的s中，由两个相同字符之间的下标距离至多为k，那么就认为它们是靠近的。若两个字符靠近，右侧的字符则会合并到左侧。合并操作按从左到右的顺序逐对进行，每次合并后，字符串都会更新，直到无法再次合并为止。若可以进行多次合并，则需要选择左侧下标最小的那一对进行合并。若存在多对字符共享最小的左侧下标，则需要选择右侧下标最小的那一对。

问合并完成后的字符串是什么。

由于题目中的合并操作必须选择下标对最小的那一组先执行，那么就可以按从左到右的顺序遍历所有字符，若当前字符出现在答案字符串的最后k个字符中，就说明当前字符需要被合并，反之则需要将其加入到答案字符串。

对于判断当前字符是否在答案字符串的最后k个字符中出现这个问题，由于s中只有小写字母，因此在这里可以使用暴力法、哈希表或者压缩后的位运算来进行判断。

最后附上python代码：

```python
class Solution(object):
    def mergeCharacters(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """
        
        res = []
        state = 0

        for c in s:
            v = 1 << (ord(c) - 97)
            if (state & v) == v:
                continue
            
            res.append(c)
            state |= v
            if len(res) > k:
                state ^= 1 << (ord(res[-k - 1]) - 97)
        
        return ''.join(res)
```
