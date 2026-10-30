---
title: "396. 旋转函数"
aliases: ["yiduobo的每日leetcode 396.旋转函数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/179301731"
zhihu_id: "179301731"
zhihu_title: "yiduobo的每日leetcode 396.旋转函数"
question_id: "396"
question: "旋转函数"
problem_url: "https://leetcode.cn/problems/rotate-function/"
difficulty: "Medium"
created: "2020-08-10T23:36:10+08:00"
updated: "2020-08-10T23:36:10+08:00"
upvotes: 0
comments: 0
---

# 396. 旋转函数

> **[yiduobo的每日leetcode 396.旋转函数](https://zhuanlan.zhihu.com/p/179301731) · 知乎 · 2020-08-10 · 赞同 0**
> 力扣：[396. 旋转函数](https://leetcode.cn/problems/rotate-function/) · Medium · 灵茶山艾府：[增量法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

396.旋转函数<https://leetcode-cn.com/problems/rotate-function/>

找规律的题目。以样例说明：

1、对于f[0]，有f[0] \= 0 \* A[0] + 1 \* A[1] + 2 \* A[2] + 3 \* A[3]

2、对于f[1]，有f[1] \= 0 \* A[3] + 1 \* A[0] + 2 \* A[1] + 3 \* A[2]

如果我们将其调换顺序，按照A来排好，那么就是

f[1] \= 1 \* A[0] + 2 \* A[1] + 3 \* A[2] + 0 \* A[3]

那么此时用f[1]减去f[0]，就有

f[1] - f[0] \= (1-0) \* A[0] + (2-1) \* A[1] + (3-2) \* A[2] + (0-3) \* A[3]

对于最后一项(0-3) \* A[3]，我们可以看做

(4 - 4 - 3) \* A[3] \= (4-3) \* A[3] - 4 \* A[3]

于是最后就有

f[1] - f[0] \= sum(A) - 4 \* A[3]

3、对于f[2]，我们将其与f[1]相减，用同样的处理方法可以得到

f[2] - [1] \= sum(A) - 4 \* A[2]

更一般地，对于f[index]，其中index > 0，我们将其与f[index - 1]相减，可以得到

f[index] - f[index - 1] \= sum(A) - len(A) \* A[len(A) - index]

到了这里，我们就可以在O(n)的时间内逐个递推出所有的f，其中的最大值即为答案。

最后附上python代码：

```python
class Solution(object):
    def maxRotateFunction(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        now = 0
        s = 0
        for index, num in enumerate(A):
            now += index * num
            s += num

        res = now
        for index in range(1, len(A)):
            now += s - len(A) * A[len(A) - index]
            res = max(now, res)

        return res
```
