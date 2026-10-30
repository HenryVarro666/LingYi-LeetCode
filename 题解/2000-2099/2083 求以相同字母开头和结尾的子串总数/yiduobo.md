---
title: "2083. 求以相同字母开头和结尾的子串总数"
aliases: ["yiduobo的每日leetcode 2083.求以相同字母开头和结尾的子串总数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626090738"
zhihu_id: "626090738"
zhihu_title: "yiduobo的每日leetcode 2083.求以相同字母开头和结尾的子串总数"
question_id: "2083"
question: "求以相同字母开头和结尾的子串总数"
problem_url: "https://leetcode.cn/problems/substrings-that-begin-and-end-with-the-same-letter/"
created: "2023-05-01T06:06:09+08:00"
updated: "2023-05-01T06:06:09+08:00"
upvotes: 0
comments: 0
---

# 2083. 求以相同字母开头和结尾的子串总数

> **[yiduobo的每日leetcode 2083.求以相同字母开头和结尾的子串总数](https://zhuanlan.zhihu.com/p/626090738) · 知乎 · 2023-05-01 · 赞同 0**
> 力扣：[2083. 求以相同字母开头和结尾的子串总数](https://leetcode.cn/problems/substrings-that-begin-and-end-with-the-same-letter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2083.求以相同字母开头和结尾的子串总数

[力扣](https://leetcode.cn/problems/substrings-that-begin-and-end-with-the-same-letter/)

对于字符串中的某个字符s[index]而言，不妨设字符串中下标在0到index之间一共有k个字符与s[index]相同，那么以s[index]为结尾的合法子串就恰好有k个。

更进一步的，若整个字符串中有n个s[index]，那么以s[index]为两端的子串就一共有n \* (n +1) / 2个。

于是可以一趟遍历，使用哈希表记录每种字符出现的次数，然后使用上面的计算方式计算以每种字符为两端的子串的总数。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        res = 0
        for v in cnt.values():
            res += v * (v + 1) / 2
        
        return res
```
