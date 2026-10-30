---
title: "13. 罗马数字转整数"
aliases: ["yiduobo的每日leetcode 13.罗马数字转整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/string", "题单/常用数据结构", "题单/面试经典-150-题", "题单/常用数据结构/编程能力强化训练", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/114550099"
zhihu_id: "114550099"
zhihu_title: "yiduobo的每日leetcode 13.罗马数字转整数"
question_id: "13"
question: "罗马数字转整数"
problem_url: "https://leetcode.cn/problems/roman-to-integer/"
difficulty: "Easy"
created: "2020-03-19T21:48:45+08:00"
updated: "2020-03-19T21:48:45+08:00"
upvotes: 0
comments: 0
---

# 13. 罗马数字转整数

> **[yiduobo的每日leetcode 13.罗马数字转整数](https://zhuanlan.zhihu.com/p/114550099) · 知乎 · 2020-03-19 · 赞同 0**
> 力扣：[13. 罗马数字转整数](https://leetcode.cn/problems/roman-to-integer/) · Easy · 灵茶山艾府：[简单题就有简单写法！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

13.罗马数字转整数<https://leetcode-cn.com/problems/roman-to-integer/>

这个题目主要是要考虑 单位一加单位五 以及 单位一加单位十 这两种特殊情况。

当我们从左往右按位累加的时候，如果出现了一个单位五，且前面是一个单位一，那么这里应该算做单位四。但是先前已经累加过一次单位一了，所以这里继续累加一个单位三即可。同理，如果是单位十前面碰上单位一，那么累加一个单位八即可。

例如，MCMXCIV

首先累加M \= 1000， ans \= 1000

接下来累加C \= 100， ans \= 1100

接下来发现第二个M之前是C，即单位十(M\=1000)前面是单位一(C\=100)，那么这里不应该加上1000，而是加上800，此时ans \= 1900

接下来X \= 10，ans \= 1910

加下来发现第二个C之前是X，这里依然是单位十前面有单位一，所以这里不应该加上100，而是加上80，此时ans \= 1990

接下来I \= 1，ans \= 1991

最后V前面接的是I，即单位五前面有单位一，所以这里不应该加5，而是加3，所以最后ans \= 1994

最后附上python代码：

```python
class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        for index, char in enumerate(s):
            if char == 'I':
                res += 1
            elif char == 'V':
                if index > 0 and s[index - 1] == 'I':
                    res += 3
                else:
                    res += 5
            elif char == 'X':
                if index > 0 and s[index - 1] == 'I':
                    res += 8
                else:
                    res += 10
            elif char == 'L':
                if index > 0 and s[index - 1] == 'X':
                    res += 30
                else:
                    res += 50
            elif char == 'C':
                if index > 0 and s[index - 1] == 'X':
                    res += 80
                else:
                    res += 100
            elif char == 'D':
                if index > 0 and s[index - 1] == 'C':
                    res += 300
                else:
                    res += 500
            else:
                if index > 0 and s[index - 1] == 'C':
                    res += 800
                else:
                    res += 1000
        
        return res
```
