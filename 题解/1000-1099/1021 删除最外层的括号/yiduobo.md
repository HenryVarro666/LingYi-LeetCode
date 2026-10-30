---
title: "1021. 删除最外层的括号"
aliases: ["yiduobo的每日leetcode 1021.删除最外层的括号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368645727"
zhihu_id: "368645727"
zhihu_title: "yiduobo的每日leetcode 1021.删除最外层的括号"
question_id: "1021"
question: "删除最外层的括号"
problem_url: "https://leetcode.cn/problems/remove-outermost-parentheses/"
created: "2021-04-28T21:59:07+08:00"
updated: "2021-04-28T21:59:07+08:00"
upvotes: 0
comments: 0
---

# 1021. 删除最外层的括号

> **[yiduobo的每日leetcode 1021.删除最外层的括号](https://zhuanlan.zhihu.com/p/368645727) · 知乎 · 2021-04-28 · 赞同 0**
> 力扣：[1021. 删除最外层的括号](https://leetcode.cn/problems/remove-outermost-parentheses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1021.删除最外层的括号

[力扣](https://leetcode-cn.com/problems/remove-outermost-parentheses/)

对于最外层括号，有一个性质是当处于在左括号之前以及右括号之后时，当前串中的左右括号正好是相等的。那么我们可以从头向后一趟扫描，使用一个变量cnt维护当前有多少尚未匹配的左括号。

当碰到一个左括号时，若此时的cnt等于0，说明该左括号就是最外层的左括号，否则我们就应该将其加入到答案当中。当然，我们还需要将cnt加上1。

当碰到一个右括号时，首先将cnt减去1，表示匹配上一个左括号。若此时的cnt等于0，说明当前括号就是匹配最外层左括号的最外层右括号，否则我们就应该将其加入到答案当中。

最后附上python代码：

```python
class Solution(object):
    def removeOuterParentheses(self, S):
        """
        :type S: str
        :rtype: str
        """

        res = []
        cnt = 0
        for char in S:
            if char == '(':
                if cnt > 0:
                    res.append(char)
                cnt += 1
            else:
                cnt -= 1
                if cnt > 0:
                    res.append(char)
        
        return ''.join(res)
```
