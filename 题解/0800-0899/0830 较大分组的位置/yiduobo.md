---
title: "830. 较大分组的位置"
aliases: ["yiduobo的每日leetcode 830.较大分组的位置"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344821064"
zhihu_id: "344821064"
zhihu_title: "yiduobo的每日leetcode 830.较大分组的位置"
question_id: "830"
question: "较大分组的位置"
problem_url: "https://leetcode.cn/problems/positions-of-large-groups/"
created: "2021-01-22T18:54:54+08:00"
updated: "2021-01-22T18:54:54+08:00"
upvotes: 1
comments: 0
---

# 830. 较大分组的位置

> **[yiduobo的每日leetcode 830.较大分组的位置](https://zhuanlan.zhihu.com/p/344821064) · 知乎 · 2021-01-22 · 赞同 1**
> 力扣：[830. 较大分组的位置](https://leetcode.cn/problems/positions-of-large-groups/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

830.较大分组的位置

[力扣](https://leetcode-cn.com/problems/positions-of-large-groups/)

比较基础的题目，直接从左往右开始一趟扫描，使用一个变量记录字符连续出现的左边界。若当前字符等于上一个字符，则继续向后扫描，否则根据当前位置以及左边界判断上一段连续字符是否满足长度大于等于3，同时重置左边界为当前位置，然后继续向后扫描。

不要忘记扫描完成后还需要额外判断最后一个区间。

最后附上python代码：

```python
class Solution(object):
    def largeGroupPositions(self, s):
        """
        :type s: str
        :rtype: List[List[int]]
        """

        start_pos = 0
        now = ''
        res = []
        for index, char in enumerate(s):
            if char != now:
                if index - start_pos >= 3:
                    res.append([start_pos, index - 1])
                start_pos = index
                now = char
        
        if index - start_pos >= 2:
            res.append([start_pos, index])
        
        return res
```
