---
title: "3597. 分割字符串"
aliases: ["yiduobo的每日leetcode 3597.分割字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/trie", "leetcode/hash-table", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1940895875216937538"
zhihu_id: "1940895875216937538"
zhihu_title: "yiduobo的每日leetcode 3597.分割字符串"
question_id: "3597"
question: "分割字符串"
problem_url: "https://leetcode.cn/problems/partition-string/"
difficulty: "Medium"
created: "2025-08-19T00:07:22+08:00"
updated: "2025-08-19T00:07:22+08:00"
upvotes: 1
comments: 0
---

# 3597. 分割字符串

> **[yiduobo的每日leetcode 3597.分割字符串](https://zhuanlan.zhihu.com/p/1940895875216937538) · 知乎 · 2025-08-19 · 赞同 1**
> 力扣：[3597. 分割字符串](https://leetcode.cn/problems/partition-string/) · Medium · 灵茶山艾府：[两种方法：哈希集合 / 字典树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3597.分割字符串

[3597. 分割字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/partition-string/description/)

题目给出一个字符串s，现在要求按一下步骤将其分割为互不相同的段 。

1、从下标0开始构造一个段

2、逐个字符扩展当前的段，直到该段之前从未出现过

3、若当前段是唯一的，就将其加入段列表，标记为已经出现过，然后从下一个下标开始构建新的段

4、重复上述步骤直到处理完整个字符串s

要求按顺序返回所有创建的段

题目中对于新的段的构造方法是在目前前缀独一无二的前提下，新添加一个字符，然后检测新的前缀是否独一无二。可以发现，在这里使用trie树进行构造和检测是非常合适的。

对于每个新的段，都从trie树的根节点开始检测。对于每个新添加的字符，如果其出现在当前树节点的孩子中，那么就说明当前前缀之前出现过了，此时应该迭代到对应的孩子节点，然后继续添加新字符进行构造，反之，则说明当前的新前缀是独一无二的，此时添加新节点后，将当前字符串添加到答案然后另起一段即可。重复此过程直到字符串中的所有字符都用完为止。

最后附上python代码：

```python
class Node(object):
    def __init__(self):
        self.children = {}

class Solution(object):
    def partitionString(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        
        root = Node()
        res = []
        p = 0
        start = 0
        while p < len(s):
            curr = root
            start = p
            while p < len(s) and s[p] in curr.children:
                curr = curr.children[s[p]]
                p += 1
            
            if p == len(s):
                break
            
            node = Node()
            curr.children[s[p]] = node
            res.append(s[start: p + 1])
            p += 1
        
        return res
```
