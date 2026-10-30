---
title: "1221. 分割平衡字符串"
aliases: ["yiduobo的每日leetcode 1221.分割平衡字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/383403201"
zhihu_id: "383403201"
zhihu_title: "yiduobo的每日leetcode 1221.分割平衡字符串"
question_id: "1221"
question: "分割平衡字符串"
problem_url: "https://leetcode.cn/problems/split-a-string-in-balanced-strings/"
created: "2021-06-23T23:46:12+08:00"
updated: "2021-06-23T23:46:12+08:00"
upvotes: 0
comments: 0
---

# 1221. 分割平衡字符串

> **[yiduobo的每日leetcode 1221.分割平衡字符串](https://zhuanlan.zhihu.com/p/383403201) · 知乎 · 2021-06-23 · 赞同 0**
> 力扣：[1221. 分割平衡字符串](https://leetcode.cn/problems/split-a-string-in-balanced-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1221.分割平衡字符串

[力扣](https://leetcode-cn.com/problems/split-a-string-in-balanced-strings/)

比较基础的题目。从头开始一趟扫描，使用一个变量cnt统计当前字符串中l和r的差值。若当前字符为L，则将cnt加上1，若当前字符为R，则将cnt减去1。若某一时刻cnt等于，说明此时出现了一个平衡字符串，因此要答案加上1。

最后附上python代码：

```python
class Solution(object):
    def balancedStringSplit(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = 0
        res = 0
        for char in s:
            if char == 'L':
                cnt += 1
            else:
                cnt -= 1
            if cnt == 0:
                res += 1
            
        return res
```
