---
title: "291. 单词规律II"
aliases: ["yiduobo的每日leetcode 291.单词规律II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595162242"
zhihu_id: "595162242"
zhihu_title: "yiduobo的每日leetcode 291.单词规律II"
question_id: "291"
question: "单词规律II"
problem_url: "https://leetcode.cn/problems/word-pattern-ii/"
created: "2022-12-29T14:15:26+08:00"
updated: "2022-12-29T14:15:26+08:00"
upvotes: 0
comments: 0
---

# 291. 单词规律II

> **[yiduobo的每日leetcode 291.单词规律II](https://zhuanlan.zhihu.com/p/595162242) · 知乎 · 2022-12-29 · 赞同 0**
> 力扣：[291. 单词规律II](https://leetcode.cn/problems/word-pattern-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

291.单词规律II

[力扣](https://leetcode.cn/problems/word-pattern-ii/)

没有什么特别好的思路，不过好在本题的数据规模比较小，可以直接暴力dfs解决。

从pattern的头部开始逐位向后移动，对于pattern当前的字符，若其已经建立了到字符串的映射关系，那么就从s当前位置开始尝试进行匹配，当匹配成功时则继续向后进行dfs。若还没有建立映射关系，那么就从s当前位置开始向后枚举映射的字符串，对于每种可用的映射，都需要将其记录下来然后继续向后dfs。

若pattern来到末尾时s也恰好来到末尾，就说明找到了一种合法的映射。

最后附上python代码：

```python
class Solution(object):
    def wordPatternMatch(self, pattern, s):
        """
        :type pattern: str
        :type s: str
        :rtype: bool
        """

        m = len(pattern)
        n = len(s)

        def dfs(now, p, mapping, mapped):
            if now == m or p == n:
                return now == m and p == n
            
            key = pattern[now]
            if key in mapping:
                if len(mapping[key]) + p - 1 >= n:
                    return False
                flag = True
                for index, char in enumerate(mapping[key]):
                    if s[index + p] != char:
                        flag = False
                        break
                
                if flag:
                    return dfs(now + 1, p + len(mapping[key]), mapping, mapped)
                else:
                    return False
            
            else:
                for q in range(p, n):
                    val = s[p : q + 1]
                    if val not in mapped:
                        mapping[key] = val
                        mapped.add(val)
                        if dfs(now + 1, q + 1, mapping, mapped):
                            return True
                        mapped.remove(val)
                        mapping.pop(key)
                return False

        return dfs(0, 0, {}, set())
```
