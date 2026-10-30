---
title: "1698. 字符串的不同子字符串个数"
aliases: ["yiduobo的每日leetcode 1698.字符串的不同子字符串个数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/suffix-array", "leetcode/zi-dong-ji", "题单/字符串", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619999809"
zhihu_id: "619999809"
zhihu_title: "yiduobo的每日leetcode 1698.字符串的不同子字符串个数"
question_id: "1698"
question: "字符串的不同子字符串个数"
problem_url: "https://leetcode.cn/problems/number-of-distinct-substrings-in-a-string/"
difficulty: "Medium"
created: "2023-04-07T00:49:14+08:00"
updated: "2023-04-07T00:49:14+08:00"
upvotes: 0
comments: 1
---

# 1698. 字符串的不同子字符串个数

> **[yiduobo的每日leetcode 1698.字符串的不同子字符串个数](https://zhuanlan.zhihu.com/p/619999809) · 知乎 · 2023-04-07 · 赞同 0**
> 力扣：[1698. 字符串的不同子字符串个数](https://leetcode.cn/problems/number-of-distinct-substrings-in-a-string/) · Medium · 灵茶山艾府：[O(N) 后缀数组 / 后缀自动机](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1698.字符串的不同子字符串个数

[力扣](https://leetcode.cn/problems/number-of-distinct-substrings-in-a-string/)

字符串中的每个子串都是其某个后缀字符串的前缀，那么王道做法自然是使用后缀数组，这样就可以得到题目要求的O(n)的算法。

我在这里偷懒，直接使用的O(n^2)的暴力算法：从头到尾遍历字符串，对于每个字符，将以当前字符为起点的所有子串加入到trie树中，在这个过程中每新产生一个节点说明就多出一种不同的子串。

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self):
        self.childs = {}

class Solution(object):
    def countDistinct(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        root = TreeNode()

        for index in range(len(s)):
            now = root
            for char in s[index:]:
                if char not in now.childs:
                    res += 1
                    tmp = TreeNode()
                    now.childs[char] = tmp
                
                now = now.childs[char]
        
        return res
```
