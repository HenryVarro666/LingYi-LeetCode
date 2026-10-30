---
title: "4043. 恰好有K对相等相邻字符的循环移位数量"
aliases: ["yiduobo的每日leetcode 4043.恰好有K对相等相邻字符的循环移位数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2079962761954706353"
zhihu_id: "2079962761954706353"
zhihu_title: "yiduobo的每日leetcode 4043.恰好有K对相等相邻字符的循环移位数量"
question_id: "4043"
question: "恰好有 K 对相等相邻字符的循环移位数量"
problem_url: "https://leetcode.cn/problems/count-rotations-with-exactly-k-equal-adjacent-pairs/"
difficulty: "Easy"
created: "2026-09-06T16:21:16+08:00"
updated: "2026-09-06T16:21:20+08:00"
upvotes: 1
comments: 0
---

# 4043. 恰好有K对相等相邻字符的循环移位数量

> **[yiduobo的每日leetcode 4043.恰好有K对相等相邻字符的循环移位数量](https://zhuanlan.zhihu.com/p/2079962761954706353) · 知乎 · 2026-09-06 · 赞同 1**
> 力扣：[4043. 恰好有 K 对相等相邻字符的循环移位数量](https://leetcode.cn/problems/count-rotations-with-exactly-k-equal-adjacent-pairs/) · Easy · 灵茶山艾府：[两种 O(n) 方法：定长滑动窗口 / 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4043.恰好有K对相等相邻字符的循环移位数量

<https://leetcode.cn/problems/count-rotations-with-exactly-k-equal-adjacent-pairs/description/>

题目给出一个长度为n的字符串s以及一个整数k。

s的一次循环移位，指的是选择一个长度从0到n - 1的前缀，将其移动到s的末尾，同时保持所有字符的相对顺序不变。

对于s的每一种循环移位，其得分定义为相同的相邻字符串对数量。即对于0 \<\= index \< n - 1，若当前s的s[index]与s[index + 1]相同，那么得分加上1。

问使得最终得分为k的循环移位数量。

首先可以明确的是，若不执行循环移位，那么s的得分就是原始形态下相同的相邻字符对数量。而如果选择执行循环位移，不妨设目前移动的前缀为s[:p]，那么原始s中的s[p - 1]与s[p]将不再相邻，而s[0]和s[-1]将会因为此次移位操作变为相邻。换言之，循环移位操作对得分的影响至多为1，因此在这里可以分情况进行讨论。

对s一趟遍历，计算原始形态下的得分cnt，接下来:

1、若cnt为k - 1：

此时如果想让得分变为k，那么必须要满足s[0]与[-1]相同，只有这样才可能通过移位操作使得得分加1。

另一方面，断开的位置两侧的字符不能相同，否则移位操作就会使得得分减去1。由于目前已经知道原始s中有cnt个位置两侧的字符相同，因此对于剩余的n - 1 - cnt \= n - 1 - (k - 1) \= n - k个位置可以用来拆分。

综合上面两个条件，若s[0]与s[-1]相同，那么答案就是n - k，否则答案为0。

2、若cnt为k：

此时可以不执行移位操作，那么保底的答案为1。接下来如果执行移位操作，那么同样是两种情况：

- 移位操作不会断开原始的相同字符对，也不会产生新的相同字符对
- 移位操作会断开一组相同字符对，也会产生一组新的相同字符对

由于是否会产生新的字符对仅取决于s[0]与s[-1]是否相同，那么当二者相同时，只能考虑第二种情况，否则只能考虑第一种情况。

对于第一种情况，也就是s[0]与s[-1]不同时，相当于断开的位置不能出现在原始的cnt个位置中，因此还有n - 1 - cnt个位置可以断开。再加上保底的答案1，因此最终答案为n - cnt \= n - k。

对于第二种情况，也就是s[0]与s[-1]相同时，相当于断开的位置必须出现在原始的cnt个位置中，再加上保底的答案1，因此最终答案为cnt + 1 \= k + 1。

3、若cnt为k + 1：

此时如果想让得分变为k，那么必须要满足s[0]与s[-1]不同，且移位操作必须断开某一对相同的字符。

因此当s[0]与s[-1]不同时，答案为cnt \= k，否则答案为0。

4、其他情况：

由于cnt的变化最多为1，因此不可能通过移位操作得到k，此时的答案为0。

最后附上python代码：

```python
class Solution(object):
    def countRotations(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        cnt = 0
        n = len(s)
        for index in range(1, n):
            if s[index] == s[index - 1]:
                cnt += 1
        
        if cnt == k - 1:
            if s[0] == s[-1]:
                return n - k
            else:
                return 0
        
        elif cnt == k:
            if s[0] == s[-1]:
                return k + 1
            else:
                return n - k
        
        elif cnt == k + 1:
            if s[0] == s[-1]:
                return 0
            else:
                return cnt
        else:
            return 0
```
