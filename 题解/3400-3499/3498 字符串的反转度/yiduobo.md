---
title: "3498. 字符串的反转度"
aliases: ["yiduobo的每日leetcode 3498.字符串的反转度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899628785604728102"
zhihu_id: "1899628785604728102"
zhihu_title: "yiduobo的每日leetcode 3498.字符串的反转度"
question_id: "3498"
question: "字符串的反转度"
problem_url: "https://leetcode.cn/problems/reverse-degree-of-a-string/"
difficulty: "Easy"
created: "2025-04-29T22:16:35+08:00"
updated: "2025-04-29T22:16:35+08:00"
upvotes: 1
comments: 0
---

# 3498. 字符串的反转度

> **[yiduobo的每日leetcode 3498.字符串的反转度](https://zhuanlan.zhihu.com/p/1899628785604728102) · 知乎 · 2025-04-29 · 赞同 1**
> 力扣：[3498. 字符串的反转度](https://leetcode.cn/problems/reverse-degree-of-a-string/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3498.字符串的反转度

[3498. 字符串的反转度 - 力扣（LeetCode）](https://leetcode.cn/problems/reverse-degree-of-a-string/description/)

题目给出一个字符串s，要求计算其反转度。

反转度的计算方法为对于s中的每个字符，将其反转字符在字母表中的位置，与其在字符串中的下标（从1开始）相乘后，再将乘积累加起来。

按照题目描述一趟遍历然后进行计算即可。再具体实现上，对于某个字符char，可以通过ascii码计算其反转字符在字母表中的位置，具体来说，char的ascii码为ord(char)，那么其距离'a'的ascii码的距离，就相当于其反转字符reverse距离'z'的ascii码的距离，也就是说ord('z') - ord(reverse) \= ord(char) - ord('a')。另一方面，reverse在字母表中的位置就是其距离'a'的ascii码的距离，也就是ord(reverse) - ord('a')，此时只需对上面的式子移项后就可以得到ord(reverse) - ord('a') \= ord('z') - ord(char)。

最后附上python代码：

```python
class Solution(object):
    def reverseDegree(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        res = 0
        for index, char in enumerate(s):
            res += (index + 1) * (123 - ord(char))
        return res
```
