---
title: "2011. 执行操作后的变量值"
aliases: ["yiduobo的每日leetcode 2011.执行操作后的变量值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/504405086"
zhihu_id: "504405086"
zhihu_title: "yiduobo的每日leetcode 2011.执行操作后的变量值"
question_id: "2011"
question: "执行操作后的变量值"
problem_url: "https://leetcode.cn/problems/final-value-of-variable-after-performing-operations/"
difficulty: "Easy"
created: "2022-04-25T00:44:23+08:00"
updated: "2022-04-25T00:44:23+08:00"
upvotes: 0
comments: 0
---

# 2011. 执行操作后的变量值

> **[yiduobo的每日leetcode 2011.执行操作后的变量值](https://zhuanlan.zhihu.com/p/504405086) · 知乎 · 2022-04-25 · 赞同 0**
> 力扣：[2011. 执行操作后的变量值](https://leetcode.cn/problems/final-value-of-variable-after-performing-operations/) · Easy · 灵茶山艾府：[简单题，简单做。附其他趣味写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2011.执行操作后的变量值

[力扣](https://leetcode-cn.com/problems/final-value-of-variable-after-performing-operations/)

无论是前缀运算符还是后缀运算符，总是能够根据字符串正中间的这个字符判断出当前执行的是加操作还是减操作。那么只需要一趟遍历，根据正中间的字符判断当前的操作并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def finalValueAfterOperations(self, operations):
        """
        :type operations: List[str]
        :rtype: int
        """

        res = 0
        for op in operations:
            if op[1] == '-':
                res -= 1
            else:
                res += 1
        
        return res
```
