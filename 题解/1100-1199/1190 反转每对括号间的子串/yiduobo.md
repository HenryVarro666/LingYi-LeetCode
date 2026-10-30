---
title: "1190. 反转每对括号间的子串"
aliases: ["yiduobo的每日leetcode 1190.反转每对括号间的子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/recursion", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380588646"
zhihu_id: "380588646"
zhihu_title: "yiduobo的每日leetcode 1190.反转每对括号间的子串"
question_id: "1190"
question: "反转每对括号间的子串"
problem_url: "https://leetcode.cn/problems/reverse-substrings-between-each-pair-of-parentheses/"
difficulty: "Medium"
created: "2021-06-14T19:54:27+08:00"
updated: "2021-06-14T19:54:27+08:00"
upvotes: 0
comments: 0
---

# 1190. 反转每对括号间的子串

> **[yiduobo的每日leetcode 1190.反转每对括号间的子串](https://zhuanlan.zhihu.com/p/380588646) · 知乎 · 2021-06-14 · 赞同 0**
> 力扣：[1190. 反转每对括号间的子串](https://leetcode.cn/problems/reverse-substrings-between-each-pair-of-parentheses/) · Medium · 灵茶山艾府：[两种方法：递归 / 左右横跳（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1190.反转每对括号间的子串

[力扣](https://leetcode-cn.com/problems/reverse-substrings-between-each-pair-of-parentheses/)

拿到题目后一个自然的想法就是计算出每个字符最终是否需要翻转，然后根据是否需要翻转构造出最终的答案。但是这里有一个问题是构造起来其实是比较麻烦的，因为反转的字符串需要从后往前加入到答案中，那么多次翻转的情况下位置就比较难确定了。

另一种思路则是一趟扫描模拟整个反转的过程，简单来说就是当反转开始时，我们直接通过括号匹配跳转到反转结束的位置，然后调转扫描方向进行遍历，直到回到反转开始的地方位置。

可以明确的是，从前向后扫描时遇到的反转起点都是奇数层的反转，而从后向前扫描时遇到的反转的起点则是偶数层的反转。

这样一来就有五种可能性：

1、当前字符不是括号：

将当前字符加入到答案中，然后处理下一个字符即可。需要注意的是，这里的下一个字符指的是当前扫描方向上的下一个字符，若当前是从后向前扫描，那么这里的下一个字符指的就是坐标意义上的上一个字符。

2、当前字符为左括号 ，且扫描方向是从前向后：

此时说明遇到一段奇数层反转的起点，那么应该直接跳转到与当前括号匹配的右括号的前一个位置，然后调转方向从后向前开始扫描。

3、当前字符为左括号，其扫描方向是从后向前：

此时说明回到了这一段奇数层反转的起点，也就是说这一段反转已经完结，那么我们应该跳转到这次反转的终点，也就是当前括号匹配的右括号的后一个字符的位置，然后调转方向从前向后开始扫描。

4、当前字符为右括号，且扫描方向是从后向前：

此时说明遇到了一段偶数层反转的起点，那么应该直接跳转到与当前括号匹配的左括号的后一个位置，然后调转方向从前向后开始扫描。

5、当前字符为右括号，且扫描方向是从前向后：

此时说明回到了这一段偶数层反转的起点，也就是说这一段反转已经完结，那么我们应该跳转到这次反转的起点，也就是当前括号匹配的左括号的前一个字符的位置，然后调转方向从后向前开始扫描。

可以发现，实际上情况2到情况5都可以用“跳转到当前括号匹配的另一边括号的位置，然后调转当前方向并前进一步”来概括，因此实际上最终就是两种情况。

有了上面的结论，我们就可以先使用栈求解出所有括号匹配的另一边括号的位置，然后一趟扫描，按上面的方法走完全程即可。

最后附上python代码：

```python
class Solution(object):
    def reverseParentheses(self, s):
        """
        :type s: str
        :rtype: str
        """

        n = len(s)
        match_pos = [None] * n
        stack = []
        for index, char in enumerate(s):
            if char == '(':
                stack.append(index)
            elif char == ')':
                left_pos = stack.pop()
                match_pos[index] = left_pos
                match_pos[left_pos] = index
        
        now = 0
        d = 1
        res = []
        while now < n:
            if match_pos[now] is not None:
                d = -d
                now = match_pos[now] + d
            else:
                res.append(s[now])
                now += d
        
        return ''.join(res)
```
