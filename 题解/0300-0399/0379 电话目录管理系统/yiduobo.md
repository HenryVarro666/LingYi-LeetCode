---
title: "379. 电话目录管理系统"
aliases: ["yiduobo的每日leetcode 379.电话目录管理系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598689148"
zhihu_id: "598689148"
zhihu_title: "yiduobo的每日leetcode 379.电话目录管理系统"
question_id: "379"
question: "电话目录管理系统"
problem_url: "https://leetcode.cn/problems/design-phone-directory/"
created: "2023-01-13T04:45:04+08:00"
updated: "2023-01-13T04:45:04+08:00"
upvotes: 0
comments: 0
---

# 379. 电话目录管理系统

> **[yiduobo的每日leetcode 379.电话目录管理系统](https://zhuanlan.zhihu.com/p/598689148) · 知乎 · 2023-01-13 · 赞同 0**
> 力扣：[379. 电话目录管理系统](https://leetcode.cn/problems/design-phone-directory/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

379.电话目录管理系统

[力扣](https://leetcode.cn/problems/design-phone-directory/)

比较基础的题目，只需使用一个集合维护当前还未使用的电话号码就行了。题目中的三种操作分别对应了集合的pop、in以及add操作。

最后附上python代码：

```python
class PhoneDirectory(object):

    def __init__(self, maxNumbers):
        """
        :type maxNumbers: int
        """
        self.idle = set(range(maxNumbers))

    def get(self):
        """
        :rtype: int
        """
        if len(self.idle) == 0:
            return -1
        return self.idle.pop()

    def check(self, number):
        """
        :type number: int
        :rtype: bool
        """
        return number in self.idle

    def release(self, number):
        """
        :type number: int
        :rtype: None
        """
        self.idle.add(number)

# Your PhoneDirectory object will be instantiated and called as such:
# obj = PhoneDirectory(maxNumbers)
# param_1 = obj.get()
# param_2 = obj.check(number)
# obj.release(number)
```
