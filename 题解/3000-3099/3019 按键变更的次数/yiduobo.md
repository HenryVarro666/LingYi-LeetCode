---
title: "3019. 按键变更的次数"
aliases: ["yiduobo的每日leetcode 3019.按键变更的次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694599756"
zhihu_id: "694599756"
zhihu_title: "yiduobo的每日leetcode 3019.按键变更的次数"
question_id: "3019"
question: "按键变更的次数"
problem_url: "https://leetcode.cn/problems/number-of-changing-keys/"
difficulty: "Easy"
created: "2024-04-26T01:23:45+08:00"
updated: "2024-04-26T01:23:45+08:00"
upvotes: 0
comments: 0
---

# 3019. 按键变更的次数

> **[yiduobo的每日leetcode 3019.按键变更的次数](https://zhuanlan.zhihu.com/p/694599756) · 知乎 · 2024-04-26 · 赞同 0**
> 力扣：[3019. 按键变更的次数](https://leetcode.cn/problems/number-of-changing-keys/) · Easy · 灵茶山艾府：[位运算简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3019.按键变更的次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-changing-keys/description/)

一趟遍历，检测相邻字符间的ascii码是否相等或者等于32，如果不是，则说明产生了变更，需要将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def countKeyChanges(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        res = 0
        for index in range(1, len(s)):
            diff = abs(ord(s[index]) - ord(s[index - 1]))
            if diff != 0 and diff != 32:
                res += 1
        
        return res
```
