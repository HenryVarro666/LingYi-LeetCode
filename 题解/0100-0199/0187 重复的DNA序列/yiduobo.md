---
title: "187. 重复的DNA序列"
aliases: ["yiduobo的每日leetcode 187.重复的DNA序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145444766"
zhihu_id: "145444766"
zhihu_title: "yiduobo的每日leetcode 187.重复的DNA序列"
question_id: "187"
question: "重复的DNA序列"
problem_url: "https://leetcode.cn/problems/repeated-dna-sequences/"
created: "2020-06-02T23:42:54+08:00"
updated: "2020-06-02T23:42:54+08:00"
upvotes: 0
comments: 1
---

# 187. 重复的DNA序列

> **[yiduobo的每日leetcode 187.重复的DNA序列](https://zhuanlan.zhihu.com/p/145444766) · 知乎 · 2020-06-02 · 赞同 0**
> 力扣：[187. 重复的DNA序列](https://leetcode.cn/problems/repeated-dna-sequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

187.重复的DNA序列<https://leetcode-cn.com/problems/repeated-dna-sequences/>

题目要求找出所有长度为10的子序列中有哪些重复出现过，第一想法就是使用哈希表来做，不过考虑到DNA序列中只有ACGT四种字符，于是可以考虑使用4进制编码来提高效率。

具体为先设置A\=0，C\=1，G\=2，T\=3，先对序列中的前十个字符进行4进制编码。接下来从第十一个字符开始，每次加入一个字符，同时将头部的字符移除。这个过程相当于将之前的编码模上4的9次方，然后往左移一位，即乘上4，最后加上新加入字符的编码值。

具体原理为：

s[0 : 10]的编码为：

(1)、s[0] \* (4^9) + s[1] \* (4^8) + s[2] \* (4^7) + ... + s[9] \* (4^0)

而s[1 : 11]的编码为：

(2)、s[1] \* (4^9) + s[2] \* (4^8) + s[3] \* (4^7) + ... + s[10] \* (4^0)

可以发现，要从式1得到式2需要先去除s[0]相关的部分，这一步可以通过用式1的值模4的9次方解决。接下来剩余的

s[1] \* (4^8) + s[2] \* (4^7) + ... + s[9] \* (4^0)

要升级成

s[1] \* (4^9) + s[2] \* (4^8) + ... + s[9] \* (4^1)

于是需要将之前取模的结果乘上4，最后再加上s[10]的值就变成了式2了。

依次按上面的方法计算出所有的编码值并加入set，若某个编码值已经在set中，则将该子序列加入到答案的dict中即可。

实际上，这种编码的做法在解决字符串匹配的问题中也经常使用，是除了kmp之外另一种经典的算法，名为rk算法。当然在字符串匹配的场景中因为是26进制的编码，所以需要做一些哈希的操作来减小编码值。

最后附上python代码：

```python
class Solution(object):
    def findRepeatedDnaSequences(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        if len(s) <= 10:
            return []

        val_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        now = 0
        for char in s[:10]:
            now = now * 4 + val_dict[char]

        check_set = set()
        check_set.add(now)

        res_dict = {}

        for index, char in enumerate(s[10:]):
            now = now % 262144 * 4 + val_dict[char]
            if now in check_set:
                res_dict[now] = s[index + 1 : index + 11]
            else:
                check_set.add(now)

        return res_dict.values()
```
