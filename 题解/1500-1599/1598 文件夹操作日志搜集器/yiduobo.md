---
title: "1598. 文件夹操作日志搜集器"
aliases: ["yiduobo的每日leetcode 1598.文件夹操作日志搜集器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432306994"
zhihu_id: "432306994"
zhihu_title: "yiduobo的每日leetcode 1598.文件夹操作日志搜集器"
question_id: "1598"
question: "文件夹操作日志搜集器"
problem_url: "https://leetcode.cn/problems/crawler-log-folder/"
created: "2021-11-12T19:29:02+08:00"
updated: "2021-11-12T19:29:02+08:00"
upvotes: 0
comments: 0
---

# 1598. 文件夹操作日志搜集器

> **[yiduobo的每日leetcode 1598.文件夹操作日志搜集器](https://zhuanlan.zhihu.com/p/432306994) · 知乎 · 2021-11-12 · 赞同 0**
> 力扣：[1598. 文件夹操作日志搜集器](https://leetcode.cn/problems/crawler-log-folder/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1598.文件夹操作日志搜集器

[力扣](https://leetcode-cn.com/problems/crawler-log-folder/)

题目看上去描述还蛮复杂的，但是仔细观察可以发现完全就是一个括号匹配问题。向下就相当于添加了一个左括号，而向上则相当于添加了一个右括号，于是只需要一趟扫描，按括号匹配的规则计算最终剩余的左括号数目即可。

需要注意的是，当某一时刻左括号的数目小于0，说明此时对应的是在根目录下执行向上操作，此时应该将左括号数目重置为0。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, logs):
        """
        :type logs: List[str]
        :rtype: int
        """

        now = 0
        for cmd in logs:
            if cmd == './':
                continue
            elif cmd == '../':
                now -= 1
                if now < 0:
                    now = 0
            else:
                now += 1
        
        return now
```
