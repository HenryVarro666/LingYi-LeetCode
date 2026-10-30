---
title: "2325. 解密消息"
aliases: ["yiduobo的每日leetcode 2325.解密消息"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/557918932"
zhihu_id: "557918932"
zhihu_title: "yiduobo的每日leetcode 2325.解密消息"
question_id: "2325"
question: "解密消息"
problem_url: "https://leetcode.cn/problems/decode-the-message/"
difficulty: "Easy"
created: "2022-08-26T00:18:29+08:00"
updated: "2022-08-26T00:18:29+08:00"
upvotes: 0
comments: 0
---

# 2325. 解密消息

> **[yiduobo的每日leetcode 2325.解密消息](https://zhuanlan.zhihu.com/p/557918932) · 知乎 · 2022-08-26 · 赞同 0**
> 力扣：[2325. 解密消息](https://leetcode.cn/problems/decode-the-message/) · Easy · 灵茶山艾府：[简化代码的小技巧](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2325.解密消息

[力扣](https://leetcode.cn/problems/decode-the-message/)

一趟遍历，根据题目的描述找出每个字母加密后对应的字母，然后将message加密后返回即可。

具体实现上，可以使用一个哈希表储存当前已知的加密关系。对于当前遍历到的字母char，若其没有出现在哈希表中，那么其对应的字母顺序恰好就是哈希表的长度，此时将char及其加密后对应的字母加入到哈希表中即可。

最后附上python代码：

```python
class Solution(object):
    def decodeMessage(self, key, message):
        """
        :type key: str
        :type message: str
        :rtype: str
        """

        mapping = {}
        cnt = 0
        for char in key:
            if char != ' ' and char not in mapping:
                mapping[char] = chr(len(mapping) + 97)

        return ''.join([mapping.get(char, ' ') for char in message])
```
