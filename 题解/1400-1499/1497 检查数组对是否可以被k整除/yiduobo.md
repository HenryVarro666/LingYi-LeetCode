---
title: "1497. 检查数组对是否可以被k整除"
aliases: ["yiduobo的每日leetcode 1497.检查数组对是否可以被k整除"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416794997"
zhihu_id: "416794997"
zhihu_title: "yiduobo的每日leetcode 1497.检查数组对是否可以被k整除"
question_id: "1497"
question: "检查数组对是否可以被k整除"
problem_url: "https://leetcode.cn/problems/check-if-array-pairs-are-divisible-by-k/"
created: "2021-10-06T21:30:25+08:00"
updated: "2021-10-06T21:30:25+08:00"
upvotes: 0
comments: 0
---

# 1497. 检查数组对是否可以被k整除

> **[yiduobo的每日leetcode 1497.检查数组对是否可以被k整除](https://zhuanlan.zhihu.com/p/416794997) · 知乎 · 2021-10-06 · 赞同 0**
> 力扣：[1497. 检查数组对是否可以被k整除](https://leetcode.cn/problems/check-if-array-pairs-are-divisible-by-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1497.检查数组对是否可以被k整除

[力扣](https://leetcode-cn.com/problems/check-if-array-pairs-are-divisible-by-k/)

对于一个数而言，其对k取模的余数必然是落在0到k - 1之间。不妨设其余数为r，那么就应该找一个余数为k - r的数来凑成一对，从而满足二者之和可以被k整除。

于是可以一趟扫描，求出每个数对k的余数，并将这些余数出现的次数保存起来。接下来遍历0到k / 2，若当前余数r出现的次数不等于k - r出现的次数，那么说明会出现落单的数，此时应该返回false。

除此之外，若k为偶数，那么有一种情况是对k取模余k / 2，那么此时则需要判断余数为k / 2的情况出现次数会否为偶数次，若不是，则返回false。

其他情况下，答案为true。

最后附上python代码：

```python
class Solution(object):
    def canArrange(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: bool
        """

        cnt_list = [0] * k
        for num in arr:
            cnt_list[num % k] += 1
        
        for r in range(1, (k + 1) / 2):
            if cnt_list[r] != cnt_list[k - r]:
                return False

        if k % 2 == 0 and cnt_list[k / 2] % 2 != 0:
            return False
        
        return True
```
