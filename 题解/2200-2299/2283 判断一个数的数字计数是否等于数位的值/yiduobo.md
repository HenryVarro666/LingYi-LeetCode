---
title: "2283. 判断一个数的数字计数是否等于数位的值"
aliases: ["yiduobo的每日leetcode 2283.判断一个数的数字计数是否等于数位的值"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/551829681"
zhihu_id: "551829681"
zhihu_title: "yiduobo的每日leetcode 2283.判断一个数的数字计数是否等于数位的值"
question_id: "2283"
question: "判断一个数的数字计数是否等于数位的值"
problem_url: "https://leetcode.cn/problems/check-if-number-has-equal-digit-count-and-digit-value/"
difficulty: "Easy"
created: "2022-08-09T22:03:35+08:00"
updated: "2022-08-09T22:03:35+08:00"
upvotes: 0
comments: 0
---

# 2283. 判断一个数的数字计数是否等于数位的值

> **[yiduobo的每日leetcode 2283.判断一个数的数字计数是否等于数位的值](https://zhuanlan.zhihu.com/p/551829681) · 知乎 · 2022-08-09 · 赞同 0**
> 力扣：[2283. 判断一个数的数字计数是否等于数位的值](https://leetcode.cn/problems/check-if-number-has-equal-digit-count-and-digit-value/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2283.判断一个数的数字计数是否等于数位的值

[力扣](https://leetcode.cn/problems/check-if-number-has-equal-digit-count-and-digit-value/)

由于题目给出的数的长度很短，因此可以直接一趟遍历，统计每种数字出现的次数，然后再一趟遍历，判断每一位下标对应的数字出现的次数是否恰好等于这位下标对应的数。

最后附上python代码：

```python
class Solution(object):
    def digitCount(self, num):
        """
        :type num: str
        :rtype: bool
        """

        cnt_dict = {}
        for char in num:
            cnt_dict[int(char)] = cnt_dict.get(int(char), 0) + 1
        
        for index, char in enumerate(num):
            if cnt_dict.get(index, 0) != int(char):
                return False
        
        return True
```
