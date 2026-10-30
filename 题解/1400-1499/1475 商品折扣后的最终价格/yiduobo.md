---
title: "1475. 商品折扣后的最终价格"
aliases: ["yiduobo的每日leetcode 1475.商品折扣后的最终价格"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/414737734"
zhihu_id: "414737734"
zhihu_title: "yiduobo的每日leetcode 1475.商品折扣后的最终价格"
question_id: "1475"
question: "商品折扣后的最终价格"
problem_url: "https://leetcode.cn/problems/final-prices-with-a-special-discount-in-a-shop/"
difficulty: "Easy"
created: "2021-09-27T23:35:04+08:00"
updated: "2021-09-27T23:35:04+08:00"
upvotes: 0
comments: 0
---

# 1475. 商品折扣后的最终价格

> **[yiduobo的每日leetcode 1475.商品折扣后的最终价格](https://zhuanlan.zhihu.com/p/414737734) · 知乎 · 2021-09-27 · 赞同 0**
> 力扣：[1475. 商品折扣后的最终价格](https://leetcode.cn/problems/final-prices-with-a-special-discount-in-a-shop/) · Easy · 灵茶山艾府：[两种单调栈写法：从右到左 / 从左到右（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1475.商品折扣后的最终价格

[力扣](https://leetcode-cn.com/problems/final-prices-with-a-special-discount-in-a-shop/)

经典的数组中每个元素的下一个较小元素位置的问题，可以使用单调栈来进行处理。具体来说就是使用一个栈来维护当前还没有找到下一个较小元素位置的元素，那么栈中的元素必然是单调不减的，因为若栈中存在两个位置i和j，满足i \< j且prices[i] \< prices[j]，那么此时i就已经有了下一个较小元素了，不应当存在于栈中。

接下来一趟扫描，对于当前元素prices[index]：

1、若prices[index]小于等于栈顶元素，那么说明栈顶元素就已经找到了下一个较小元素的位置，此时应该将栈顶弹出。重复这个过程直到prices[index]大于栈顶元素，或者栈为空

2、此时还需要将prices[index]压入栈中

最后附上python代码：

```python
class Solution(object):
    def finalPrices(self, prices):
        """
        :type prices: List[int]
        :rtype: List[int]
        """

        stack = [0]
        res = prices[:]
        for index in range(1, len(prices)):
            while stack and prices[stack[-1]] >= prices[index]:
                res[stack[-1]] -= prices[index]
                stack.pop()
            
            stack.append(index)
        
        return res
```
