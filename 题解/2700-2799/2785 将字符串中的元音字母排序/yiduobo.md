---
title: "2785. 将字符串中的元音字母排序"
aliases: ["yiduobo的每日leetcode 2785.将字符串中的元音字母排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/counting-sort"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656363204"
zhihu_id: "656363204"
zhihu_title: "yiduobo的每日leetcode 2785.将字符串中的元音字母排序"
question_id: "2785"
question: "将字符串中的元音字母排序"
problem_url: "https://leetcode.cn/problems/sort-vowels-in-a-string/"
difficulty: "Medium"
created: "2023-09-15T04:15:00+08:00"
updated: "2023-09-15T04:15:00+08:00"
upvotes: 0
comments: 0
---

# 2785. 将字符串中的元音字母排序

> **[yiduobo的每日leetcode 2785.将字符串中的元音字母排序](https://zhuanlan.zhihu.com/p/656363204) · 知乎 · 2023-09-15 · 赞同 0**
> 力扣：[2785. 将字符串中的元音字母排序](https://leetcode.cn/problems/sort-vowels-in-a-string/) · Medium · 灵茶山艾府：[三种写法：排序/位运算优化/计数排序（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2785.将字符串中的元音字母排序

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sort-vowels-in-a-string/)

首先一趟遍历，将所有元音字母都收集起来并排序，得到排序后的元音字母数组vowel_list。接下来再一趟遍历，并使用一个变量p表示当前遍历到了原字符串中的第几个元音字母。对于当前遍历到的字符char，若char不是元音字母，那么就直接将其加入到答案中，否则就将vowel_list[p]加入到答案中，并将p加上1。

最后附上python代码：

```python
class Solution(object):
    def sortVowels(self, s):
        """
        :type s: str
        :rtype: str
        """

        vowel_set = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])
        vowel_list = []
        for char in s:
            if char in vowel_set:
                vowel_list.append(char)
        
        vowel_list.sort()
        p = 0
        res = []
        for char in s:
            if char in vowel_set:
                res.append(vowel_list[p])
                p += 1
            else:
                res.append(char)
        
        return ''.join(res)
```
