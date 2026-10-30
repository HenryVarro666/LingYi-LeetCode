---
title: "3083. 字符串及其反转中是否存在同一子字符串"
aliases: ["yiduobo的每日leetcode 3083.字符串及其反转中是否存在同一子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/array", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698549764"
zhihu_id: "698549764"
zhihu_title: "yiduobo的每日leetcode 3083.字符串及其反转中是否存在同一子字符串"
question_id: "3083"
question: "字符串及其反转中是否存在同一子字符串"
problem_url: "https://leetcode.cn/problems/existence-of-a-substring-in-a-string-and-its-reverse/"
difficulty: "Easy"
created: "2024-05-19T00:28:07+08:00"
updated: "2024-05-19T00:28:07+08:00"
upvotes: 1
comments: 0
---

# 3083. 字符串及其反转中是否存在同一子字符串

> **[yiduobo的每日leetcode 3083.字符串及其反转中是否存在同一子字符串](https://zhuanlan.zhihu.com/p/698549764) · 知乎 · 2024-05-19 · 赞同 1**
> 力扣：[3083. 字符串及其反转中是否存在同一子字符串](https://leetcode.cn/problems/existence-of-a-substring-in-a-string-and-its-reverse/) · Easy · 灵茶山艾府：[一次遍历+位运算优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3083.字符串及其反转中是否存在同一子字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/existence-of-a-substring-in-a-string-and-its-reverse/description/)

题目需要判断的子串长度仅为2，那么只需一趟遍历，将所有长度为2的子串加入到集合中，然后再一趟反向遍历，检测所有长度为2的反向子串是否出现在集合中即可。

最后附上python代码：

```python
class Solution(object):
    def isSubstringPresent(self, s):
        """
        :type s: str
        :rtype: bool
        """

        sub_set = set()
        for index in range(len(s) - 1):
            sub_set.add(s[index] + s[index + 1])
        
        for index in range(len(s) - 1, 0, -1):
            if s[index] + s[index - 1] in sub_set:
                return True

        return False
```
