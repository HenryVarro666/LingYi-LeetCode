---
title: "408. 有效单词缩写"
aliases: ["yiduobo的每日leetcode 408.有效单词缩写"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598951031"
zhihu_id: "598951031"
zhihu_title: "yiduobo的每日leetcode 408.有效单词缩写"
question_id: "408"
question: "有效单词缩写"
problem_url: "https://leetcode.cn/problems/valid-word-abbreviation/"
created: "2023-01-14T03:54:40+08:00"
updated: "2023-01-14T03:54:40+08:00"
upvotes: 0
comments: 0
---

# 408. 有效单词缩写

> **[yiduobo的每日leetcode 408.有效单词缩写](https://zhuanlan.zhihu.com/p/598951031) · 知乎 · 2023-01-14 · 赞同 0**
> 力扣：[408. 有效单词缩写](https://leetcode.cn/problems/valid-word-abbreviation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

408.有效单词缩写

[力扣](https://leetcode.cn/problems/valid-word-abbreviation/)

注意到题目中的缩写只能针对不相邻的子串，那么也就意味着缩写中出现的数字唯一地代表了某个子串的长度，因此可以遍历缩写子串，然后使用一个变量p记录原串中下一个与缩写子串匹配的下标位置。若当前遍历到的是一个字符，那么就检测其与word[p]是否相同，若遍历到的是数字，那么就将p向后移动相应的位数。

若过程中出现无法匹配或者p移出边界的情况，那么就返回false。另外，若遍历完成后p没有移动到word的末尾，同样应该返回false。

最后附上python代码：

```python
class Solution(object):
    def validWordAbbreviation(self, word, abbr):
        """
        :type word: str
        :type abbr: str
        :rtype: bool
        """

        p = 0
        n = len(word)

        now = 0
        for char in abbr:
            if char >= '0' and char <= '9':
                if now == 0 and char == '0':
                    return False
                now = now * 10 + int(char)
            else:
                if now > 0:
                    p += now
                    now = 0
                
                if p >= n or word[p] != char:
                    return False
                p += 1

        if now > 0:
            p += now
        
        return p == n
```
