---
title: "424. 替换后的最长重复字符"
aliases: ["yiduobo的每日leetcode 424.替换后的最长重复字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/194343478"
zhihu_id: "194343478"
zhihu_title: "yiduobo的每日leetcode 424.替换后的最长重复字符"
question_id: "424"
question: "替换后的最长重复字符"
problem_url: "https://leetcode.cn/problems/longest-repeating-character-replacement/"
created: "2020-08-22T21:04:13+08:00"
updated: "2020-08-22T21:04:13+08:00"
upvotes: 0
comments: 0
---

# 424. 替换后的最长重复字符

> **[yiduobo的每日leetcode 424.替换后的最长重复字符](https://zhuanlan.zhihu.com/p/194343478) · 知乎 · 2020-08-22 · 赞同 0**
> 力扣：[424. 替换后的最长重复字符](https://leetcode.cn/problems/longest-repeating-character-replacement/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

424.替换后的最长重复字符<https://leetcode-cn.com/problems/longest-repeating-character-replacement/>

注意到题目保证只会有大写字母，于是可以枚举s中的出现的字母，设其为最终答案中出现的字母，然后通过滑动窗口的方法从左往右进行框选，找出选择当前字母时最长的重复字符串。

滑动窗口右边界扩展的规则也很简单，只要当前的s[r]与假设的字符char相同，或者s[r]与char不同但此时k大于0，那么就可以将r往右扩展。如果是通过后一种方式进行的扩展，则表示将s[r]替换成了char，那么此时需要将k减去1。同样的，在l往右移动时，若初始的s[l]不等于char，说明之前在s[l]这里进行过一次替换，那么在l滑出去之后则需要将k加上1。

最后附上python代码：

```python
class Solution(object):
    def characterReplacement(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        if len(s) == 0:
            return 0
        
        char_set = set()
        for char in s:
            char_set.add(char)

        res = 0
        for char in char_set:
            l = r = 0
            rest_k = k
            while l < len(s) and len(s) - l > res:
                while r < len(s) and ((s[r] == char) or (s[r] != char and rest_k > 0)):
                    if s[r] != char:
                        rest_k -= 1
                    r += 1
                if r - l > res:
                    res = r - l
            
                if s[l] != char:
                    rest_k += 1
                l += 1
            
        return res
```
