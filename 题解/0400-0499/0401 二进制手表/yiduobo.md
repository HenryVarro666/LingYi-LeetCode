---
title: "401. 二进制手表"
aliases: ["yiduobo的每日leetcode 401.二进制手表"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/183261520"
zhihu_id: "183261520"
zhihu_title: "yiduobo的每日leetcode 401.二进制手表"
question_id: "401"
question: "二进制手表"
problem_url: "https://leetcode.cn/problems/binary-watch/"
difficulty: "Easy"
created: "2020-08-13T23:43:37+08:00"
updated: "2020-08-13T23:43:37+08:00"
upvotes: 0
comments: 0
---

# 401. 二进制手表

> **[yiduobo的每日leetcode 401.二进制手表](https://zhuanlan.zhihu.com/p/183261520) · 知乎 · 2020-08-13 · 赞同 0**
> 力扣：[401. 二进制手表](https://leetcode.cn/problems/binary-watch/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

401.二进制手表<https://leetcode-cn.com/problems/binary-watch/>

这里可以用dfs去做，不过我的做法是直接枚举可能的所有时间，然后反推出led的数目。

具体来说就是对于每个合法的hour或者minute，其二进制表示中1的数量即为led的数量，于是可以通过lowbit来逐个分离掉最低位进行统计。

最后附上python代码：

```python
class Solution(object):
    def readBinaryWatch(self, num):
        """
        :type num: int
        :rtype: List[str]
        """

        res = []
        for hour in range(12):
            hour_cnt = 0
            tmp = hour
            while tmp:
                tmp -= tmp & -tmp
                hour_cnt += 1
            if hour_cnt > num:
                continue
            for minute in range(60):
                minute_cnt = 0
                tmp = minute
                while tmp:
                    tmp -= tmp & - tmp
                    minute_cnt += 1
                if minute_cnt + hour_cnt == num:
                    res.append('%d:%02d' % (hour, minute))

        return res
```
