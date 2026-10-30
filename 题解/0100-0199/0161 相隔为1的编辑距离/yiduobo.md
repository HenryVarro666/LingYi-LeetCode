---
title: "161. 相隔为1的编辑距离"
aliases: ["yiduobo的每日leetcode 161.相隔为1的编辑距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591081914"
zhihu_id: "591081914"
zhihu_title: "yiduobo的每日leetcode 161.相隔为1的编辑距离"
question_id: "161"
question: "相隔为1的编辑距离"
problem_url: "https://leetcode.cn/problems/one-edit-distance/"
created: "2022-12-12T00:23:20+08:00"
updated: "2022-12-12T00:23:20+08:00"
upvotes: 0
comments: 0
---

# 161. 相隔为1的编辑距离

> **[yiduobo的每日leetcode 161.相隔为1的编辑距离](https://zhuanlan.zhihu.com/p/591081914) · 知乎 · 2022-12-12 · 赞同 0**
> 力扣：[161. 相隔为1的编辑距离](https://leetcode.cn/problems/one-edit-distance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

161.相隔为1的编辑距离

[力扣](https://leetcode.cn/problems/one-edit-distance/)

首先考虑特殊情况。由于题目要求的是两个字符串的编辑距离恰好为1，那么若s和t完全相同，此时的答案应该为false。接下来，由于只能编辑一次，若s和t长度差的绝对值大于1，那么答案必然也是false。

处理完上面两种情况，接下来就需要按照长度差来决定如何判断两个字符串的编辑距离是否为1。

当两个字符串长度相等时，如果要使得编辑距离为1，那么s和t中就必须有且仅有一个位置上的字符不同，那么可以使用一个标记flag表示当前是否已经存在某个不同的位置，flag的初始值为false。接下来一趟遍历，若当前位置上的字符相同，那么直接跳过，若不同，那么需要检查当前flag的情况。若当前flag为false，那么就置flag为true，否则说明至少有两个位置的字符不同，此时直接返回false。

遍历完成后，若flag为false，说明两个字符串完全相同，这种情况也是不符合题目要求的，因为题目要求字符串的编辑距离为1，因此同样是返回false，否则返回true。

另一种情况，即两个字符串长度相差为1时，不妨先通过交换保证s是较长的字符串，t是较短的字符串，那么在这类就要求s中有某个字符是单独出现的，而其他字符与t中的字符逐一匹配。那么同样可以一趟遍历，使用一个标记flag表示当前s中是否已经有过单独出现的字符，同时使用一个变量p记录s中下一个参与匹配的字符。若当前位置上的t[index]与s[p]相同，那么就将p向后移动一位，若不同，那么需要检测当前flag的情况。若当前flag为false，那么就置flag为true，同时尝试使用s[p + 1]来匹配t[index]。若依然不能匹配，那么直接返回false。另一方面，若flag一开始已经为true了，那么同样是直接返回false。

遍历如果能顺利完成，那么就可以返回true了。

最后附上python代码：

```python
class Solution(object):
    def isOneEditDistance(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """

        length_diff = len(s) - len(t)
        if abs(length_diff) > 1:
            return False
        
        if length_diff == 0:
            flag = False
            for index in range(len(s)):
                if s[index] != t[index]:
                    if not flag:
                        flag = True
                    else:
                        return False
            
            return flag
        
        else:
            if length_diff < 0:
                s, t = t, s
            
            p = 0
            flag = False
            for index in range(len(t)):
                if t[index] != s[p]:
                    if not flag:
                        flag = True
                    else:
                        return False
                    
                    p += 1
                    if s[p] != t[index]:
                        return False
                
                p += 1
            
            return True
```
