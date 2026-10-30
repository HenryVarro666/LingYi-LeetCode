---
title: "3913. 按频率对元音排序"
aliases: ["yiduobo的每日leetcode 3913.按频率对元音排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2032958958906949871"
zhihu_id: "2032958958906949871"
zhihu_title: "yiduobo的每日leetcode 3913.按频率对元音排序"
question_id: "3913"
question: "按频率对元音排序"
problem_url: "https://leetcode.cn/problems/sort-vowels-by-frequency/"
difficulty: "Medium"
created: "2026-04-29T23:10:50+08:00"
updated: "2026-04-29T23:10:50+08:00"
upvotes: 1
comments: 0
---

# 3913. 按频率对元音排序

> **[yiduobo的每日leetcode 3913.按频率对元音排序](https://zhuanlan.zhihu.com/p/2032958958906949871) · 知乎 · 2026-04-29 · 赞同 1**
> 力扣：[3913. 按频率对元音排序](https://leetcode.cn/problems/sort-vowels-by-frequency/) · Medium · 灵茶山艾府：[节省空间的做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3913.按频率对元音排序

<https://leetcode.cn/problems/sort-vowels-by-frequency/>

题目给出一个由小写英文字母组成的字符串s。现在要求将其中的元音字母按照出现频率从高到低进行排序，若两种元音字母出现频率相同，则按照它们在s中首次出现的位置排序。

要求返回修改后的字符串。

先对s进行一趟遍历，使用哈希表记录每种元音字母出现的次数以及首次出现的下标。接下来对哈希表的key，也就是所有出现过的元音字母按照题目描述的，以出现次数为第一关键字，首次出现的位置为第二关键字进行排序。

接下来再对s进行一趟遍历，若当前遍历到的字符为元音字符，就将排序后的元音字符填充到答案中，否则将当前字符填充到答案中。

最后附上python代码：

```python
class Solution(object):
    def sortVowels(self, s):
        """
        :type s: str
        :rtype: str
        """

        vowel = {
            'a': [0, None],
            'e': [0, None],
            'i': [0, None],
            'o': [0, None],
            'u': [0, None]
        }

        for index, c in enumerate(s):
            if c in vowel:
                if vowel[c][0] == 0:
                    vowel[c][1] = index
                vowel[c][0] += 1
        
        v = sorted(vowel.keys(), key=lambda d:(-vowel[d][0], vowel[d][1]))
        res = []
        p = 0
        for c in s:
            if c in vowel:
                res.append(v[p])
                vowel[v[p]][0] -= 1
                if vowel[v[p]][0] == 0:
                    p += 1
            else:
                res.append(c)

        return ''.join(res)
```
