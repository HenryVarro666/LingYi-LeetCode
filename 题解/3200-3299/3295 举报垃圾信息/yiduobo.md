---
title: "3295. 举报垃圾信息"
aliases: ["yiduobo的每日leetcode 3295.举报垃圾信息"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/919280546"
zhihu_id: "919280546"
zhihu_title: "yiduobo的每日leetcode 3295.举报垃圾信息"
question_id: "3295"
question: "举报垃圾信息"
problem_url: "https://leetcode.cn/problems/report-spam-message/"
difficulty: "Medium"
created: "2024-10-10T23:57:05+08:00"
updated: "2024-10-10T23:57:05+08:00"
upvotes: 1
comments: 0
---

# 3295. 举报垃圾信息

> **[yiduobo的每日leetcode 3295.举报垃圾信息](https://zhuanlan.zhihu.com/p/919280546) · 知乎 · 2024-10-10 · 赞同 1**
> 力扣：[3295. 举报垃圾信息](https://leetcode.cn/problems/report-spam-message/) · Medium · 灵茶山艾府：[哈希集合，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3295.举报垃圾信息

[. - 力扣（LeetCode）](https://leetcode.cn/problems/report-spam-message/description/)

题目给出两个字符串数组message和bannedWords，要求判断message中是否至少有两个单词出现在bannedWords当中。

将bannedWords做成trie树或者哈希表，然后遍历message中的所有单词，判断是否有两个单词出现在bannedWords中即可。

最后附上python代码：

```python
class Solution(object):
    def reportSpam(self, message, bannedWords):
        """
        :type message: List[str]
        :type bannedWords: List[str]
        :rtype: bool
        """

        banned_set = set(bannedWords)
        cnt = 0
        for word in message:
            if word in banned_set:
                cnt += 1
                if cnt == 2:
                    return True

        return False
```
