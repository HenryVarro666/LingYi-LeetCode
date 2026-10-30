---
title: "423. 从英文中重建数字"
aliases: ["yiduobo的每日leetcode 423.从英文中重建数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/194341402"
zhihu_id: "194341402"
zhihu_title: "yiduobo的每日leetcode 423.从英文中重建数字"
question_id: "423"
question: "从英文中重建数字"
problem_url: "https://leetcode.cn/problems/reconstruct-original-digits-from-english/"
created: "2020-08-22T20:58:16+08:00"
updated: "2020-08-22T20:58:16+08:00"
upvotes: 0
comments: 0
---

# 423. 从英文中重建数字

> **[yiduobo的每日leetcode 423.从英文中重建数字](https://zhuanlan.zhihu.com/p/194341402) · 知乎 · 2020-08-22 · 赞同 0**
> 力扣：[423. 从英文中重建数字](https://leetcode.cn/problems/reconstruct-original-digits-from-english/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

423.从英文中重建数字<https://leetcode-cn.com/problems/reconstruct-original-digits-from-english/>

注意到0-9这些数字的英文单词中，某些单词具体独一无二的字母，例如zero的z和two的w。于是可以首先通过统计这些字母的个数来求出对应单词出现的次数，然后再根据剩下的字母来确定其他的单词。

最后附上python代码：

```python
class Solution(object):
    def originalDigits(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_cnt = {}
        for char in s:
            char_cnt[char] = char_cnt.get(char, 0) + 1

        cnt = [0] * 10

        cnt[0] = self.check(char_cnt, 'z', 'zero')
        cnt[2] = self.check(char_cnt, 'w', 'two')
        cnt[4] = self.check(char_cnt, 'u', 'four')
        cnt[3] = self.check(char_cnt, 'r', 'three')
        cnt[1] = self.check(char_cnt, 'o', 'one')
        cnt[5] = self.check(char_cnt, 'f', 'five')
        cnt[6] = self.check(char_cnt, 'x', 'six')
        cnt[7] = self.check(char_cnt, 's', 'seven')
        cnt[8] = self.check(char_cnt, 'h', 'eight')
        cnt[9] = self.check(char_cnt, 'i', 'nine')
        
        res = ''.join([str(x) * cnt[x] for x in range(10)])
        return res

    def check(self, char_cnt, char, num):
        cnt = char_cnt.get(char, 0)
        if cnt > 0:
            for char in num:
                char_cnt[char] -= cnt

        return cnt
```
