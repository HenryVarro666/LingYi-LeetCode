---
title: "3703. 移除K-平衡子字符串"
aliases: ["yiduobo的每日leetcode 3703.移除K-平衡子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1958255802046486279"
zhihu_id: "1958255802046486279"
zhihu_title: "yiduobo的每日leetcode 3703.移除K-平衡子字符串"
question_id: "3703"
question: "移除K-平衡子字符串"
problem_url: "https://leetcode.cn/problems/remove-k-balanced-substrings/"
difficulty: "Medium"
rating: 1802
created: "2025-10-06T22:48:56+08:00"
updated: "2025-10-06T22:48:57+08:00"
upvotes: 1
comments: 0
---

# 3703. 移除K-平衡子字符串

> **[yiduobo的每日leetcode 3703.移除K-平衡子字符串](https://zhuanlan.zhihu.com/p/1958255802046486279) · 知乎 · 2025-10-06 · 赞同 1**
> 力扣：[3703. 移除K-平衡子字符串](https://leetcode.cn/problems/remove-k-balanced-substrings/) · Medium · 灵茶山艾府：[邻项消除问题的套路：栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3703.移除K-平衡子字符串

[3703. 移除K-平衡子字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/remove-k-balanced-substrings/)

题目给出一个只包含左括号和右括号的字符串s，以及一个整数k。

若一个字符串恰好是k个连续的左括号后面跟着k个连续的右括号，也就是'(((...(())...)))'，其中左右括号恰好都为k个，那么就称这是k平衡的。例如当k \= 3时，k-平衡字符串就是'((()))'

现在要求重复地从s中移除所有不重叠的k-平衡子串，然后将剩余部分连接起来。持续这个过程直到不存在k-平衡子串为止。

返回执行所有移除操作后的最终字符串。

题目可以认为是括号匹配问题的变体，不过在这里是k个一组进行匹配，直观感觉上应该依然可以通过栈模拟来完成，不过直接记录具体的括号字符串复杂度就太高了，可以改为记录括号的数量。为了区分左右括号，在这里可以将左括号的数量作为正数记录在栈中，相对的，右括号则作为负数记录在栈中。

接下来只需一趟遍历，分离出相同的括号段：

1、若当前括号段为一段左括号：

对于这种情况，只需将这一段括号对应的数量加入到栈中。需要注意的是，若此时的栈顶也是左括号，那么就应该将当前括号的数量累加到栈顶元素中。若栈为空或者栈顶为右括号，则应该直接将当前这一段的数量加入到栈中。

2、若当前括号段为一段右括号：

对于这种情况，应该先按相同的方法将对应的数量加入到栈中，接下来还需要判断是否存在可以消除的情况。

具体来说，若栈中元素大于等于两个，且栈顶元素小于等于-k，同时栈中的除栈顶外的第二个元素数量大于等于k，那么就出现了可以消除的k-平衡子串。

在这里可以这样做的理由是因为上述操作中已经合并了同类的括号，因此当栈顶为右括号时，除栈顶外的第二个元素必然就是左括号。根据最开始的设定，左括号存正数右括号存负数，在这里就对应到栈顶元素小于等于k，除栈顶外的第二个元素大于等于k。

方便起见，在这里将栈顶的两个元素分别弹出，同时记right为栈顶元素的相反数，除栈顶元素外的第二个元素为left，那么此时消除的批次t就应该是left和right中的较小值整除以k。接下来，需要让left和right分别减去t \* k，表示消除了t组k-平衡子串。在消除完成后，可能有某一侧或者两侧的括号被完全消除掉，此时还需要对这些情况进行处理，具体来说：

2-1）若left和right都为0：

说明此时栈顶的左右括号都被消耗完了，无需进行任何额外操作

2-2）若right为0，left不为0：

说明此时右括号用完了，但是还有左括号剩余，应该将left加回到栈中

2-3）若right不为0，left为0：

说明此时左括号用完了，但是右括号还有剩余，应该将right加回到栈中。需要特别注意的是，若此时的栈非空，那么就应该让栈顶元素减去right，理由是栈顶元素表示的是右括号，此时应该将剩余的right个右括号合并进去。反之，则只需将-right加入到栈中即可。

2-4）若right和left都不为0：

此时两种括号都有剩余，应该先将left加入到栈中，然后将-right加入到栈中。

由于在一次消除操作后，由于右括号的合并产生新的可消除括号对，因此在这里需要重复以上的过程，直到栈中元素不足两个，或者栈顶对应的左括号或者右括号数量不足为止。

遍历完成后，只需对栈进行一趟反向遍历，构造出最终的结果字符串即可。

最后附上python代码：

```python
class Solution(object):
    def removeSubstring(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        stack = []
        p = 0
        while p < len(s):
            q = p + 1
            while q < len(s) and s[q] == s[p]:
                q += 1
                
            cnt = q - p

            if s[p] == '(':
                if stack and stack[-1] > 0:
                    stack[-1] += cnt
                else:
                    stack.append(cnt)
            
            else:
                if stack and stack[-1] < 0:
                    stack[-1] -= cnt
                else:
                    stack.append(-cnt)
                
                while len(stack) >= 2 and stack[-1] <= -k and stack[-2] >= k:
                    right = -stack.pop()
                    left = stack.pop()
                    t = min(left, right) // k
                    right -= t * k
                    left -= t * k
                    if right == 0:
                        if left == 0:
                            pass
                        else:
                            stack.append(left)
                    elif left == 0:
                        if stack:
                            stack[-1] -= right
                        else:
                            stack.append(-right)
                    else:
                        stack.append(left)
                        stack.append(-right)
        
            p = q

        res = []
        for v in stack:
            if v > 0:
                res.append('(' * v)
            else:
                res.append(')' * -v)
        
        return ''.join(res)
```
