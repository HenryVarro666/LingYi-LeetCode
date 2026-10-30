---
title: "2522. 将字符串分割成值不超过K的子字符串"
aliases: ["yiduobo的每日leetcode 2522.将字符串分割成值不超过K的子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/635183023"
zhihu_id: "635183023"
zhihu_title: "yiduobo的每日leetcode 2522.将字符串分割成值不超过K的子字符串"
question_id: "2522"
question: "将字符串分割成值不超过 K 的子字符串"
problem_url: "https://leetcode.cn/problems/partition-string-into-substrings-with-values-at-most-k/"
difficulty: "Medium"
rating: 1605
created: "2023-06-09T22:49:10+08:00"
updated: "2023-06-09T22:49:10+08:00"
upvotes: 0
comments: 0
---

# 2522. 将字符串分割成值不超过K的子字符串

> **[yiduobo的每日leetcode 2522.将字符串分割成值不超过K的子字符串](https://zhuanlan.zhihu.com/p/635183023) · 知乎 · 2023-06-09 · 赞同 0**
> 力扣：[2522. 将字符串分割成值不超过 K 的子字符串](https://leetcode.cn/problems/partition-string-into-substrings-with-values-at-most-k/) · Medium · 灵茶山艾府：[贪心 + 一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2522.将字符串分割成值不超过K的子字符串

[力扣](https://leetcode.cn/problems/partition-string-into-substrings-with-values-at-most-k/)

首先考虑无解的情况。当k为两位数时，必然不会出现无解的情况，因为最坏情况下也可以通过逐位分离字符串来完成分割。而对于k为个位数的情况，若字符串中最大的数值大于k，那么就无解，反之答案就是字符串的长度。

接下来考虑k大于等于10的情况。由于字符串中的每一位都必须使用，因此对于每个子字符串的划分就应该尽量将可以包含的字符包含进来，这样一来才能让后续的分割更加容易。根据这个结论，就可以使用一个变量p，从字符串头部开始向后迭代。每一轮都尽量分割出以下标p为起始位置的子字符串，然后将p移动到分割后的下一位，直到p来到字符串的末尾为止。

最后附上python代码：

```python
class Solution(object):
    def minimumPartition(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        if k < 10:
            if int(max(list(s))) > k:
                return -1
            else:
                return len(s)
        else:
            cnt = 0
            p = 0
            now = 0
            while p < len(s):
                while p < len(s) and now * 10 + int(s[p]) <= k:
                    now = now * 10 + int(s[p])
                    p += 1
                
                cnt += 1
                now = 0
            
            return cnt
```
