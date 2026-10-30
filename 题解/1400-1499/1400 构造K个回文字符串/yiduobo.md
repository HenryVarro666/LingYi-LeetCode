---
title: "1400. 构造K个回文字符串"
aliases: ["yiduobo的每日leetcode 1400.构造K个回文字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/404764374"
zhihu_id: "404764374"
zhihu_title: "yiduobo的每日leetcode 1400.构造K个回文字符串"
question_id: "1400"
question: "构造K个回文字符串"
problem_url: "https://leetcode.cn/problems/construct-k-palindrome-strings/"
created: "2021-08-29T17:09:01+08:00"
updated: "2021-08-29T17:09:01+08:00"
upvotes: 0
comments: 0
---

# 1400. 构造K个回文字符串

> **[yiduobo的每日leetcode 1400.构造K个回文字符串](https://zhuanlan.zhihu.com/p/404764374) · 知乎 · 2021-08-29 · 赞同 0**
> 力扣：[1400. 构造K个回文字符串](https://leetcode.cn/problems/construct-k-palindrome-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1400.构造K个回文字符串

[力扣](https://leetcode-cn.com/problems/construct-k-palindrome-strings/)

首先，每个字符单独拎出来都是一个回文字符串，因此最多一共可以构造出n \= len(s)个回文字符串。若n小于k，那么答案必然为false。

接下来，分析回文字符串的特点。对于一个奇数长度的回文字符串，其必然具备一个单独出现的中心字符，然后在这个中心字符两侧扩展出成对的字符；对于一个偶数长度的回文字符串，其没有中心字符，但同样是由一些成对的字符构成的。

换言之，每个落单的字符都必须要形成一个奇数长度的回文串，于是一个自然的想法是统计落单字符的数目odd，若odd > k，那么答案必然为false。

对于其他情况，我们则可以先用这odd个落单字符构成odd个回文字符串，那么就需要使用剩下even \= (n - odd) / 2组成对的字符来构成余下的rest \= k - odd个回文字符串。

若这里的rest为偶数，那么我可以拆开rest / 2组成对的字符作为回文字符串的中心，然后将其他的成对字符串随意放在这些回文字符的两侧即可。

若这里的rest为奇数，那么我们同样是拆开rest / 2组成对的字符作为回文字符串的中心，再选择字符成对字符构成一个长度为2的回文字符串，然后将其他的成对字符串随意放在这些回文字符的两侧即可。

由于这里的k \< n，从而有even \= (n - odd) / 2 > (k - odd) / 2 \= rest / 2，也就说明必然有足够的成对字符串来构成k个回文字符串。

最后附上python代码：

```python
class Solution(object):
    def canConstruct(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: bool
        """

        if len(s) < k:
            return False

        cnt_dict = {}
        for char in s:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        odd = 0
        for index in range(26):
            cnt = cnt_dict.get(chr(index + 97), 0)
            if cnt % 2 == 1:
                odd += 1
        
        if k < odd:
            return False
        
        return True
```
