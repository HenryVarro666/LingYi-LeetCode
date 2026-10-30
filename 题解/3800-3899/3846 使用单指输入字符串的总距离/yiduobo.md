---
title: "3846. 使用单指输入字符串的总距离"
aliases: ["yiduobo的每日leetcode 3846.使用单指输入字符串的总距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011481473522374355"
zhihu_id: "2011481473522374355"
zhihu_title: "yiduobo的每日leetcode 3846.使用单指输入字符串的总距离"
question_id: "3846"
question: "使用单指输入字符串的总距离"
problem_url: "https://leetcode.cn/problems/total-distance-to-type-a-string-using-one-finger/"
created: "2026-03-01T16:47:38+08:00"
updated: "2026-03-01T16:47:38+08:00"
upvotes: 1
comments: 0
---

# 3846. 使用单指输入字符串的总距离

> **[yiduobo的每日leetcode 3846.使用单指输入字符串的总距离](https://zhuanlan.zhihu.com/p/2011481473522374355) · 知乎 · 2026-03-01 · 赞同 1**
> 力扣：[3846. 使用单指输入字符串的总距离](https://leetcode.cn/problems/total-distance-to-type-a-string-using-one-finger/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3846.使用单指输入字符串的总距离

<https://leetcode.cn/problems/total-distance-to-type-a-string-using-one-finger/description/>

题目给出一个常规的键盘，其中字符按键按一下矩形网格排列：

| q | w | e | r | t | y | u | i | o | p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a | s | d | f | g | h | j | k | l |  |
| z | x | c | v | b | n | m |  |  |  |

另外给出一个只包含小写字符的字符串s。要求计算仅使用一个手指输入字符串s的总移动距离。初始状态下，手指处于字母键'a'上。

两个位于(r1, c1)和(r2, c2)的按键距离为abs(r1 - r2) + abs(c1 - c2)。

直接模拟输入过程，记录当前目标字符位置与手指位置间的距离，累加到答案后将手指位置更新为当前目标字符的位置即可。

具体实现上，可以先构造处这个矩形网格['qwertyuiop'、'asdfghjkl'、'zxcvbnm']，然后遍历其中的字符，利用哈希表建立起每种字符到下标位置的映射，接下来再按照上面描述的算法遍历并计算答案即可。

最后附上python代码：

```python
class Solution(object):
    def totalDistance(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        key = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        x = {}
        y = {}

        for i, w in enumerate(key):
            for j, c in enumerate(w):
                x[c] = i
                y[c] = j
        
        res = 0
        nowx, nowy = 1, 0
        for c in s:
            res += abs(x[c] - nowx) + abs(y[c] - nowy)
            nowx, nowy = x[c], y[c]
        
        return res
```
