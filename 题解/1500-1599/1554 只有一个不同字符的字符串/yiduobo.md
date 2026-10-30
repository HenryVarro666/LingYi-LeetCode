---
title: "1554. 只有一个不同字符的字符串"
aliases: ["yiduobo的每日leetcode 1554.只有一个不同字符的字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617798590"
zhihu_id: "617798590"
zhihu_title: "yiduobo的每日leetcode 1554.只有一个不同字符的字符串"
question_id: "1554"
question: "只有一个不同字符的字符串"
problem_url: "https://leetcode.cn/problems/strings-differ-by-one-character/"
created: "2023-03-29T00:05:50+08:00"
updated: "2023-03-29T00:05:50+08:00"
upvotes: 0
comments: 1
---

# 1554. 只有一个不同字符的字符串

> **[yiduobo的每日leetcode 1554.只有一个不同字符的字符串](https://zhuanlan.zhihu.com/p/617798590) · 知乎 · 2023-03-29 · 赞同 0**
> 力扣：[1554. 只有一个不同字符的字符串](https://leetcode.cn/problems/strings-differ-by-one-character/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1554.只有一个不同字符的字符串

[力扣](https://leetcode.cn/problems/strings-differ-by-one-character/)

题目实际上是要求找出两个字符串，在同一个位置抹去一个字符后这两个字符串是否完全一致。对于一个长度为m的字符串，抹去字符的方案一共有m种，另外需要注意这里的抹去指的是用一个空值来填充这个位置而不是直接从字符串中删去。

为了得到O(mn)的算法，在这里就必须使用哈希表来储存所有这些抹去字符后的字符串。一种可行的做法是使用rk算法，也就是将字符串视为一个27进制的数，将其转化为10进制然后哈希。这里选择27的进制的理由是a到z占据了1到26，而0则需要留给被抹去字符代表的空值。

得到一个字符串的哈希值之后，就可以通过哈希表检测之前是否存在某个符合条件的字符串，若没有，则需要将当前的哈希值加入到哈希表中。

值得一提的是，如果哈希函数设计的比较简单，那么一旦出现哈希冲突就意味着答案错误，所以我在这里选择了两个值分别取模来计算哈希值，这样可以有效降低哈希冲突的风险。

关于rk算法的简单介绍可以参考之前的2156题，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 2156.查找给定哈希值的子串](https://zhuanlan.zhihu.com/p/531523744)

最后附上python代码：

```python
class Solution(object):
    def differByOne(self, dict):
        """
        :type dict: List[str]
        :rtype: bool
        """

        mod1 = 10**9 + 7
        mod2 = 2147483647

        pow1 = [1]
        pow2 = [1]

        m = len(dict)
        n = len(dict[0])

        for index in range(n):
            pow1.append(pow1[-1] * 27 % mod1)
            pow2.append(pow2[-1] * 27 % mod2)
        
        h = set()
        for word in dict:
            v1 = v2 = 0
            for index, char in enumerate(word):
                v1 = (v1 + (ord(char) - 96) * pow1[n - index - 1]) % mod1
                v2 = (v2 + (ord(char) - 96) * pow2[n - index - 1]) % mod2
            
            for index, char in enumerate(word):
                t1 = v1 - (ord(char) - 96) * pow1[n - index - 1] % mod1
                if t1 < 0:
                    t1 += mod1
                
                t2 = v2 - (ord(char) - 96) * pow2[n - index - 1] % mod2
                if t2 < 0:
                    t2 += mod2
                
                if (t1, t2) in h:
                    return True
                
                h.add((t1, t2))
        
        return False
```
