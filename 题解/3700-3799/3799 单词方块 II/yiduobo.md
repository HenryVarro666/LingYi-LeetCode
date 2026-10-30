---
title: "3799. 单词方块II"
aliases: ["yiduobo的每日leetcode 3799.单词方块II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "leetcode/sorting", "leetcode/simulation", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992276385759240979"
zhihu_id: "1992276385759240979"
zhihu_title: "yiduobo的每日leetcode 3799.单词方块II"
question_id: "3799"
question: "单词方块 II"
problem_url: "https://leetcode.cn/problems/word-squares-ii/"
difficulty: "Medium"
rating: 1606
created: "2026-01-09T01:34:05+08:00"
updated: "2026-01-09T01:34:06+08:00"
upvotes: 1
comments: 0
---

# 3799. 单词方块II

> **[yiduobo的每日leetcode 3799.单词方块II](https://zhuanlan.zhihu.com/p/1992276385759240979) · 知乎 · 2026-01-09 · 赞同 1**
> 力扣：[3799. 单词方块 II](https://leetcode.cn/problems/word-squares-ii/) · Medium · 灵茶山艾府：[排列型回溯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3799.单词方块II

[3799. 单词方块 II - 力扣（LeetCode）](https://leetcode.cn/problems/word-squares-ii/description/)

题目给出一个字符串数组words，其中包含一组互不相同且由小写英文字母组成的四字母字符串。words的长度不超过15。

单词方块指的是由4个互不相同的单词组成：top、left、right以及bottom，其中

- top形成顶部行
- bottom形成底部行
- left形成左侧列（从上到下）
- right形成右侧列（有上到下）

这个方块必须满足：

- top[0] \= left[0], top[3] \= right[0]
- bottom[0] \= left[3], bottom[3] \= right[3]

要求返回所有满足要求的不同单词方块，按(top, left, right, bottom)的字典序升序排序

由于words的长度不超过15，因此可以直接四重循环暴力，枚举形成四条边的单词，然后检测是否符合构成方块的条件即可。

由于题目需要保证按(top, left, right, bottom)的字典序升序排序，因此需要先将words排序，然后按照top、left、right、bottom的顺序来进行枚举。

最后附上python代码：

```python
class Solution(object):
    def wordSquares(self, words):
        """
        :type words: List[str]
        :rtype: List[List[str]]
        """
        
        res = []
        words.sort()
        for top in words:
            for left in words:
                if top == left or top[0] != left[0]:
                    continue
                for right in words:
                    if top == right or left == right or top[3] != right[0]:
                        continue
                    for bottom in words:
                        if top == bottom or left == bottom or right == bottom or bottom[0] != left[3] or bottom[3] != right[3]:
                            continue
                        res.append((top, left, right, bottom))
        
        return res
```
