---
title: "2381. 字母移位II"
aliases: ["yiduobo的每日leetcode 2381.字母移位II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/564875613"
zhihu_id: "564875613"
zhihu_title: "yiduobo的每日leetcode 2381.字母移位II"
question_id: "2381"
question: "字母移位 II"
problem_url: "https://leetcode.cn/problems/shifting-letters-ii/"
difficulty: "Medium"
rating: 1793
created: "2022-09-16T00:15:39+08:00"
updated: "2022-09-16T00:15:39+08:00"
upvotes: 0
comments: 0
---

# 2381. 字母移位II

> **[yiduobo的每日leetcode 2381.字母移位II](https://zhuanlan.zhihu.com/p/564875613) · 知乎 · 2022-09-16 · 赞同 0**
> 力扣：[2381. 字母移位 II](https://leetcode.cn/problems/shifting-letters-ii/) · Medium · 灵茶山艾府：[差分（Python 简洁写法）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2381.字母移位II

[力扣](https://leetcode.cn/problems/shifting-letters-ii/)

题目相当于给出一个区间和若干操作，每次操作都会将某个子区间中的数都加上1或者减去1，问最终这个区间是什么样的。

由于是最后询问一次，因此在这里很适合使用差分数组来求解。具体来说，就是对于子区间[left, right]上的操作，可以将其拆分为在后缀区间[left, n]上的正向操作，以及在后缀区间[right + 1, n]上的负向操作，那么就可以令f[i]表示后缀区间[i, n]的操作情况，那么对于区间[left, right]的操作就可以用过更新f[left]和f[right + 1]来完成。全部操作完成后，遍历一趟f就可以得到区间上每个位置的最终情况了。

最后附上python代码：

```python
class Solution(object):
    def shiftingLetters(self, s, shifts):
        """
        :type s: str
        :type shifts: List[List[int]]
        :rtype: str
        """

        n = len(s)
        f = [0] * n
        for start, end, direction in shifts:
            if direction == 0:
                delta = -1
            else:
                delta = 1
            
            f[start] += delta
            if end + 1 < n:
                f[end + 1] -= delta

        res = []
        delta = 0
        for index in range(n):
            delta += f[index]
            now = ord(s[index]) - 97 + delta
            if now < 0:
                now = 26 - (-now) % 26
            now %= 26
            res.append(chr(now + 97))
        
        return ''.join(res)
```
