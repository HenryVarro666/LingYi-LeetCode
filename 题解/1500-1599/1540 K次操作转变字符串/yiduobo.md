---
title: "1540. K次操作转变字符串"
aliases: ["yiduobo的每日leetcode 1540.K次操作转变字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424239213"
zhihu_id: "424239213"
zhihu_title: "yiduobo的每日leetcode 1540.K次操作转变字符串"
question_id: "1540"
question: "K次操作转变字符串"
problem_url: "https://leetcode.cn/problems/can-convert-string-in-k-moves/"
created: "2021-10-22T18:58:51+08:00"
updated: "2021-10-22T18:58:51+08:00"
upvotes: 0
comments: 0
---

# 1540. K次操作转变字符串

> **[yiduobo的每日leetcode 1540.K次操作转变字符串](https://zhuanlan.zhihu.com/p/424239213) · 知乎 · 2021-10-22 · 赞同 0**
> 力扣：[1540. K次操作转变字符串](https://leetcode.cn/problems/can-convert-string-in-k-moves/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1540.K次操作转变字符串

[力扣](https://leetcode-cn.com/problems/can-convert-string-in-k-moves/)

由于题目每次只能替换一个字符，若其中存在n个需要切换m次的字符，那么这n个字符需要在第m次、m + 26次、m + 52次、...、m + (n - 1) \* 26次操作时进行转换，于是可以先统计所有字符转换需要的轮次，然后根据上面的计算方式得出最大需要的操作次数，对比其与k的大小即可。

最后附上python代码：

```python
class Solution(object):
    def canConvertString(self, s, t, k):
        """
        :type s: str
        :type t: str
        :type k: int
        :rtype: bool
        """
        
        if len(s) != len(t):
            return False

        cnt_list = [0] * 26
        n = len(s)
        for index in range(n):
            dis = ord(t[index]) - ord(s[index])
            if dis < 0:
                dis += 26
            
            cnt_list[dis] += 1
        
        res = 0
        for index in range(1, 26):
            if cnt_list[index] > 0:
                res = max(res, (cnt_list[index] - 1) * 26 + index)
        
        return res <= k
```
