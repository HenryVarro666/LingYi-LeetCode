---
title: "2544. 交替数字和"
aliases: ["yiduobo的每日leetcode 2544.交替数字和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637872275"
zhihu_id: "637872275"
zhihu_title: "yiduobo的每日leetcode 2544.交替数字和"
question_id: "2544"
question: "交替数字和"
problem_url: "https://leetcode.cn/problems/alternating-digit-sum/"
difficulty: "Easy"
created: "2023-06-20T22:59:01+08:00"
updated: "2023-06-20T22:59:01+08:00"
upvotes: 0
comments: 0
---

# 2544. 交替数字和

> **[yiduobo的每日leetcode 2544.交替数字和](https://zhuanlan.zhihu.com/p/637872275) · 知乎 · 2023-06-20 · 赞同 0**
> 力扣：[2544. 交替数字和](https://leetcode.cn/problems/alternating-digit-sum/) · Easy · 灵茶山艾府：[不用字符串，O(1) 空间写法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2544.交替数字和

[力扣](https://leetcode.cn/problems/alternating-digit-sum/)

比较基础的题目。首先通过摸10除以10的操作将n的数位分离出来，翻转后一趟遍历，按照当前下标对其进行加法或者减法即可。

最后附上python代码：

```python
class Solution(object):
    def alternateDigitSum(self, n):
        """
        :type n: int
        :rtype: int
        """

        digit_list = []
        while n:
            digit_list.append(n % 10)
            n /= 10
        
        digit_list.reverse()

        res = 0
        for index in range(len(digit_list)):
            if index % 2 == 0:
                delta = 1
            else:
                delta = -1
            
            res += delta * digit_list[index]
        
        return res
```
