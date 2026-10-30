---
title: "1374. 生成每种字符都是奇数个的字符串"
aliases: ["yiduobo的每日leetcode 1374.生成每种字符都是奇数个的字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/401222191"
zhihu_id: "401222191"
zhihu_title: "yiduobo的每日leetcode 1374.生成每种字符都是奇数个的字符串"
question_id: "1374"
question: "生成每种字符都是奇数个的字符串"
problem_url: "https://leetcode.cn/problems/generate-a-string-with-characters-that-have-odd-counts/"
created: "2021-08-18T22:15:48+08:00"
updated: "2021-08-18T22:15:48+08:00"
upvotes: 0
comments: 0
---

# 1374. 生成每种字符都是奇数个的字符串

> **[yiduobo的每日leetcode 1374.生成每种字符都是奇数个的字符串](https://zhuanlan.zhihu.com/p/401222191) · 知乎 · 2021-08-18 · 赞同 0**
> 力扣：[1374. 生成每种字符都是奇数个的字符串](https://leetcode.cn/problems/generate-a-string-with-characters-that-have-odd-counts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1374.生成每种字符都是奇数个的字符串

[力扣](https://leetcode-cn.com/problems/generate-a-string-with-characters-that-have-odd-counts/)

比较基础的题目。若n为奇数，那么n个'a'就是一个合法答案。若n为偶数，那么n - 1必然为奇数，因此n - 1个'a'加上一个'b'就是一个合法答案。

最后附上python代码：

```python
class Solution(object):
    def generateTheString(self, n):
        """
        :type n: int
        :rtype: str
        """

        res = ['a'] * n
        if n % 2 == 0:
            res[-1] = 'b'
        
        return ''.join(res)
```
