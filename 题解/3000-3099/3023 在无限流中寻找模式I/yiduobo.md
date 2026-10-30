---
title: "3023. 在无限流中寻找模式I"
aliases: ["yiduobo的每日leetcode 3023.在无限流中寻找模式I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694928317"
zhihu_id: "694928317"
zhihu_title: "yiduobo的每日leetcode 3023.在无限流中寻找模式I"
question_id: "3023"
question: "在无限流中寻找模式I"
created: "2024-04-28T00:47:19+08:00"
updated: "2024-04-28T00:47:19+08:00"
upvotes: 1
comments: 0
---

# 3023. 在无限流中寻找模式I

> **[yiduobo的每日leetcode 3023.在无限流中寻找模式I](https://zhuanlan.zhihu.com/p/694928317) · 知乎 · 2024-04-28 · 赞同 1**
> 力扣：3023. 在无限流中寻找模式I

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3023.在无限流中寻找模式I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-pattern-in-infinite-stream-i/description/)

非常标准的字符串匹配问题，适合使用kmp算法。先基于pattern建立next数组，然后不断向后遍历stream，利用next来进行匹配即可。

kmp算法的具体细节可以参考之前的28题，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 28.实现 strStr()](https://zhuanlan.zhihu.com/p/117670077)

另外，之后的3037题也是同样的题目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-pattern-in-infinite-stream-ii/description/)

最后附上python代码：

```python
# Definition for an infinite stream.
# class InfiniteStream:
#     def next(self):
#         pass
class Solution(object):
    def findPattern(self, stream, pattern):
        """
        :type stream: InfiniteStream
        :type pattern: List[int]
        :rtype: int
        """

        f = [0]
        p = 0
        for index in range(1, len(pattern)):
            while p and pattern[index] != pattern[p]:
                p = f[p - 1]
            
            if pattern[index] == pattern[p]:
                p += 1
            
            f.append(p)
        
        index = -1
        p = 0
        while p < len(pattern):
            index += 1
            char = stream.next()
            while p and pattern[p] != char:
                p = f[p - 1]
            
            if char == pattern[p]:
                p += 1
        
        return index - len(pattern) + 1
```
