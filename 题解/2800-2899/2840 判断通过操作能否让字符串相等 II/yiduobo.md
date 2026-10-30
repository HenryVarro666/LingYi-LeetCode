---
title: "2840. 判断通过操作能否让字符串相等II"
aliases: ["yiduobo的每日leetcode 2840.判断通过操作能否让字符串相等II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659687671"
zhihu_id: "659687671"
zhihu_title: "yiduobo的每日leetcode 2840.判断通过操作能否让字符串相等II"
question_id: "2840"
question: "判断通过操作能否让字符串相等 II"
problem_url: "https://leetcode.cn/problems/check-if-strings-can-be-made-equal-with-operations-ii/"
difficulty: "Medium"
rating: 1486
created: "2023-10-06T03:03:42+08:00"
updated: "2023-10-06T03:03:42+08:00"
upvotes: 1
comments: 1
---

# 2840. 判断通过操作能否让字符串相等II

> **[yiduobo的每日leetcode 2840.判断通过操作能否让字符串相等II](https://zhuanlan.zhihu.com/p/659687671) · 知乎 · 2023-10-06 · 赞同 1**
> 力扣：[2840. 判断通过操作能否让字符串相等 II](https://leetcode.cn/problems/check-if-strings-can-be-made-equal-with-operations-ii/) · Medium · 灵茶山艾府：[看下标为偶数/奇数的字符个数是否都一样（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2840.判断通过操作能否让字符串相等II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/check-if-strings-can-be-made-equal-with-operations-ii/)

上一题的加强版，本题中可以执行操作的下标对必须是同奇偶的，那么做法就顺势变成了按照奇偶将两个字符串都分成两个部分，然后比较这两个部分中每个字符出现的次数是否相同。具体实现上则可以利用哈希表分别记录奇偶下标中每种字符出现的次数然后进行比较。

最后附上python代码：

```python
class Solution(object):
    def checkStrings(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        cnt = [[0] * 26 for _ in range(2)]

        for index, char in enumerate(s1):
            cnt[index % 2][ord(char) - 97] += 1
        
        for index, char in enumerate(s2):
            cnt[index % 2][ord(char) - 97] -= 1
            if cnt[index % 2][ord(char) - 97] < 0:
                return False
        
        return True
```
