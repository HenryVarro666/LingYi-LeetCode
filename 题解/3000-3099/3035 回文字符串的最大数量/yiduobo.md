---
title: "3035. 回文字符串的最大数量"
aliases: ["yiduobo的每日leetcode 3035.回文字符串的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695747412"
zhihu_id: "695747412"
zhihu_title: "yiduobo的每日leetcode 3035.回文字符串的最大数量"
question_id: "3035"
question: "回文字符串的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-palindromes-after-operations/"
difficulty: "Medium"
rating: 1857
created: "2024-05-03T02:33:03+08:00"
updated: "2024-05-03T02:33:03+08:00"
upvotes: 0
comments: 0
---

# 3035. 回文字符串的最大数量

> **[yiduobo的每日leetcode 3035.回文字符串的最大数量](https://zhuanlan.zhihu.com/p/695747412) · 知乎 · 2024-05-03 · 赞同 0**
> 力扣：[3035. 回文字符串的最大数量](https://leetcode.cn/problems/maximum-palindromes-after-operations/) · Medium · 灵茶山艾府：[两种方法：正向思维 / 逆向思维（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3035.回文字符串的最大数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-palindromes-after-operations/description/)

题目中的操作不仅可以任意交换两个不同字符的任意一组字符，还可以任意调整单个字符串中字符的顺序，换言之，只需要字符串中的字符成对出现，那么就一定可以将其调整为回文串。

另一方面，题目要求构成的回文串数量最多，因此就应该优先构造长度较短的回文串以节省字符的使用。

于是可以一趟遍历，统计每种字符出现的次数，并收集所有字符串的长度，然后根据字符数量计算当前有多少组字符对以及多少落单的字符，分别记为pair和single。

接下来，从小到大遍历字符串的长度l，尝试构造长度为l的回文串。对于当前遍历到的l，其需要的字符对数目为l整除2，另外当l为奇数时，还需要1个落单字符。若剩余的成对字符数量不够，那么就无法构造；除此之外，若落单字符不够，则需要尝试拆开一组成对字符形成两个落单字符，若此时成对字符也不够了，那么也无法构造。

最后附上python代码：

```python
class Solution(object):
    def maxPalindromesAfterOperations(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        freq = Counter()
        length_list = []
        for w in words:
            for char in w:
                freq[char] += 1
            length_list.append(len(w))
        length_list.sort()
        
        pair = 0
        single = 0
        for f in freq.values():
            if f % 2 == 1:
                single += 1
            pair += f // 2
        
        res = 0
        for l in length_list:
            need_pair = l // 2
            need_single = l % 2

            if need_pair > pair:
                break
            pair -= need_pair
            if need_single:
                if single > 0:
                    single -= 1
                elif pair > 0:
                    pair -= 1
                    single += 1
                else:
                    break
            
            res += 1

        return res
```
