---
title: "468. 验证ip地址"
aliases: ["yiduobo的每日leetcode 468.验证ip地址"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/231992295"
zhihu_id: "231992295"
zhihu_title: "yiduobo的每日leetcode 468.验证ip地址"
question_id: "468"
question: "验证IP地址"
problem_url: "https://leetcode.cn/problems/validate-ip-address/"
difficulty: "Medium"
created: "2020-09-10T18:08:38+08:00"
updated: "2020-09-10T18:08:38+08:00"
upvotes: 0
comments: 0
---

# 468. 验证ip地址

> **[yiduobo的每日leetcode 468.验证ip地址](https://zhuanlan.zhihu.com/p/231992295) · 知乎 · 2020-09-10 · 赞同 0**
> 力扣：[468. 验证IP地址](https://leetcode.cn/problems/validate-ip-address/) · Medium · 灵茶山艾府：[Go 库函数+特判](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

468.验证ip地址<https://leetcode-cn.com/problems/validate-ip-address/>

直接按照题目描述的进行判断即可。

首先通过split点或者冒号来确定是ipv4还是ipv6，然后判断其分割之后的长度是否合法，接下来对分割之后的每个部分进行判断。

最后附上python代码：

```python
class Solution(object):
    def validIPAddress(self, IP):
        """
        :type IP: str
        :rtype: str
        """

        IP = IP.split('.')
        if len(IP) > 1:
            if len(IP) != 4:
                return 'Neither'
            for part in IP:
                if len(part) == 0:
                    return 'Neither'
                if part[0] == '0' and len(part) > 1:
                    return 'Neither'
                for char in part:
                    if ord(char) < 48 or ord(char) > 57:
                        return 'Neither'
                if int(part) > 255:
                    return 'Neither'

            return 'IPv4'

        else:
            IP = IP[0].split(':')
            if len(IP) != 8:
                return 'Neither'
            for part in IP:
                if len(part) > 4 or len(part) == 0:
                    return 'Neither'
                for char in part:
                    if ord(char) >= 48 and ord(char) <= 57:
                        continue  
                    if ord(char) >= 65 and ord(char) <= 70:
                        continue
                    if ord(char) >= 97 and ord(char) <= 102:
                        continue
                    return 'Neither'
                
            return 'IPv6'
```
