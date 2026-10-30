---
title: "1839. 所有元音按顺序排布的最长子字符串"
aliases: ["yiduobo的每日leetcode 1839.所有元音按顺序排布的最长子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/zheng-ze-biao-da-shi", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/469337882"
zhihu_id: "469337882"
zhihu_title: "yiduobo的每日leetcode 1839.所有元音按顺序排布的最长子字符串"
question_id: "1839"
question: "所有元音按顺序排布的最长子字符串"
problem_url: "https://leetcode.cn/problems/longest-substring-of-all-vowels-in-order/"
difficulty: "Medium"
rating: 1580
created: "2022-02-18T23:14:03+08:00"
updated: "2022-02-18T23:14:03+08:00"
upvotes: 0
comments: 0
---

# 1839. 所有元音按顺序排布的最长子字符串

> **[yiduobo的每日leetcode 1839.所有元音按顺序排布的最长子字符串](https://zhuanlan.zhihu.com/p/469337882) · 知乎 · 2022-02-18 · 赞同 0**
> 力扣：[1839. 所有元音按顺序排布的最长子字符串](https://leetcode.cn/problems/longest-substring-of-all-vowels-in-order/) · Medium · 灵茶山艾府：[O(N) 模拟，或正则表达式](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1839.所有元音按顺序排布的最长子字符串

[力扣](https://leetcode-cn.com/problems/longest-substring-of-all-vowels-in-order/)

题目要求的子字符串需要满足单调性，并包含全部五种字符。由于是子字符串，因此在处理单调性上可以直接一趟遍历，对比相邻字符的大小。在遍历过程中，则可以利用哈希表收集出现过的字符，然后通过哈希表中字符的数目来判断当前子字符串是否具有全部五中字符。

具体来说，就是从头开始向后一趟遍历，对于当前字符word[index]：

1、若其大于等于上一个字符word[index - 1]，那么将其加入到哈希表，然后继续向后遍历

2、若其小于上一个字符word[index - 1]，那么说明上一个子字符串已经结束，此时需要检测哈希表中是否有全部五种字符。若有，那么使用上一个子字符串的长度来更新答案。

无论如何接下来都需要情况哈希表，再将word[index]加入到哈希表中去。

遍历完成后，还需要检测最后一个子字符串是否包含全部五中字符，若包含，那么还需要用该字符串的长度来更新答案。

最后附上python代码：

```python
class Solution(object):
    def longestBeautifulSubstring(self, word):
        """
        :type word: str
        :rtype: int
        """

        char_set = set()
        start = None
        last = None
        res = 0

        for index, char in enumerate(word):
            if start is None:
                start = index
            elif char < last:
                if len(char_set) == 5:
                    res = max(res, index - start)
                start = index
                char_set = set()
            
            last = char
            char_set.add(char)
            
        if len(char_set) == 5:
            res = max(res, len(word) - start)
        
        return res
```
