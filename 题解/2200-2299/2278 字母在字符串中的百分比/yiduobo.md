---
title: "2278. 字母在字符串中的百分比"
aliases: ["yiduobo的每日leetcode 2278.字母在字符串中的百分比"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550865706"
zhihu_id: "550865706"
zhihu_title: "yiduobo的每日leetcode 2278.字母在字符串中的百分比"
question_id: "2278"
question: "字母在字符串中的百分比"
problem_url: "https://leetcode.cn/problems/percentage-of-letter-in-string/"
difficulty: "Easy"
created: "2022-08-07T15:38:45+08:00"
updated: "2022-08-07T15:38:45+08:00"
upvotes: 0
comments: 0
---

# 2278. 字母在字符串中的百分比

> **[yiduobo的每日leetcode 2278.字母在字符串中的百分比](https://zhuanlan.zhihu.com/p/550865706) · 知乎 · 2022-08-07 · 赞同 0**
> 力扣：[2278. 字母在字符串中的百分比](https://leetcode.cn/problems/percentage-of-letter-in-string/) · Easy · 灵茶山艾府：[库函数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2278.字母在字符串中的百分比

[力扣](https://leetcode.cn/problems/percentage-of-letter-in-string/)

一趟遍历统计指定字母出现的次数，然后乘以100后除以字符串的长度就是百分比了。

最后附上python代码：

```python
class Solution(object):
    def percentageLetter(self, s, letter):
        """
        :type s: str
        :type letter: str
        :rtype: int
        """

        cnt = 0
        for char in s:
            if char == letter:
                cnt += 1
        
        return cnt * 100 / len(s)
```
