---
title: "2299. 强密码检测器II"
aliases: ["yiduobo的每日leetcode 2299.强密码检测器II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/554167497"
zhihu_id: "554167497"
zhihu_title: "yiduobo的每日leetcode 2299.强密码检测器II"
question_id: "2299"
question: "强密码检验器 II"
problem_url: "https://leetcode.cn/problems/strong-password-checker-ii/"
difficulty: "Easy"
created: "2022-08-16T00:24:55+08:00"
updated: "2022-08-16T00:24:55+08:00"
upvotes: 0
comments: 0
---

# 2299. 强密码检测器II

> **[yiduobo的每日leetcode 2299.强密码检测器II](https://zhuanlan.zhihu.com/p/554167497) · 知乎 · 2022-08-16 · 赞同 0**
> 力扣：[2299. 强密码检验器 II](https://leetcode.cn/problems/strong-password-checker-ii/) · Easy · 灵茶山艾府：[利用位运算简化代码](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2299.强密码检测器II

[力扣](https://leetcode.cn/problems/strong-password-checker-ii/)

首先判断密码长度是否达标，接下来一趟遍历，判断是否出现每种需要出现的字符，同时判断每个字符是否与上一个字符不同就行了。

最后附上python代码：

```python
class Solution(object):
    def strongPasswordCheckerII(self, password):
        """
        :type password: str
        :rtype: bool
        """

        if len(password) < 8:
            return False
        
        spe_set = set(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+'])

        up_flag = down_flag = digit_flag = spe_flag = False
        for index, char in enumerate(password):
            if 'a' <= char <= 'z':
                down_flag = True
            elif 'A' <= char <= 'Z':
                up_flag = True
            elif '0' <= char <= '9':
                digit_flag = True
            elif char in spe_set:
                spe_flag = True

            if index > 0 and char == password[index - 1]:
                return False

        return up_flag and down_flag and digit_flag and spe_flag
```
