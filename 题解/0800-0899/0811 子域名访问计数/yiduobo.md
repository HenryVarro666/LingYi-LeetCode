---
title: "811. 子域名访问计数"
aliases: ["yiduobo的每日leetcode 811.子域名访问计数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343809343"
zhihu_id: "343809343"
zhihu_title: "yiduobo的每日leetcode 811.子域名访问计数"
question_id: "811"
question: "子域名访问计数"
problem_url: "https://leetcode.cn/problems/subdomain-visit-count/"
created: "2021-01-12T20:03:38+08:00"
updated: "2021-01-12T20:03:38+08:00"
upvotes: 0
comments: 0
---

# 811. 子域名访问计数

> **[yiduobo的每日leetcode 811.子域名访问计数](https://zhuanlan.zhihu.com/p/343809343) · 知乎 · 2021-01-12 · 赞同 0**
> 力扣：[811. 子域名访问计数](https://leetcode.cn/problems/subdomain-visit-count/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

811.子域名访问计数

[力扣](https://leetcode-cn.com/problems/subdomain-visit-count/)

比较基础的题目，用点来分割域名的各个部分，然后从后往前逐个组合并使用dict统计出现次数即可。

最后附上python代码：

```python
class Solution(object):
    def subdomainVisits(self, cpdomains):
        """
        :type cpdomains: List[str]
        :rtype: List[str]
        """

        domain_dict = {}
        for cpdomain in cpdomains:
            cnt, domain = cpdomain.split(' ')
            parts = domain.split('.')
            cnt = int(cnt)
            n = len(parts)
            now = parts[n - 1]
            domain_dict[now] = domain_dict.get(now, 0) + cnt
            for index in range(n - 2, -1, -1):
                now = parts[index] + '.' + now
                domain_dict[now] = domain_dict.get(now, 0) + cnt
        
        return [str(value) + ' ' + key for key, value in domain_dict.items()]
```
