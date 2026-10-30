---
title: "402. 移掉K位数字"
aliases: ["yiduobo的每日leetcode 402.移掉K位数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/183262373"
zhihu_id: "183262373"
zhihu_title: "yiduobo的每日leetcode 402.移掉K位数字"
question_id: "402"
question: "移掉K位数字"
problem_url: "https://leetcode.cn/problems/remove-k-digits/"
created: "2020-08-14T00:09:27+08:00"
updated: "2020-08-14T00:09:27+08:00"
upvotes: 0
comments: 0
---

# 402. 移掉K位数字

> **[yiduobo的每日leetcode 402.移掉K位数字](https://zhuanlan.zhihu.com/p/183262373) · 知乎 · 2020-08-14 · 赞同 0**
> 力扣：[402. 移掉K位数字](https://leetcode.cn/problems/remove-k-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

402.移掉K位数字<https://leetcode-cn.com/problems/remove-k-digits/>

贪心加栈操作的题目，印象中之前似乎出现过一道类似的，不过不记得具体题号了。

具体来说就是从高位开始往低位看，若存在相邻的两位满足高位大于低位，那么此时就应该删去高位，同时继续往前验证。

于是现在就有了一种做法：维护一个栈，然后从高位到低位进行遍历。

若当前数字的值小于栈顶元素，且还未删除够K个数字，那么就移除栈顶，重复该操作直到栈为空，或者栈顶元素小于等于当前数字，或者已经删够了K个数字。

接下来将当前位入栈，然后考察下一位直到遍历完整个num。

若遍历完整个num之后还需要删去k个元素，那么就应该删去栈顶的k个元素，因为此时的栈是单调递增的。

最后栈中剩余的元素即为答案。

最后附上python代码：

```python
class Solution(object):
    def removeKdigits(self, num, k):
        """
        :type num: str
        :type k: int
        :rtype: str
        """

        stack = []
        for now in num:
            while stack and k > 0 and stack[-1] > now:
                stack.pop()
                k -= 1
            stack.append(now)

        while k > 0:
            stack.pop()
            k -= 1
        
        if not stack:
            return '0'

        return str(int(''.join(stack)))
```
