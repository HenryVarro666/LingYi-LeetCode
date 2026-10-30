---
title: "1177. 构建回文串检测"
aliases: ["yiduobo的每日leetcode 1177.构建回文串检测"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380049919"
zhihu_id: "380049919"
zhihu_title: "yiduobo的每日leetcode 1177.构建回文串检测"
question_id: "1177"
question: "构建回文串检测"
problem_url: "https://leetcode.cn/problems/can-make-palindrome-from-substring/"
difficulty: "Medium"
rating: 1848
created: "2021-06-11T23:28:15+08:00"
updated: "2021-06-11T23:28:15+08:00"
upvotes: 0
comments: 0
---

# 1177. 构建回文串检测

> **[yiduobo的每日leetcode 1177.构建回文串检测](https://zhuanlan.zhihu.com/p/380049919) · 知乎 · 2021-06-11 · 赞同 0**
> 力扣：[1177. 构建回文串检测](https://leetcode.cn/problems/can-make-palindrome-from-substring/) · Medium · 灵茶山艾府：[一步步优化！从前缀和到前缀异或和（附题单！）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1177.构建回文串检测

[力扣](https://leetcode-cn.com/problems/can-make-palindrome-from-substring/)

对于询问的区间，由于可以自由排列字符的顺序，那么若某个字符出现偶数次，那么我们可以将其放在对称的位置上，而某个字符若出现奇数次，那么必然有一个落单的字符无法配对。另外，若区间长度本身就是奇数，我们则可以将一个落单的字符安排在最中间的位置。

设给定区间有n个出现奇数次的字符，若区间长度为奇数则需要将n减去1，表示目前一共有n个字符无法配对。那么在一次修改之后，我们可以将其中两个字符配对，也就是说k次修改最多可以解决掉2 \* k个落单字符的配对问题，那么只需要判断n和2 \* k的大小就能判断当前区间能否变成回文串。

而对于区间内每个字符出现次数的问题，我们则可以经典的前缀数组来解决。

最后附上python代码：

```python
class Solution(object):
    def canMakePaliQueries(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        cnt_dict = {}
        cnt_dict_list = []
        for char in s:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
            cnt_dict_list.append(cnt_dict.copy())
        
        res = []
        for l, r, k in queries:
            odd = 0
            for index in range(26):
                char = chr(index + 97)
                cnt = cnt_dict_list[r].get(char, 0)
                if l > 0:
                    cnt -= cnt_dict_list[l - 1].get(char, 0)
                
                if cnt % 2 == 1:
                    odd += 1
            
            if (r - l + 1) % 2 == 1:
                odd -= 1
            
            res.append(odd <= k + k)
        
        return res
```
