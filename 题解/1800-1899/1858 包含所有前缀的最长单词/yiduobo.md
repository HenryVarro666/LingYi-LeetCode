---
title: "1858. 包含所有前缀的最长单词"
aliases: ["yiduobo的每日leetcode 1858.包含所有前缀的最长单词"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/trie", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622408855"
zhihu_id: "622408855"
zhihu_title: "yiduobo的每日leetcode 1858.包含所有前缀的最长单词"
question_id: "1858"
question: "包含所有前缀的最长单词"
problem_url: "https://leetcode.cn/problems/longest-word-with-all-prefixes/"
difficulty: "Medium"
created: "2023-04-16T23:16:36+08:00"
updated: "2023-04-16T23:16:36+08:00"
upvotes: 0
comments: 0
---

# 1858. 包含所有前缀的最长单词

> **[yiduobo的每日leetcode 1858.包含所有前缀的最长单词](https://zhuanlan.zhihu.com/p/622408855) · 知乎 · 2023-04-16 · 赞同 0**
> 力扣：[1858. 包含所有前缀的最长单词](https://leetcode.cn/problems/longest-word-with-all-prefixes/) · Medium · 灵茶山艾府：[字典树+DFS](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1858.包含所有前缀的最长单词

[力扣](https://leetcode.cn/problems/longest-word-with-all-prefixes/)

将所有单词按长度从小到大排序，然后一趟遍历。对于当前遍历到的单词w，首先检测w除了最后一个字母外的前缀是否在之前的遍历过程中出现过。在这里可以使用trie树来储存所有合法的前缀，这样一来就可以在一趟遍历的时间内判断w的所有前缀是否都出现过。如果都出现过，那么就将w的最后这个字符也加入到trie树中，并使用w更新答案。

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self):
        self.childs = {}

class Solution(object):
    def longestWord(self, words):
        """
        :type words: List[str]
        :rtype: str
        """

        res = ''
        root = TreeNode()
        for w in sorted(words, key=lambda d:len(d)):
            now = root
            n = len(w)
            flag = True
            for index in range(n - 1):
                if w[index] not in now.childs:
                    flag = False
                    break
                
                now = now.childs[w[index]]
            
            if flag:
                tmp = TreeNode()
                now.childs[w[-1]] = tmp
                if len(w) > len(res) or (len(w) == len(res) and w < res):
                    res = w
        
        return res
```
