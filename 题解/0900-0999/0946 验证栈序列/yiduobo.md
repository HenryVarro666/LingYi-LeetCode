---
title: "946. 验证栈序列"
aliases: ["yiduobo的每日leetcode 946.验证栈序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359101465"
zhihu_id: "359101465"
zhihu_title: "yiduobo的每日leetcode 946.验证栈序列"
question_id: "946"
question: "验证栈序列"
problem_url: "https://leetcode.cn/problems/validate-stack-sequences/"
created: "2021-03-22T22:32:16+08:00"
updated: "2021-03-22T22:32:16+08:00"
upvotes: 0
comments: 0
---

# 946. 验证栈序列

> **[yiduobo的每日leetcode 946.验证栈序列](https://zhuanlan.zhihu.com/p/359101465) · 知乎 · 2021-03-22 · 赞同 0**
> 力扣：[946. 验证栈序列](https://leetcode.cn/problems/validate-stack-sequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

946.验证栈序列

[力扣](https://leetcode-cn.com/problems/validate-stack-sequences/)

可以直接使用一个栈来模拟整个流程。由于栈是先进后出的数据结构，对于当前应该出栈的元素而言，其必须恰好是栈顶的元素。

我们可以遍历整个出栈序列，对于当前应该出栈的数x而言，若当前栈顶元素不是x，就将入栈序列的下一个数加入栈中，直到入栈序列为空或者栈顶元素为x。若此时栈顶元素就是x，那么将其弹出然后考察出栈序列的下一个元素，否则说明无法达成，返回false即可。

若可以顺利遍历完成，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def validateStackSequences(self, pushed, popped):
        """
        :type pushed: List[int]
        :type popped: List[int]
        :rtype: bool
        """

        n = len(pushed)
        push_pos = pop_pos = 0
        stack = []
        while pop_pos < n:
            while push_pos < n and (not stack or stack[-1] != popped[pop_pos]):
                stack.append(pushed[push_pos])
                push_pos += 1
            
            if not stack or stack[-1] != popped[pop_pos]:
                return False
            
            stack.pop()
            pop_pos += 1
        
        return True
```
