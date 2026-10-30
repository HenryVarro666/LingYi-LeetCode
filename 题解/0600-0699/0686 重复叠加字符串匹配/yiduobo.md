---
title: "686. 重复叠加字符串匹配"
aliases: ["yiduobo的每日leetcode 686.重复叠加字符串匹配"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/304631081"
zhihu_id: "304631081"
zhihu_title: "yiduobo的每日leetcode 686.重复叠加字符串匹配"
question_id: "686"
question: "重复叠加字符串匹配"
problem_url: "https://leetcode.cn/problems/repeated-string-match/"
created: "2020-11-21T18:08:00+08:00"
updated: "2020-11-21T18:08:00+08:00"
upvotes: 0
comments: 0
---

# 686. 重复叠加字符串匹配

> **[yiduobo的每日leetcode 686.重复叠加字符串匹配](https://zhuanlan.zhihu.com/p/304631081) · 知乎 · 2020-11-21 · 赞同 0**
> 力扣：[686. 重复叠加字符串匹配](https://leetcode.cn/problems/repeated-string-match/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

686.重复叠加字符串匹配

[力扣](https://leetcode-cn.com/problems/repeated-string-match/)

设a的长度为m，b的长度为n，那么如果a重复叠加之后b是a的子串，那么在叠加n / m + 2次之内就能形成匹配。其原理是当复制n / m + 1次之后，复制串a'的长度将大于b，此时再添加一个a串之后，那么a'中就能包含从a中任意字符开始的，长度为n的子串，若b是a'的子串，那么b必然属于其中之一。

于是直接将a复制n / m + 2次，然后执行kmp算法查找b第一次在复制串中出现的位置，最后通过匹配上的位置判断究竟需要复制多少次即可。

最后附上python代码：

```
class Solution(object):
    def repeatedStringMatch(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: int
        """

        m = len(a)
        n = len(b)

        k = n / m + 2
        tmp = a * k

        pos = 0
        f = [0]
        for index in range(1, n):
            while pos > 0 and b[pos] != b[index]:
                pos = f[pos - 1]
            if b[pos] == b[index]:
                pos += 1
            f.append(pos)

        pos = 0
        for index in range(m * k):
            while pos > 0 and b[pos] != tmp[index]:
                pos = f[pos - 1]
            if b[pos] == tmp[index]:
                pos += 1
            if pos == n:
                if index < m * (k - 2):
                    return k - 2
                elif index < m * (k - 1):
                    return k - 1
                else:
                    return k

        return -1
```
