---
title: "1614. 括号的最大嵌套深度"
aliases: ["yiduobo的每日leetcode 1614.括号的最大嵌套深度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435018232"
zhihu_id: "435018232"
zhihu_title: "yiduobo的每日leetcode 1614.括号的最大嵌套深度"
question_id: "1614"
question: "括号的最大嵌套深度"
problem_url: "https://leetcode.cn/problems/maximum-nesting-depth-of-the-parentheses/"
difficulty: "Easy"
rating: 1323
created: "2021-11-19T00:04:16+08:00"
updated: "2021-11-19T00:04:16+08:00"
upvotes: 0
comments: 0
---

# 1614. 括号的最大嵌套深度

> **[yiduobo的每日leetcode 1614.括号的最大嵌套深度](https://zhuanlan.zhihu.com/p/435018232) · 知乎 · 2021-11-19 · 赞同 0**
> 力扣：[1614. 括号的最大嵌套深度](https://leetcode.cn/problems/maximum-nesting-depth-of-the-parentheses/) · Easy · 灵茶山艾府：[格式化一下就能看得更清楚（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1614.括号的最大嵌套深度

[力扣](https://leetcode-cn.com/problems/maximum-nesting-depth-of-the-parentheses/)

比较基础的题目，由于题目保证了括号字符串是有效的，那么只需一趟扫描，记录当前敞开的左括号数目即可。

最后附上python代码：

```python
class Solution(object):
    def maxDepth(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = 0
        res = 0
        for char in s:
            if char == '(':
                cnt += 1
                res = max(res, cnt)
            elif char == ')':
                cnt -= 1
        
        return res
```
