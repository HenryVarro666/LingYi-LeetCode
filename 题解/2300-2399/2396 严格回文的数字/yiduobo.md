---
title: "2396. 严格回文的数字"
aliases: ["yiduobo的每日leetcode 2396.严格回文的数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/贪心算法", "题单/数学算法/七-杂项", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/566509720"
zhihu_id: "566509720"
zhihu_title: "yiduobo的每日leetcode 2396.严格回文的数字"
question_id: "2396"
question: "严格回文的数字"
problem_url: "https://leetcode.cn/problems/strictly-palindromic-number/"
difficulty: "Medium"
rating: 1329
created: "2022-09-20T23:24:45+08:00"
updated: "2022-09-20T23:24:45+08:00"
upvotes: 0
comments: 0
---

# 2396. 严格回文的数字

> **[yiduobo的每日leetcode 2396.严格回文的数字](https://zhuanlan.zhihu.com/p/566509720) · 知乎 · 2022-09-20 · 赞同 0**
> 力扣：[2396. 严格回文的数字](https://leetcode.cn/problems/strictly-palindromic-number/) · Medium · 灵茶山艾府：[数学证明](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2396.严格回文的数字

[力扣](https://leetcode.cn/problems/strictly-palindromic-number/)

乍一看以为是数学题，再一看数据规模感觉模拟也行，仔细一想发现原来是脑筋急转弯的题目。

题目中的n都大于等于4，那么对于4而言，只需要判断其2进制表示，为100，不是回文。

而对于大于4的任意n，如果将其转化为n - 2进制的话，最终表示必然是12，同样不是回文。

综合起来，答案必然为false。

最后附上python代码：

```python
class Solution(object):
    def isStrictlyPalindromic(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        return False
```
