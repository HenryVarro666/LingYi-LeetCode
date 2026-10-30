---
title: "2810. 故障键盘"
aliases: ["yiduobo的每日leetcode 2810.故障键盘"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/queue", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658058396"
zhihu_id: "658058396"
zhihu_title: "yiduobo的每日leetcode 2810.故障键盘"
question_id: "2810"
question: "故障键盘"
problem_url: "https://leetcode.cn/problems/faulty-keyboard/"
difficulty: "Easy"
created: "2023-09-24T01:09:06+08:00"
updated: "2023-09-24T01:09:06+08:00"
upvotes: 0
comments: 0
---

# 2810. 故障键盘

> **[yiduobo的每日leetcode 2810.故障键盘](https://zhuanlan.zhihu.com/p/658058396) · 知乎 · 2023-09-24 · 赞同 0**
> 力扣：[2810. 故障键盘](https://leetcode.cn/problems/faulty-keyboard/) · Easy · 灵茶山艾府：[双端队列 O(n) 做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2810.故障键盘

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/faulty-keyboard/description/)

题目的数据规模很小，完全可以直接一趟遍历进行模拟。当遇到字符i时将当前已有的字符串翻转过来就行了。

另外，也可以换一种角度思考，不翻转字符串本身，而是翻转插入字符串的位置，也就是当字符i出现时，下一个字符插入的位置将在数组末尾或数组头部中进行切换，这样的话就需要支持两端插入的数据结构，例如双向链表或者双端队列。不过我在这里还是直接使用的暴力算法。

最后附上python代码：

```python
class Solution(object):
    def finalString(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = []
        for char in s:
            if char == 'i':
                left = 0
                right = len(res) - 1
                while left < right:
                    res[left], res[right] = res[right], res[left]
                    left += 1
                    right -= 1
            else:
                res.append(char)
        
        return ''.join(res)
```
