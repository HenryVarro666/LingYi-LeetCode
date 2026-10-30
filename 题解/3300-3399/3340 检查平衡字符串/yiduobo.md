---
title: "3340. 检查平衡字符串"
aliases: ["yiduobo的每日leetcode 3340.检查平衡字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25465406573"
zhihu_id: "25465406573"
zhihu_title: "yiduobo的每日leetcode 3340.检查平衡字符串"
question_id: "3340"
question: "检查平衡字符串"
problem_url: "https://leetcode.cn/problems/check-balanced-string/"
difficulty: "Easy"
created: "2025-02-21T23:53:13+08:00"
updated: "2025-02-21T23:53:13+08:00"
upvotes: 2
comments: 0
---

# 3340. 检查平衡字符串

> **[yiduobo的每日leetcode 3340.检查平衡字符串](https://zhuanlan.zhihu.com/p/25465406573) · 知乎 · 2025-02-21 · 赞同 2**
> 力扣：[3340. 检查平衡字符串](https://leetcode.cn/problems/check-balanced-string/) · Easy · 灵茶山艾府：[遍历求和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3340.检查平衡字符串

[3340. 检查平衡字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/check-balanced-string/description/)

题目给出一个仅由数字0到9构成的字符串num，若字符串中偶数下标的数字之和与奇数下标的数字之和相等，就认为这个字符串是平衡字符串。问num是否为平衡字符串。

比较基础的题目，直接一趟遍历，根据下标的奇偶性计算更新奇偶下标数字之和的差值即可。

最后附上python代码：

```python
class Solution(object):
    def isBalanced(self, num):
        """
        :type num: str
        :rtype: bool
        """

        diff = 0
        for index, c in enumerate(num):
            if index % 2 == 0:
                diff += int(c)
            else:
                diff -= int(c)
        
        return diff == 0
```
