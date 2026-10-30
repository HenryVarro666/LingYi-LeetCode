---
title: "1903. 字符串中的最大奇数"
aliases: ["yiduobo的每日leetcode 1903.字符串中的最大奇数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/brainteaser", "leetcode/string", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/480990758"
zhihu_id: "480990758"
zhihu_title: "yiduobo的每日leetcode 1903.字符串中的最大奇数"
question_id: "1903"
question: "字符串中的最大奇数"
problem_url: "https://leetcode.cn/problems/largest-odd-number-in-string/"
difficulty: "Easy"
rating: 1249
created: "2022-03-14T22:18:32+08:00"
updated: "2022-03-14T22:18:33+08:00"
upvotes: 0
comments: 0
---

# 1903. 字符串中的最大奇数

> **[yiduobo的每日leetcode 1903.字符串中的最大奇数](https://zhuanlan.zhihu.com/p/480990758) · 知乎 · 2022-03-14 · 赞同 0**
> 力扣：[1903. 字符串中的最大奇数](https://leetcode.cn/problems/largest-odd-number-in-string/) · Easy · 灵茶山艾府：[找最后一个奇数位置（附一行写法）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1903.字符串中的最大奇数

[力扣](https://leetcode-cn.com/problems/largest-odd-number-in-string/)

为了使得最终结果最大，那么就需要位数尽可能多。由于一个奇数的最低位必然也是奇数，只需要从后向前找到字符串中的最后一个奇数所在的位置p，那么字符串的前缀s[:p + 1]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def largestOddNumber(self, num):
        """
        :type num: str
        :rtype: str
        """

        n = len(num)
        p = n
        for index in range(n - 1, -1, -1):
            if int(num[index]) % 2 == 1:
                p = index
                break
        
        if p == n:
            return ''
        else:
            return num[:p + 1]
```
