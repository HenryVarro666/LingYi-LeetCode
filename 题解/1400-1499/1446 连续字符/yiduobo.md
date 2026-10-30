---
title: "1446. 连续字符"
aliases: ["yiduobo的每日leetcode 1446.连续字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/410816880"
zhihu_id: "410816880"
zhihu_title: "yiduobo的每日leetcode 1446.连续字符"
question_id: "1446"
question: "连续字符"
problem_url: "https://leetcode.cn/problems/consecutive-characters/"
created: "2021-09-15T23:48:02+08:00"
updated: "2021-09-15T23:48:02+08:00"
upvotes: 1
comments: 0
---

# 1446. 连续字符

> **[yiduobo的每日leetcode 1446.连续字符](https://zhuanlan.zhihu.com/p/410816880) · 知乎 · 2021-09-15 · 赞同 1**
> 力扣：[1446. 连续字符](https://leetcode.cn/problems/consecutive-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1446.连续字符

[力扣](https://leetcode-cn.com/problems/consecutive-characters/)

比较基础的题目。一趟扫描，若当前字符与前一个字符相同，那么将cnt加上1，否则使用cnt更新答案，并更新cnt为1。扫描完成后，还需要使用最后这个cnt更新答案，因为此时的cnt表示最后一段连续字符的长度。

最后附上python代码：

```python
class Solution(object):
    def maxPower(self, s):
        """
        :type s: str
        :rtype: int
        """

        now = None
        res = 0
        cnt = 0
        for char in s:
            if char != now:
                res = max(res, cnt)
                now = char
                cnt = 1
            else:
                cnt += 1
        
        return max(res, cnt)
```
