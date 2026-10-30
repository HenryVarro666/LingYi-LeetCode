---
title: "2546. 执行逐位运算使字符串相等"
aliases: ["yiduobo的每日leetcode 2546.执行逐位运算使字符串相等"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637874046"
zhihu_id: "637874046"
zhihu_title: "yiduobo的每日leetcode 2546.执行逐位运算使字符串相等"
question_id: "2546"
question: "执行逐位运算使字符串相等"
problem_url: "https://leetcode.cn/problems/apply-bitwise-operations-to-make-strings-equal/"
difficulty: "Medium"
rating: 1605
created: "2023-06-21T21:55:50+08:00"
updated: "2023-06-21T21:55:50+08:00"
upvotes: 0
comments: 0
---

# 2546. 执行逐位运算使字符串相等

> **[yiduobo的每日leetcode 2546.执行逐位运算使字符串相等](https://zhuanlan.zhihu.com/p/637874046) · 知乎 · 2023-06-21 · 赞同 0**
> 力扣：[2546. 执行逐位运算使字符串相等](https://leetcode.cn/problems/apply-bitwise-operations-to-make-strings-equal/) · Medium · 灵茶山艾府：[脑筋急转弯+一行代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2546.执行逐位运算使字符串相等

[力扣](https://leetcode.cn/problems/apply-bitwise-operations-to-make-strings-equal/)

观察题目中给出的操作，如果是两个0参与运算，那么结果依然是两个0；如果是0和1参与运算，那么结果则是两个1；如果是两个1参与运算，那么结果是1和0。

可以发现，只要s中存在1，那么就可以将s变为任意包含至少一个1的字符串，但无法变为全0的字符串。反过来，若s是全0构成的字符串，那么s最终也只能是全0构成的字符串。

换言之，若s和target中都包含至少一个1，或者s和target都是全0，那么就有变换的方案，否则就没有。

最后附上python代码：

```python
class Solution(object):
    def makeStringsEqual(self, s, target):
        """
        :type s: str
        :type target: str
        :rtype: bool
        """

        flag_s = False
        for char in s:
            if char == '1':
                flag_s = True
                break
        
        flag_target = False
        for char in target:
            if char == '1':
                flag_target = True
                break
        
        return flag_s == flag_target
```
