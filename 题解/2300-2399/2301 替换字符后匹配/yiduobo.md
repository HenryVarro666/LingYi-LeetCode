---
title: "2301. 替换字符后匹配"
aliases: ["yiduobo的每日leetcode 2301.替换字符后匹配"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/554569228"
zhihu_id: "554569228"
zhihu_title: "yiduobo的每日leetcode 2301.替换字符后匹配"
question_id: "2301"
question: "替换字符后匹配"
problem_url: "https://leetcode.cn/problems/match-substring-after-replacement/"
difficulty: "Hard"
created: "2022-08-16T23:45:30+08:00"
updated: "2022-08-16T23:45:30+08:00"
upvotes: 0
comments: 0
---

# 2301. 替换字符后匹配

> **[yiduobo的每日leetcode 2301.替换字符后匹配](https://zhuanlan.zhihu.com/p/554569228) · 知乎 · 2022-08-16 · 赞同 0**
> 力扣：[2301. 替换字符后匹配](https://leetcode.cn/problems/match-substring-after-replacement/) · Hard · 灵茶山艾府：[预处理 + 暴力枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2301.替换字符后匹配

[力扣](https://leetcode.cn/problems/match-substring-after-replacement/)

没有什么特别好的思路，不过题目的数据规模不大，直接在s中枚举匹配的起点，然后一趟遍历，利用哈希表来进行暴力匹配也是可行的，最终的时间复杂度为O(n^2)。

需要注意题目中的转化是可以一对多的。

最后附上python代码：

```python
class Solution(object):
    def matchReplacement(self, s, sub, mappings):
        """
        :type s: str
        :type sub: str
        :type mappings: List[List[str]]
        :rtype: bool
        """

        reverse_mapping = {}
        for char in s:
            if char not in reverse_mapping:
                reverse_mapping[char] = set()
        
        for old, new in mappings:
            if new not in reverse_mapping:
                continue
            reverse_mapping[new].add(old)
        
        for i in range(len(s) - len(sub) + 1):
            flag = True
            for j in range(len(sub)):
                if s[i + j] != sub[j] and sub[j] not in reverse_mapping[s[i + j]]:
                    flag = False
                    break
            
            if flag:
                return True
        
        return False
```
