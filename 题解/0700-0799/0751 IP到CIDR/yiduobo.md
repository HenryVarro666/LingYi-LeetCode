---
title: "751. IP到CIDR"
aliases: ["yiduobo的每日leetcode 751.IP到CIDR"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605782882"
zhihu_id: "605782882"
zhihu_title: "yiduobo的每日leetcode 751.IP到CIDR"
question_id: "751"
question: "IP到CIDR"
problem_url: "https://leetcode.cn/problems/ip-to-cidr/"
created: "2023-02-13T00:38:55+08:00"
updated: "2023-02-13T00:38:55+08:00"
upvotes: 0
comments: 0
---

# 751. IP到CIDR

> **[yiduobo的每日leetcode 751.IP到CIDR](https://zhuanlan.zhihu.com/p/605782882) · 知乎 · 2023-02-13 · 赞同 0**
> 力扣：[751. IP到CIDR](https://leetcode.cn/problems/ip-to-cidr/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

751.IP到CIDR

[力扣](https://leetcode.cn/problems/ip-to-cidr/)

题目中所描述的CIDR可以认为是由起始ip地址以及区间长度组成的一段ip区间。在这里有一个隐藏条件是由于CIDR包含了前缀ip中的所有ip地址，那么就意味着起始ip地址的最后若干位必然为0，而区间中最后一个ip地址的最后若干位必然为1，因此这个区间长度必然是2的幂次。

有了这个结论，就可以根据当前起始ip和n的大小来找出最大可用的2的幂次，将这一段ip分离出去形成一组CIDR，然后更新起始ip以及n并重复此过程，直到n等于0为止。

最后附上python代码：

```python
class Solution(object):
    def ipToCIDR(self, ip, n):
        """
        :type ip: str
        :type n: int
        :rtype: List[str]
        """

        ip = ip.split('.')
        now = (int(ip[0]) << 24) | (int(ip[1]) << 16) | (int(ip[2]) << 8) | int(ip[3])
        cnt = 1
        res = []
        while n > 0:
            while 1 << cnt <= n and (now & (1 << (cnt - 1)) == 0):
                cnt += 1
            
            res.append('%d.%d.%d.%d/%d' % (now >> 24, (now >> 16) & 255, (now >> 8) & 255, now & 255, 32 - cnt + 1))
            now += 1 << (cnt - 1)
            n -= 1 << (cnt - 1)
            cnt = 1
        
        return res
```
