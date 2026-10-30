---
title: "1961. 检测字符串是否为数组前缀"
aliases: ["yiduobo的每日leetcode 1961.检测字符串是否为数组前缀"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/493388630"
zhihu_id: "493388630"
zhihu_title: "yiduobo的每日leetcode 1961.检测字符串是否为数组前缀"
question_id: "1961"
question: "检查字符串是否为数组前缀"
problem_url: "https://leetcode.cn/problems/check-if-string-is-a-prefix-of-array/"
difficulty: "Easy"
created: "2022-04-05T17:24:18+08:00"
updated: "2022-04-05T17:24:19+08:00"
upvotes: 0
comments: 0
---

# 1961. 检测字符串是否为数组前缀

> **[yiduobo的每日leetcode 1961.检测字符串是否为数组前缀](https://zhuanlan.zhihu.com/p/493388630) · 知乎 · 2022-04-05 · 赞同 0**
> 力扣：[1961. 检查字符串是否为数组前缀](https://leetcode.cn/problems/check-if-string-is-a-prefix-of-array/) · Easy · 灵茶山艾府：[线性做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1961.检测字符串是否为数组前缀

[力扣](https://leetcode-cn.com/problems/check-if-string-is-a-prefix-of-array/)

使用两个变量p和now分别表示当前匹配到了数组中第p个单词的第now个字符，初始情况下p和now都是0。接下来对字符串一趟遍历，判断两边字符是否相同。若相同，则将now向后移动。若now移动到了p这个单词的结尾，则将now置为0，并将p向后移动。

若在过程中出现了不匹配，或者p移动到了数组末尾而字符串还没有匹配完，那么就返回false。若匹配完成，但now不等于0，说明并不是完整的单词构成了字符串，同样返回false，否则返回true。

最后附上python代码：

```python
class Solution(object):
    def isPrefixString(self, s, words):
        """
        :type s: str
        :type words: List[str]
        :rtype: bool
        """

        p = 0
        now = 0
        for char in s:
            if p == len(words):
                return False
            if char != words[p][now]:
                return False
            now += 1
            if now == len(words[p]):
                p += 1
                now = 0
        
        return now == 0
```
