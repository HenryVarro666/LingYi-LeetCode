---
title: "3104. Find Longest Self-Contained Substring"
aliases: ["yiduobo的每日leetcode 3104.Find Longest Self-Contained Substring"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700185321"
zhihu_id: "700185321"
zhihu_title: "yiduobo的每日leetcode 3104.Find Longest Self-Contained Substring"
question_id: "3104"
question: "Find Longest Self-Contained Substring"
problem_url: "https://leetcode.cn/problems/find-longest-self-contained-substring/"
created: "2024-05-28T00:57:34+08:00"
updated: "2024-05-28T00:57:34+08:00"
upvotes: 1
comments: 0
---

# 3104. Find Longest Self-Contained Substring

> **[yiduobo的每日leetcode 3104.Find Longest Self-Contained Substring](https://zhuanlan.zhihu.com/p/700185321) · 知乎 · 2024-05-28 · 赞同 1**
> 力扣：[3104. Find Longest Self-Contained Substring](https://leetcode.cn/problems/find-longest-self-contained-substring/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3104.Find Longest Self-Contained Substring

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-longest-self-contained-substring/description/)

leetcode上少有的翻译都没有的题。。题目给出一个由小写字母组成的字符串s，要求从中找出一个最长的子串t，满足t中出现的每种字符都仅在t中出现，而s中剩下的每种字符则都不在t中出现。

由于s仅由小写字符组成，那么可以考虑枚举t左边界上的字符进行，因此需要记录每种字符第一次出现的位置。又由于每种字符一旦出现在t中，就必须全部处于t中，因此还需要额外记录每种字符最后一次出现的位置以及出现的总次数，其中终点位置的作用是用来扩展t的右边界，而只有当t的长度等于其中各种字符出现的总数时，t才是一个合法的字符串。

有了上面这些信息，只需将每种字符按首次出现的位置从小到大进行排序，将排序后的字符记为sorted_char，然后枚举t左边界left上的字符sorted_char[i]，此时t的右边界right就应该初始化为sorted_char[i]最后一次出现的位置，而t的合法长度cnt则应该是sorted_char[i]出现的次数。若此时的t是合法的，即t的长度right - left + 1等于cnt，那么就需要先更新一次答案。

另一方面，由于字符已经按照首次出现的位置排序好了，那么如果t是合法的，且t中还有其他的字符，那么这些字符必然是按照sorted_char的顺序出现的，因此只需从i + 1开始枚举后续的字符sorted_char[j]，尝试将所有的sorted_char[j]都加入到t中。此时就应该使用sorted_char[j]最后一次出现的位置来更新right，同时将其出现的次数累加到cnt。每新加入一个字符，都需要检测此时的长度right - left + 1是否等于cnt。若满足，那么也需要更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxSubstringLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        first = {}
        last = {}
        freq = {}
        for index, char in enumerate(s):
            if char not in first:
                first[char] = index
                last[char] = index
                freq[char] = 1
            else:
                last[char] = index
                freq[char] += 1
        
        sorted_char = sorted(first.keys(), key=lambda d:first[d])
        res = -1
        for i, char in enumerate(sorted_char):
            left, right, cnt = first[char], last[char], freq[char]
            if cnt < len(s) and cnt == right - left + 1:
                res = max(res, cnt)
            for j in range(i + 1, len(sorted_char)):
                right = max(right, last[sorted_char[j]])
                cnt += freq[sorted_char[j]]
                if cnt < len(s) and cnt == right - left + 1:
                    res = max(res, cnt)
            
        return res
```
