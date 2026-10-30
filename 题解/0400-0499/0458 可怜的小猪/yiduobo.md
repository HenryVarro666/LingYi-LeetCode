---
title: "458. 可怜的小猪"
aliases: ["yiduobo的每日leetcode 458.可怜的小猪"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/218250005"
zhihu_id: "218250005"
zhihu_title: "yiduobo的每日leetcode 458.可怜的小猪"
question_id: "458"
question: "可怜的小猪"
problem_url: "https://leetcode.cn/problems/poor-pigs/"
created: "2020-09-05T22:41:19+08:00"
updated: "2020-09-05T22:41:19+08:00"
upvotes: 0
comments: 0
---

# 458. 可怜的小猪

> **[yiduobo的每日leetcode 458.可怜的小猪](https://zhuanlan.zhihu.com/p/218250005) · 知乎 · 2020-09-05 · 赞同 0**
> 力扣：[458. 可怜的小猪](https://leetcode.cn/problems/poor-pigs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

458.可怜的小猪<https://leetcode-cn.com/problems/poor-pigs/>

对于一头猪而言，在p分钟内可能出现下面几种情况：

1、喝了第一桶水，死了

2、喝了第一桶水没死，然后喝第二桶水死了

。。。

p/m、喝了前p/m桶水没死，然后喝第p/m桶水死了

除此之外，还可能喝所有p/m桶水都没有死。

换言之，一头猪可以表达p/m + 1种状态，于是k头猪就可以表达(p/m + 1) ^ k种状态。现在要求从n桶水中找出有毒的一桶，那么只要(p/m + 1) ^ k大于等于n就行了。解出这个k即为最后答案。

最后附上python代码：

```python
class Solution(object):
    def poorPigs(self, buckets, minutesToDie, minutesToTest):
        """
        :type buckets: int
        :type minutesToDie: int
        :type minutesToTest: int
        :rtype: int
        """

        test_round = minutesToTest / minutesToDie + 1
        pigs = 0
        while test_round ** pigs < buckets:
            pigs += 1
        
        return pigs
```
