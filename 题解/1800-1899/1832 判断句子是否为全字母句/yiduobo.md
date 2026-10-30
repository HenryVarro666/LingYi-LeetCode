---
title: "1832. 判断句子是否为全字母句"
aliases: ["yiduobo的每日leetcode 1832.判断句子是否为全字母句"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/467929879"
zhihu_id: "467929879"
zhihu_title: "yiduobo的每日leetcode 1832.判断句子是否为全字母句"
question_id: "1832"
question: "判断句子是否为全字母句"
problem_url: "https://leetcode.cn/problems/check-if-the-sentence-is-pangram/"
difficulty: "Easy"
created: "2022-02-15T23:42:17+08:00"
updated: "2022-02-15T23:42:17+08:00"
upvotes: 0
comments: 0
---

# 1832. 判断句子是否为全字母句

> **[yiduobo的每日leetcode 1832.判断句子是否为全字母句](https://zhuanlan.zhihu.com/p/467929879) · 知乎 · 2022-02-15 · 赞同 0**
> 力扣：[1832. 判断句子是否为全字母句](https://leetcode.cn/problems/check-if-the-sentence-is-pangram/) · Easy · 灵茶山艾府：[位运算 O(1) 空间复杂度](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1832.判断句子是否为全字母句

[力扣](https://leetcode-cn.com/problems/check-if-the-sentence-is-pangram/)

由于题目中的句子里面只包含小写字母，因此可以一趟扫描，使用set来进行去重。最终set的大小如果为26，那么就说明句子中包含了每一种字母，否则就缺失了部分的字母。

最后附上python代码：

```python
class Solution(object):
    def checkIfPangram(self, sentence):
        """
        :type sentence: str
        :rtype: bool
        """

        char_set = set()
        for char in sentence:
            char_set.add(char)
        
        return len(char_set) == 26
```
