---
title: "2942. 查找包含给定字符的单词"
aliases: ["yiduobo的每日leetcode 2942.查找包含给定字符的单词"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691394200"
zhihu_id: "691394200"
zhihu_title: "yiduobo的每日leetcode 2942.查找包含给定字符的单词"
question_id: "2942"
question: "查找包含给定字符的单词"
problem_url: "https://leetcode.cn/problems/find-words-containing-character/"
difficulty: "Easy"
created: "2024-04-08T23:30:11+08:00"
updated: "2024-04-08T23:30:11+08:00"
upvotes: 1
comments: 0
---

# 2942. 查找包含给定字符的单词

> **[yiduobo的每日leetcode 2942.查找包含给定字符的单词](https://zhuanlan.zhihu.com/p/691394200) · 知乎 · 2024-04-08 · 赞同 1**
> 力扣：[2942. 查找包含给定字符的单词](https://leetcode.cn/problems/find-words-containing-character/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2942.查找包含给定字符的单词

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-words-containing-character/description/)

比较基础的题目，一趟遍历，检测每个单词中是否包含指定字符即可。

最后附上python代码：

```python
class Solution(object):
    def findWordsContaining(self, words, x):
        """
        :type words: List[str]
        :type x: str
        :rtype: List[int]
        """

        res = []
        for i, w in enumerate(words):
            if w.find(x) != -1:
                res.append(i)
        
        return res
```
