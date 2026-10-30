---
title: "2288. 价格减免"
aliases: ["yiduobo的每日leetcode 2288.价格减免"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/api"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/552716944"
zhihu_id: "552716944"
zhihu_title: "yiduobo的每日leetcode 2288.价格减免"
question_id: "2288"
question: "价格减免"
problem_url: "https://leetcode.cn/problems/apply-discount-to-prices/"
difficulty: "Medium"
created: "2022-08-11T21:13:21+08:00"
updated: "2022-08-11T21:13:21+08:00"
upvotes: 0
comments: 0
---

# 2288. 价格减免

> **[yiduobo的每日leetcode 2288.价格减免](https://zhuanlan.zhihu.com/p/552716944) · 知乎 · 2022-08-11 · 赞同 0**
> 力扣：[2288. 价格减免](https://leetcode.cn/problems/apply-discount-to-prices/) · Medium · 灵茶山艾府：[按空格分割+替换（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2288.价格减免

[力扣](https://leetcode.cn/problems/apply-discount-to-prices/)

题目要求找出所有表示价格的单词，然后将这些单词修改为打折后的价格。根据题目的描述，一个单词为价格单词需要满足三个条件：

1、单词的长度必须大于等于2

2、单词的首字母为美元符号

3、单词中除首字母外的所有字符都必须为数字

于是可以先使用空格将句子分离成单词数组，然后遍历其中的每个单词。对于当前遍历到的单词，根据上面三个条件判断是否为价格单词，若是则将价格打折后加入到答案数组中，否则直接加入到答案数组中。

遍历完成后，以空格为间隔将答案数组拼接在一起就行了。

最后附上python代码：

```python
class Solution(object):
    def discountPrices(self, sentence, discount):
        """
        :type sentence: str
        :type discount: int
        :rtype: str
        """

        def check(word):
            if len(word) < 2:
                return False
            if word[0] != '$':
                return False
            
            for char in word[1:]:
                if char < '0' or char > '9':
                    return False
            
            return True

        res = []
        for word in sentence.split(' '):
            if check(word):
                res.append('$%.2f' % (int(word[1:]) * 1.0 * (100 - discount) / 100.0))
            else:
                res.append(word)
        
        return ' '.join(res)
```
