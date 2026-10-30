---
title: "2734. 执行子串操作后的字典序最小字符串"
aliases: ["yiduobo的每日leetcode 2734.执行子串操作后的字典序最小字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652702896"
zhihu_id: "652702896"
zhihu_title: "yiduobo的每日leetcode 2734.执行子串操作后的字典序最小字符串"
question_id: "2734"
question: "执行子串操作后的字典序最小字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-substring-operation/"
difficulty: "Medium"
rating: 1405
created: "2023-08-28T00:56:03+08:00"
updated: "2023-08-28T00:56:03+08:00"
upvotes: 0
comments: 0
---

# 2734. 执行子串操作后的字典序最小字符串

> **[yiduobo的每日leetcode 2734.执行子串操作后的字典序最小字符串](https://zhuanlan.zhihu.com/p/652702896) · 知乎 · 2023-08-28 · 赞同 0**
> 力扣：[2734. 执行子串操作后的字典序最小字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-substring-operation/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2734.执行子串操作后的字典序最小字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/lexicographically-smallest-string-after-substring-operation/)

题目中的替换操作，对于除a之外的字符都是正收益，而替换a则是负收益。为了使得替换后的字符串字典序最小，那么就应该找到最高位的非a字符，从这个字符开始进行替换。

这里有一种特殊情况就是整个原字符串都是a，此时则应该替换掉最低位的a。对于其他情况，找到这个最高位的非a字符后，接下来从这个字符开始向后遍历直到数组末尾或者下一个字符a位置，然后替换掉中间这一段字符就行了。

最后附上python代码：

```python
class Solution(object):
    def smallestString(self, s):
        """
        :type s: str
        :rtype: str
        """

        left = 0
        while left < len(s) and s[left] == 'a':
            left += 1
        
        if left == len(s):
            return s[:len(s) - 1] + 'z'
        
        right = left + 1
        while right < len(s) and s[right] != 'a':
            right += 1
        
        return s[:left] + ''.join([chr(ord(ch) - 1) for ch in s[left : right]]) + s[right:]
```
