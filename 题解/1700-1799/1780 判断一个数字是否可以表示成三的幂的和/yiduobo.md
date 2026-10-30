---
title: "1780. 判断一个数字是否可以表示成三的幂的和"
aliases: ["yiduobo的每日leetcode 1780.判断一个数字是否可以表示成三的幂的和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/462562939"
zhihu_id: "462562939"
zhihu_title: "yiduobo的每日leetcode 1780.判断一个数字是否可以表示成三的幂的和"
question_id: "1780"
question: "判断一个数字是否可以表示成三的幂的和"
problem_url: "https://leetcode.cn/problems/check-if-number-is-a-sum-of-powers-of-three/"
difficulty: "Medium"
rating: 1506
created: "2022-01-27T22:40:50+08:00"
updated: "2022-01-27T22:40:50+08:00"
upvotes: 0
comments: 0
---

# 1780. 判断一个数字是否可以表示成三的幂的和

> **[yiduobo的每日leetcode 1780.判断一个数字是否可以表示成三的幂的和](https://zhuanlan.zhihu.com/p/462562939) · 知乎 · 2022-01-27 · 赞同 0**
> 力扣：[1780. 判断一个数字是否可以表示成三的幂的和](https://leetcode.cn/problems/check-if-number-is-a-sum-of-powers-of-three/) · Medium · 灵茶山艾府：[三进制分解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1780.判断一个数字是否可以表示成三的幂的和

[力扣](https://leetcode-cn.com/problems/check-if-number-is-a-sum-of-powers-of-three/)

题目实际上就是问n的三进制表示下是否有某一位的值不等于0或者1，那么这一位肯定就是等于2。于是可以采用经典的模3取余法来将n转化为三进制。若过程中某一轮的余数为2，那么返回false。若没有任何位上的值为2，那么返回true。

最后附上python代码：

```python
class Solution(object):
    def checkPowersOfThree(self, n):
        """
        :type n: int
        :rtype: bool
        """

        while n:
            if n % 3 == 2:
                return False
            n /= 3
        
        return True
```
