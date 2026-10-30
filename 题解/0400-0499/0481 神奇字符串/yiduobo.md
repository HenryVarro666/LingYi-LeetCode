---
title: "481. 神奇字符串"
aliases: ["yiduobo的每日leetcode 481.神奇字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/simulation", "leetcode/dong-hua", "leetcode/gou-zao"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/246302300"
zhihu_id: "246302300"
zhihu_title: "yiduobo的每日leetcode 481.神奇字符串"
question_id: "481"
question: "神奇字符串"
problem_url: "https://leetcode.cn/problems/magical-string/"
difficulty: "Medium"
created: "2020-09-15T21:27:42+08:00"
updated: "2020-09-15T21:27:42+08:00"
upvotes: 0
comments: 0
---

# 481. 神奇字符串

> **[yiduobo的每日leetcode 481.神奇字符串](https://zhuanlan.zhihu.com/p/246302300) · 知乎 · 2020-09-15 · 赞同 0**
> 力扣：[481. 神奇字符串](https://leetcode.cn/problems/magical-string/) · Medium · 灵茶山艾府：[一个动画秒懂本题+简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

481.神奇字符串<https://leetcode-cn.com/problems/magical-string/>

直接按题目要求模拟。每次往字符串尾部添加与当前尾部不同的数字，同时根据字符串头部指针指向的数确定添加的数量，同时更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def magicalString(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n <= 0:
            return 0

        q = [1]
        pos = 0
        res = 1
        while len(q) < n:
            q.append(3 - q[-1])
            res += 2 - q[-1]
            pos += 1
            now = q[pos]
            if now == 2 and len(q) < n:
                q.append(q[-1])
                res += 2 - q[-1]

        return res
```
