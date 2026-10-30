---
title: "2729. 判断一个数是否迷人"
aliases: ["yiduobo的每日leetcode 2729.判断一个数是否迷人"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652183541"
zhihu_id: "652183541"
zhihu_title: "yiduobo的每日leetcode 2729.判断一个数是否迷人"
question_id: "2729"
question: "判断一个数是否迷人"
problem_url: "https://leetcode.cn/problems/check-if-the-number-is-fascinating/"
difficulty: "Easy"
created: "2023-08-24T22:17:04+08:00"
updated: "2023-08-24T22:17:04+08:00"
upvotes: 0
comments: 0
---

# 2729. 判断一个数是否迷人

> **[yiduobo的每日leetcode 2729.判断一个数是否迷人](https://zhuanlan.zhihu.com/p/652183541) · 知乎 · 2023-08-24 · 赞同 0**
> 力扣：[2729. 判断一个数是否迷人](https://leetcode.cn/problems/check-if-the-number-is-fascinating/) · Easy · 灵茶山艾府：[两种做法：位运算/打表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2729.判断一个数是否迷人

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/check-if-the-number-is-fascinating/)

按照题目要求计算出2n和3n，首先要保证3n不超过1000，接下来将这三个数的数位分离出来，最后检测这些数位是否包含1到9各一次。

最后附上python代码：

```python
class Solution(object):
    def isFascinating(self, n):
        """
        :type n: int
        :rtype: bool
        """

        if n * 3 >= 1000:
            return False

        num_set = set()
        for char in str(n):
            num_set.add(char)
        for char in str(n + n):
            num_set.add(char)
        for char in str(n + n + n):
            num_set.add(char)
        
        return len(num_set) == 9 and '0' not in num_set
```
