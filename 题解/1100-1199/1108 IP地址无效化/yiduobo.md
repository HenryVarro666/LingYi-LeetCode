---
title: "1108. IP地址无效化"
aliases: ["yiduobo的每日leetcode 1108.IP地址无效化"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374549528"
zhihu_id: "374549528"
zhihu_title: "yiduobo的每日leetcode 1108.IP地址无效化"
question_id: "1108"
question: "IP地址无效化"
problem_url: "https://leetcode.cn/problems/defanging-an-ip-address/"
created: "2021-05-23T12:57:59+08:00"
updated: "2021-05-23T12:57:59+08:00"
upvotes: 0
comments: 0
---

# 1108. IP地址无效化

> **[yiduobo的每日leetcode 1108.IP地址无效化](https://zhuanlan.zhihu.com/p/374549528) · 知乎 · 2021-05-23 · 赞同 0**
> 力扣：[1108. IP地址无效化](https://leetcode.cn/problems/defanging-an-ip-address/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1108.IP地址无效化

[力扣](https://leetcode-cn.com/problems/defanging-an-ip-address/)

利好python的题目，直接利用语言特性replace一下即可。

最后附上python代码：

```python
class Solution(object):
    def defangIPaddr(self, address):
        """
        :type address: str
        :rtype: str
        """

        return address.replace('.', '[.]')
```
