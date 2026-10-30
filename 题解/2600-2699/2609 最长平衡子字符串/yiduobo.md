---
title: "2609. 最长平衡子字符串"
aliases: ["yiduobo的每日leetcode 2609.最长平衡子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645300062"
zhihu_id: "645300062"
zhihu_title: "yiduobo的每日leetcode 2609.最长平衡子字符串"
question_id: "2609"
question: "最长平衡子字符串"
problem_url: "https://leetcode.cn/problems/find-the-longest-balanced-substring-of-a-binary-string/"
difficulty: "Easy"
created: "2023-07-23T01:20:53+08:00"
updated: "2023-07-23T01:20:53+08:00"
upvotes: 0
comments: 0
---

# 2609. 最长平衡子字符串

> **[yiduobo的每日leetcode 2609.最长平衡子字符串](https://zhuanlan.zhihu.com/p/645300062) · 知乎 · 2023-07-23 · 赞同 0**
> 力扣：[2609. 最长平衡子字符串](https://leetcode.cn/problems/find-the-longest-balanced-substring-of-a-binary-string/) · Easy · 灵茶山艾府：[O(n) 分段遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2609.最长平衡子字符串

[力扣](https://leetcode.cn/problems/find-the-longest-balanced-substring-of-a-binary-string/)

首先，可以将题目给出的字符串拆分成连续的0、连续的1交错出现的形式，接下来对于一段连续的0和其后方紧接着的连续的1，就可以从这一段0中选取长度为k的后缀，从这一段1中选组长度为k的前缀，这样一来就组合成了一个长度为2k的平衡子串。

为了使得平衡子串最长，那么就应该让这个k尽量大，而这个k的最大值就是这一段0的长度以及这一段1的长度的较小值。于是只需一趟遍历，每次分离出一段连续的0和一段连续的1，然后取二者长度的较小值更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def findTheLongestBalancedSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        p = 0
        res = 0
        while p < len(s):
            start = p
            while p < len(s) and s[p] == '0':
                p += 1
            zero_cnt = p - start

            start = p
            while p < len(s) and s[p] == '1':
                p += 1
            one_cnt = p - start
            
            res = max(res, min(zero_cnt, one_cnt))
        
        return res + res
```
