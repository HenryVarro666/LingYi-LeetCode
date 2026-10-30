---
title: "3860. 不同邮件组"
aliases: ["yiduobo的每日leetcode 3860.不同邮件组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2013786687310963665"
zhihu_id: "2013786687310963665"
zhihu_title: "yiduobo的每日leetcode 3860.不同邮件组"
question_id: "3860"
question: "不同邮件组"
problem_url: "https://leetcode.cn/problems/unique-email-groups/"
created: "2026-03-08T23:35:42+08:00"
updated: "2026-03-08T23:35:45+08:00"
upvotes: 1
comments: 0
---

# 3860. 不同邮件组

> **[yiduobo的每日leetcode 3860.不同邮件组](https://zhuanlan.zhihu.com/p/2013786687310963665) · 知乎 · 2026-03-08 · 赞同 1**
> 力扣：[3860. 不同邮件组](https://leetcode.cn/problems/unique-email-groups/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3860.不同邮件组

<https://leetcode.cn/problems/unique-email-groups/description/>

题目给出一个字符串数组emails，其中每个字符串都是一个有效的邮件地址。

若两个邮件地址的规范化本地名称和规范化域名名称都相同，则属于同一组。

规范化规则如下：

- 本地名称是'@'符号之前的部分
   - 忽略其中的所有点'.'
   - 若存在'+'，则忽略其中第一个'+'之后的所有内容
   - 转换为小写
- 域名是'@'符号后面的部分
   - 转换为小写

要求计算规范化之后不同电子邮件组的数量。

按照题目要求遍历所有邮箱地址，使用一个集合emails_set记录不同的电子邮件组。

对于当前地址e先通过'@'进行split，得到本地名称local以及域名domain

接下来，对local通过'+'进行一次split操作，取split结果中下标为0的部分，接下来通过replace操作将其中的'.'都替换为''，最后将其转化为小写，得到最终的local。

然后，将domain转化为小写，与local以及'@'拼接后得到最终的域名final。

最后，将final加入到emails_set，然后继续处理下一个地址即可。

遍历完成后，emails_set的长度即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def uniqueEmailGroups(self, emails):
        """
        :type emails: List[str]
        :rtype: int
        """
        
        emails_set = set()

        for e in emails:
            local, domain = e.split('@')
            local = local.split('+', 1)[0].replace('.', '').lower()
            domain = domain.lower()
            final = local + '@' + domain
            emails_set.add(final)
        
        return len(emails_set)
```
