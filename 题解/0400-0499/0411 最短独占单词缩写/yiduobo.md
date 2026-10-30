---
title: "411. 最短独占单词缩写"
aliases: ["yiduobo的每日leetcode 411.最短独占单词缩写"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598951209"
zhihu_id: "598951209"
zhihu_title: "yiduobo的每日leetcode 411.最短独占单词缩写"
question_id: "411"
question: "最短独占单词缩写"
problem_url: "https://leetcode.cn/problems/minimum-unique-word-abbreviation/"
created: "2023-01-14T04:01:09+08:00"
updated: "2023-01-14T04:01:09+08:00"
upvotes: 0
comments: 0
---

# 411. 最短独占单词缩写

> **[yiduobo的每日leetcode 411.最短独占单词缩写](https://zhuanlan.zhihu.com/p/598951209) · 知乎 · 2023-01-14 · 赞同 0**
> 力扣：[411. 最短独占单词缩写](https://leetcode.cn/problems/minimum-unique-word-abbreviation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

411.最短独占单词缩写

[力扣](https://leetcode.cn/problems/minimum-unique-word-abbreviation/)

注意到题目中有一个条件 log2(n) + m \<\= 21，也就是说2^(log2(n) + m) \= n \* (2^m) \<\= 2^21，这恰好也是枚举所有子串可能缩写的复杂度。换言之，在这里使用暴力算法是完全可行的。

因此可以先枚举dictionary中的所有字符串，然后通过dfs找出这些字符串的所有缩写，并使用哈希表将这些字符串的缩写都记录下来。接下来再通过dfs找出target的所有缩写，排序后一趟遍历，找出第一个没有出现在哈希表的缩写即可。

另外，由于两个字符串的缩写如果相同，那么这两个字符串的长度必然相同，因此在最开始遍历dictionary时可以直接跳过与target长度不同的字符串。

最后附上python代码：

```python
class Solution(object):
    def minAbbreviation(self, target, dictionary):
        """
        :type target: str
        :type dictionary: List[str]
        :rtype: str
        """

        def dfs(level, now, abbr, word_set):
            if level == n:
                if abbr > 0:
                    tmp = str(abbr)
                else:
                    tmp = ''
                word_set.add(''.join(now) + tmp)
                return

            dfs(level + 1, now, abbr + 1, word_set)
            
            if abbr > 0:
                now.append(str(abbr))
                now.append(word[level])
                dfs(level + 1, now, 0, word_set)
                now.pop()
                now.pop()
            else:
                now.append(word[level])
                dfs(level + 1, now, 0, word_set)
                now.pop()
        
        dict_set = set()
        for word in dictionary:
            if len(word) != len(target):
                continue
            n = len(word)
            dfs(0, [], 0, dict_set)
        
        target_set = set()
        word = target
        n = len(word)
        dfs(0, [], 0, target_set)
        for res in sorted(list(target_set), key=lambda d:len(d)):
            if res not in dict_set:
                return res
```
