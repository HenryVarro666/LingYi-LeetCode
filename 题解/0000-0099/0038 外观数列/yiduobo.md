---
title: "38. 外观数列"
aliases: ["yiduobo的每日leetcode 38.外观数列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/121816725"
zhihu_id: "121816725"
zhihu_title: "yiduobo的每日leetcode 38.外观数列"
question_id: "38"
question: "外观数列"
problem_url: "https://leetcode.cn/problems/count-and-say/"
created: "2020-03-31T22:19:21+08:00"
updated: "2020-03-31T22:19:21+08:00"
upvotes: 0
comments: 0
---

# 38. 外观数列

> **[yiduobo的每日leetcode 38.外观数列](https://zhuanlan.zhihu.com/p/121816725) · 知乎 · 2020-03-31 · 赞同 0**
> 力扣：[38. 外观数列](https://leetcode.cn/problems/count-and-say/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

38.外观数列<https://leetcode-cn.com/problems/count-and-say/>

字符串模拟的题目，每次遍历当前的串，然后判断这一位是否与上一位相同：

(1)与上一位相同，则计数器加一。

(2)与上一位不同，那么将计数器与上一位加入到新串，并重置计数器。

个人感觉这个问题可能存在某种生成式的解法，但是目前没什么思路，先老老实实用模拟的方法解决。时间复杂度方面由于跟上一个串有关，因此不知道如何判断。

最后附上python代码：

```python
class Solution(object):
    def countAndSay(self, n):
        """
        :type n: int
        :rtype: str
        """

        f = ['', '1']

        for index in range(2, n + 1):
            now = None
            cnt = 0
            f.append('')
            for char in f[index - 1]:
                if now is None or now != char:
                    if cnt > 0:
                        f[index] += str(cnt) + now
                    now = char
                    cnt = 1
                else:
                    cnt += 1

            if cnt > 0:
                f[index] += str(cnt) + now
        return f[n]
```
