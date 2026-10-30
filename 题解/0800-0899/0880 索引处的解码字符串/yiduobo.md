---
title: "880. 索引处的解码字符串"
aliases: ["yiduobo的每日leetcode 880.索引处的解码字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351094651"
zhihu_id: "351094651"
zhihu_title: "yiduobo的每日leetcode 880.索引处的解码字符串"
question_id: "880"
question: "索引处的解码字符串"
problem_url: "https://leetcode.cn/problems/decoded-string-at-index/"
created: "2021-02-17T18:18:15+08:00"
updated: "2021-02-17T18:18:15+08:00"
upvotes: 0
comments: 0
---

# 880. 索引处的解码字符串

> **[yiduobo的每日leetcode 880.索引处的解码字符串](https://zhuanlan.zhihu.com/p/351094651) · 知乎 · 2021-02-17 · 赞同 0**
> 力扣：[880. 索引处的解码字符串](https://leetcode.cn/problems/decoded-string-at-index/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

880.索引处的解码字符串

[力扣](https://leetcode-cn.com/problems/decoded-string-at-index/)

拿到题目之后很容易想到直接按题目规则扩展字符串直到其长度达到K，但是由于这里的K可能非常大，因此不能实打实地扩展字符串，否则时间和空间复杂度都承受不住。

既然不能实打实地扩展，那么就只能先计算其长度，具体做法为从头往后一趟扫描，若当期字符char为小写字母，那么长度l加1，否则l应该复制char - 1次，于是有l \*\= char。当某一时刻的l大于等于K时，记最后一个扩展的字符下标为last_pos。

接下来，可以从last_pos开始往前，反过来找答案：

1、若当前字符char为小写字母，且l等于K：

此时的char就是我们要找的答案，直接返回即可

2、若当前字符char为小写字母，且l大于K：

此时答案应该在char的前面，因此将l减去1，然后继续向前遍历

3、若当前字符char为数字：

此时的S由char之前的字符串S'复制char次得到，因此可以先将l除以char得到S'的长度l'。由于S是由S'复制char得到，因此S中的第K个字符就与S'中的第K % l'个字符一样，于是此时还需要将K对l'取模，然后继续向前遍历。

这里需要注意，若K % l'等于0，那么应当将K置为l'。

最后附上python代码：

```python
class Solution(object):
    def decodeAtIndex(self, S, K):
        """
        :type S: str
        :type K: int
        :rtype: str
        """

        l = 0
        last_pos = 0
        for index, char in enumerate(S):
            if char >= 'a' and char <= 'z':
                l += 1
            else:
                l *= int(char)
            if l >= K:
                last_pos = index
                break

        for index in range(last_pos, -1, -1):
            char = S[index]
            if char >= 'a' and char <= 'z':
                if l == K:
                    return char
                l -= 1
            else:
                l /= int(char)
                K %= l
                if K == 0:
                    K = l
```
