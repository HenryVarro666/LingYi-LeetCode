---
title: "929. 独特的电子邮件地址"
aliases: ["yiduobo的每日leetcode 929.独特的电子邮件地址"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356854782"
zhihu_id: "356854782"
zhihu_title: "yiduobo的每日leetcode 929.独特的电子邮件地址"
question_id: "929"
question: "独特的电子邮件地址"
problem_url: "https://leetcode.cn/problems/unique-email-addresses/"
created: "2021-03-13T16:41:33+08:00"
updated: "2021-03-13T16:41:33+08:00"
upvotes: 0
comments: 0
---

# 929. 独特的电子邮件地址

> **[yiduobo的每日leetcode 929.独特的电子邮件地址](https://zhuanlan.zhihu.com/p/356854782) · 知乎 · 2021-03-13 · 赞同 0**
> 力扣：[929. 独特的电子邮件地址](https://leetcode.cn/problems/unique-email-addresses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

929.独特的电子邮件地址

[力扣](https://leetcode-cn.com/problems/unique-email-addresses/)

首先，可以通过'@'将邮件地址分离成前半部分以及后半部分。

接下来，对于前半部分，只选取'+'前面的部分，然后将其中的'.'去除掉。再次感叹python处理这类问题太好用了。

最后，将两部分组合起来加入哈希表即可。

最后附上python代码：

```python
class Solution(object):
    def numUniqueEmails(self, emails):
        """
        :type emails: List[str]
        :rtype: int
        """

        email_dict = {}
        for email in emails:
            part1, part2 = email.split('@')
            part1 = part1.split('+', 1)[0].replace('.', '')
            if part2 not in email_dict:
                email_dict[part2] = set()
            email_dict[part2].add(part1)
        
        res = 0
        for value in email_dict.values():
            res += len(value)
        
        return res
```
