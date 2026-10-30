---
title: "3106. 满足距离约束且字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 3106.满足距离约束且字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700394920"
zhihu_id: "700394920"
zhihu_title: "yiduobo的每日leetcode 3106.满足距离约束且字典序最小的字符串"
question_id: "3106"
question: "满足距离约束且字典序最小的字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-operations-with-constraint/"
difficulty: "Medium"
rating: 1515
created: "2024-05-29T00:18:52+08:00"
updated: "2024-05-29T00:18:52+08:00"
upvotes: 0
comments: 0
---

# 3106. 满足距离约束且字典序最小的字符串

> **[yiduobo的每日leetcode 3106.满足距离约束且字典序最小的字符串](https://zhuanlan.zhihu.com/p/700394920) · 知乎 · 2024-05-29 · 赞同 0**
> 力扣：[3106. 满足距离约束且字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-operations-with-constraint/) · Medium · 灵茶山艾府：[贪心，O(n) 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3106.满足距离约束且字典序最小的字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-string-after-operations-with-constraint/description/)

题目给出一个字符串s以及一个整数k，可以使用代价x将字符串中的任意字符char变为字母表中与char距离为x的字符，要求使用k的代价对s进行变换，使得s的字典序尽量小。

为了使得答案的字典序尽量小，那么就应该让字符串的头部尽量向字符'a'靠拢，于是可以一趟遍历，计算当前字符char与'a'的距离dis，也就是char的ascii码减去'a'的ascii码，以及'z'的ascii码加1再减去char的ascii码，这两种方案距离的较小值。

若dis小于等于当前的k，那么就可以将char变为'a'，此时需要将k减去dis；反之，若dis大于k，那么无法将char变为'a'，但是应该让char尽量小，因此此时就应该将char向前移动k个字符，此时k已经消耗完，可以退出循环了。

最后附上python代码：

```python
class Solution(object):
    def getSmallestString(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        res = list(s)
        for index, char in enumerate(res):
            if char == 'a':
                continue
            
            dis = min(ord(char) - 97, 123 - ord(char))
            if dis <= k:
                k -= dis
                res[index] = 'a'
            else:
                res[index] = chr(ord(char) - k)
                break
        
        return ''.join(res)
```
