---
title: "2451. 差值数组不同的字符串"
aliases: ["yiduobo的每日leetcode 2451.差值数组不同的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/585133292"
zhihu_id: "585133292"
zhihu_title: "yiduobo的每日leetcode 2451.差值数组不同的字符串"
question_id: "2451"
question: "差值数组不同的字符串"
problem_url: "https://leetcode.cn/problems/odd-string-difference/"
difficulty: "Easy"
created: "2022-11-20T18:19:35+08:00"
updated: "2022-11-20T18:19:35+08:00"
upvotes: 0
comments: 0
---

# 2451. 差值数组不同的字符串

> **[yiduobo的每日leetcode 2451.差值数组不同的字符串](https://zhuanlan.zhihu.com/p/585133292) · 知乎 · 2022-11-20 · 赞同 0**
> 力扣：[2451. 差值数组不同的字符串](https://leetcode.cn/problems/odd-string-difference/) · Easy · 灵茶山艾府：[哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2451.差值数组不同的字符串

[力扣](https://leetcode.cn/problems/odd-string-difference/)

首先可以遍历所有的字符串，利用ascii码计算出其对应的差值数组，接下来需要找出其中不同的那一个。对比words[0]、words[1]这两个字符串的差值数组，若相同，说明答案出现在后面。此时需要遍历后面的差值数组，找出与words[0]对应的差值数组不同的那一个；若不同，则说明答案就是words[0]或者words[1]，此时只需要检测words[0]和words[2]对应的差值数组是否相同。若相同，说明答案为words[1]，否则为words[0]。

最后附上python代码：

```python
class Solution(object):
    def oddString(self, words):
        """
        :type words: List[str]
        :rtype: str
        """

        diff_list = []
        for word in words:
            diff_list.append([])
            for index in range(1, len(word)):
                diff_list[-1].append(ord(word[index]) - ord(word[index - 1]))
        
        def same(p, q):
            for index in range(len(diff_list[p])):
                if diff_list[p][index] != diff_list[q][index]:
                    return False
            return True

        if same(0, 1):
            for index in range(2, len(words)):
                if not same(0, index):
                    return words[index]
        elif same(0, 2):
            return words[1]
        else:
            return words[0]
```
