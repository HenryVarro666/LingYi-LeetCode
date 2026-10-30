---
title: "2506. 统计相似字符串对的数目"
aliases: ["yiduobo的每日leetcode 2506.统计相似字符串对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634310201"
zhihu_id: "634310201"
zhihu_title: "yiduobo的每日leetcode 2506.统计相似字符串对的数目"
question_id: "2506"
question: "统计相似字符串对的数目"
problem_url: "https://leetcode.cn/problems/count-pairs-of-similar-strings/"
difficulty: "Easy"
created: "2023-06-03T00:11:39+08:00"
updated: "2023-06-03T00:11:40+08:00"
upvotes: 0
comments: 1
---

# 2506. 统计相似字符串对的数目

> **[yiduobo的每日leetcode 2506.统计相似字符串对的数目](https://zhuanlan.zhihu.com/p/634310201) · 知乎 · 2023-06-03 · 赞同 0**
> 力扣：[2506. 统计相似字符串对的数目](https://leetcode.cn/problems/count-pairs-of-similar-strings/) · Easy · 灵茶山艾府：[线性做法：枚举右，维护左（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2506.统计相似字符串对的数目

[力扣](https://leetcode.cn/problems/count-pairs-of-similar-strings/)

对于每个字符串，都可以使用一个26位的二进制来表示，其中每一位都对应字符串中的某个字符，若某个字符存在，其对应的位置就是1，否则就为0。这样一来，就将这些字符串都转化成了一个整数，接下来先使用哈希表查找当前整数之前出现的次数并更新答案，然后将更新当前整数出现的次数即可。

最后附上python代码：

```python
class Solution(object):
    def similarPairs(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        cnt = {}
        res = 0
        for w in words:
            state = 0
            for char in w:
                state |= (1 << (ord(char) - 97))
            
            res += cnt.get(state, 0)
            cnt[state] = cnt.get(state, 0) + 1
        
        return res
```
