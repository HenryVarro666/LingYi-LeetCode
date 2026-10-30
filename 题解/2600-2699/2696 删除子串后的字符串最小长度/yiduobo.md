---
title: "2696. 删除子串后的字符串最小长度"
aliases: ["yiduobo的每日leetcode 2696.删除子串后的字符串最小长度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650231388"
zhihu_id: "650231388"
zhihu_title: "yiduobo的每日leetcode 2696.删除子串后的字符串最小长度"
question_id: "2696"
question: "删除子串后的字符串最小长度"
problem_url: "https://leetcode.cn/problems/minimum-string-length-after-removing-substrings/"
difficulty: "Easy"
rating: 1282
created: "2023-08-15T19:46:32+08:00"
updated: "2023-08-15T19:46:32+08:00"
upvotes: 0
comments: 0
---

# 2696. 删除子串后的字符串最小长度

> **[yiduobo的每日leetcode 2696.删除子串后的字符串最小长度](https://zhuanlan.zhihu.com/p/650231388) · 知乎 · 2023-08-15 · 赞同 0**
> 力扣：[2696. 删除子串后的字符串最小长度](https://leetcode.cn/problems/minimum-string-length-after-removing-substrings/) · Easy · 灵茶山艾府：[两种算法：暴力替换/栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2696.删除子串后的字符串最小长度

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-string-length-after-removing-substrings/description/)

经典的栈模拟问题。使用栈的理由可以参考样例一中删除CD后形成了第二组AB，因此需要使用某种数据结构储存之前的字符串。

一趟遍历，将字符串中的字符逐个加入到栈中，每次加入后检测当前栈顶的两个元素是否为AB或者CD，若是，则将这两个字符弹出然后再次检测，直到栈中元素不足两个或者栈顶的两个元素不是AB也不是CD为止。

最后附上python代码：

```python
class Solution(object):
    def minLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        stack = []
        for char in s:
            stack.append(char)
            while len(stack) >= 2 and ((stack[-1] == 'D' and stack[-2] == 'C') or (stack[-1] == 'B' and stack[-2] == 'A')):
                stack.pop()
                stack.pop()
        
        return len(stack)
```
