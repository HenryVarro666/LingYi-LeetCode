---
title: "1816. 截断句子"
aliases: ["yiduobo的每日leetcode 1816.截断句子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/465551060"
zhihu_id: "465551060"
zhihu_title: "yiduobo的每日leetcode 1816.截断句子"
question_id: "1816"
question: "截断句子"
problem_url: "https://leetcode.cn/problems/truncate-sentence/"
created: "2022-02-09T23:51:49+08:00"
updated: "2022-02-09T23:51:49+08:00"
upvotes: 0
comments: 0
---

# 1816. 截断句子

> **[yiduobo的每日leetcode 1816.截断句子](https://zhuanlan.zhihu.com/p/465551060) · 知乎 · 2022-02-09 · 赞同 0**
> 力扣：[1816. 截断句子](https://leetcode.cn/problems/truncate-sentence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1816.截断句子

[力扣](https://leetcode-cn.com/problems/truncate-sentence/)

比较基础的题目，我这里直接用了python的split和join，不过个人感觉更好的写法应该一趟遍历，尝试去找句子中第k个空格。若找到了，那么输出这个空格前面的内容。若找不到，那么直接返回整个句子。

最后附上python代码：

```python
class Solution(object):
    def truncateSentence(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        return ' '.join(s.split(' ')[:k])
```
