---
title: "1346. 检查整数及其两倍数是否存在"
aliases: ["yiduobo的每日leetcode 1346.检查整数及其两倍数是否存在"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/397177737"
zhihu_id: "397177737"
zhihu_title: "yiduobo的每日leetcode 1346.检查整数及其两倍数是否存在"
question_id: "1346"
question: "检查整数及其两倍数是否存在"
problem_url: "https://leetcode.cn/problems/check-if-n-and-its-double-exist/"
created: "2021-08-06T22:53:23+08:00"
updated: "2021-08-06T22:53:23+08:00"
upvotes: 0
comments: 0
---

# 1346. 检查整数及其两倍数是否存在

> **[yiduobo的每日leetcode 1346.检查整数及其两倍数是否存在](https://zhuanlan.zhihu.com/p/397177737) · 知乎 · 2021-08-06 · 赞同 0**
> 力扣：[1346. 检查整数及其两倍数是否存在](https://leetcode.cn/problems/check-if-n-and-its-double-exist/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1346.检查整数及其两倍数是否存在

[力扣](https://leetcode-cn.com/problems/check-if-n-and-its-double-exist/)

一趟扫描，使用哈希表储存已经访问过的数。对于当前值num，若num \* 2以及num / 2出现在哈希表中，那么就返回true，否则将num加入到哈希表中然后继续向后扫描。

若扫描正常结束，说明没有数对满足两倍关系，那么返回false。

最后附上python代码：

```python
class Solution(object):
    def checkIfExist(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        num_set = set()
        for num in arr:
            if num + num in num_set:
                return True
            if num % 2 == 0 and num / 2 in num_set:
                return True
            num_set.add(num)
        
        return False
```
