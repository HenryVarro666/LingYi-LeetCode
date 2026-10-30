---
title: "1636. 按照频率将数组升序排序"
aliases: ["yiduobo的每日leetcode 1636.按照频率将数组升序排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/438282536"
zhihu_id: "438282536"
zhihu_title: "yiduobo的每日leetcode 1636.按照频率将数组升序排序"
question_id: "1636"
question: "按照频率将数组升序排序"
problem_url: "https://leetcode.cn/problems/sort-array-by-increasing-frequency/"
created: "2021-11-27T00:26:05+08:00"
updated: "2021-11-27T00:26:05+08:00"
upvotes: 0
comments: 0
---

# 1636. 按照频率将数组升序排序

> **[yiduobo的每日leetcode 1636.按照频率将数组升序排序](https://zhuanlan.zhihu.com/p/438282536) · 知乎 · 2021-11-27 · 赞同 0**
> 力扣：[1636. 按照频率将数组升序排序](https://leetcode.cn/problems/sort-array-by-increasing-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1636.按照频率将数组升序排序

[力扣](https://leetcode-cn.com/problems/sort-array-by-increasing-frequency/)

比较基础的题目。先计算每个数出现的频率，然后按频率为第一关键字，数值大小的相反数为第二关键字从小到大进行排序，然后对于每一组数值-频率，将对应数目的数值加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def frequencySort(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = []
        for num, cnt in sorted(cnt_dict.items(), key=lambda d:(d[1], -d[0])):
            res.extend([num] * cnt)
        
        return res
```
