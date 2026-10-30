---
title: "1156. 单字符重复子串的最大长度"
aliases: ["yiduobo的每日leetcode 1156.单字符重复子串的最大长度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378154454"
zhihu_id: "378154454"
zhihu_title: "yiduobo的每日leetcode 1156.单字符重复子串的最大长度"
question_id: "1156"
question: "单字符重复子串的最大长度"
problem_url: "https://leetcode.cn/problems/swap-for-longest-repeated-character-substring/"
created: "2021-06-05T15:18:12+08:00"
updated: "2021-06-05T15:18:12+08:00"
upvotes: 0
comments: 0
---

# 1156. 单字符重复子串的最大长度

> **[yiduobo的每日leetcode 1156.单字符重复子串的最大长度](https://zhuanlan.zhihu.com/p/378154454) · 知乎 · 2021-06-05 · 赞同 0**
> 力扣：[1156. 单字符重复子串的最大长度](https://leetcode.cn/problems/swap-for-longest-repeated-character-substring/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1156.单字符重复子串的最大长度

[力扣](https://leetcode-cn.com/problems/swap-for-longest-repeated-character-substring/)

题目可以交换一次字符，那么这里有两种使用方法：

1、对于形如AAAAAB的子串，我们从远处弄一个A来与这里的B交换，那么此时可以得到一个长度为原始子串中A的数值再加上1的字符串。当然这里需要存在一个远处的A来与B进行交换，在这里也可以对比交换后新串的长度与整个字符串中A的数目来判断是否存在远处的A。

2、对于形如AAAABAAAAA的子串，同样是从远处弄一个A来与这里的B交换，那么此时可以得到一个长度为两段A的长度之和再加上1的字符串。类似地，这里也需要一个远处的A来与B进行交换，否则就只能用使用头部或者尾部的A来交换，变成BAAAAAAAAA或者AAAAAAAAAB。同样这里也可以对比交换后新串的长度与整个字符串中A的数目来判断是否存在远处的A。

根据以上两点，我们可以先通过一趟扫描，计算出原始串中各个连续子串的长度，并将其组织成[char, l]的形式，其中char表示当前连续子串中的字符是什么，l表示其长度。接下来枚举每一个连续子串。对于当前连续子串index：

1、根据使用方法1，那么此时可以用min(l[index] + 1， tot(char[index]))来更新答案。其中tot(char)表示原始字符串中char的数目，这个可以在先前扫描的时候计算出来。

2、根据使用方法2，若此时的l[index - 1]等于1，且char[index - 2]等于char[index]，那么我们就可以用min(l[index] + l[index - 2] + 1, tot(char[index]))来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxRepOpt1(self, text):
        """
        :type text: str
        :rtype: int
        """

        s = {}
        now = text[0]
        cnt = 1
        part = []
        for char in text[1:]:
            if char != now:
                part.append([now, cnt])
                s[now] = s.get(now, 0) + cnt
                now = char
                cnt = 1
            else:
                cnt += 1
        
        part.append([now, cnt])
        s[now] = s.get(now, 0) + cnt
        
        res = 0
        for index in range(len(part)):
            tmp = part[index][1] + 1
            if index >= 2 and part[index - 1][1] == 1 and part[index - 2][0] == part[index][0]:
                tmp += part[index - 2][1]
            
            res = max(res, min(tmp, s[part[index][0]]))
        
        return res
```
