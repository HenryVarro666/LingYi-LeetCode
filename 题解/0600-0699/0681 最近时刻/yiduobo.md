---
title: "681. 最近时刻"
aliases: ["yiduobo的每日leetcode 681.最近时刻"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603683291"
zhihu_id: "603683291"
zhihu_title: "yiduobo的每日leetcode 681.最近时刻"
question_id: "681"
question: "最近时刻"
problem_url: "https://leetcode.cn/problems/next-closest-time/"
created: "2023-02-05T18:20:29+08:00"
updated: "2023-02-05T18:20:29+08:00"
upvotes: 0
comments: 0
---

# 681. 最近时刻

> **[yiduobo的每日leetcode 681.最近时刻](https://zhuanlan.zhihu.com/p/603683291) · 知乎 · 2023-02-05 · 赞同 0**
> 力扣：[681. 最近时刻](https://leetcode.cn/problems/next-closest-time/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

681.最近时刻

[力扣](https://leetcode.cn/problems/next-closest-time/)

首先，将当前时间中的各个数字收集起来，形成一个数组num_list，接下来，从低位向高位讨论，看看是否存在可行的方案。

对于当前处理到的位置check_pos，将num_list中满足num_list[check_pos] \< num \< upper的所有num收集起来，这里的upper表示当前位上数字的上限，需要依据位置来决定。具体来说：

1、对于分钟的个位，upper为10

2、对于分钟的十位，upper为6

3、对于小时的个位，若小时的十位为2，那么upper为4，否则upper为10

4、对于小时的十位，upper为3

若收集到的candidate不为空，说明在当前的check_pos存在某种替代方案。此时就应该选择candidate中的最小值来替代check_pos这一位的值，同时将check_pos右侧的所有位都置为num_list中的最小值。

这种处理方法得到的必然是最优的答案，同时不需要担心越界的问题，因为替代check_pos这一位的值在选择candidate时已经经过了校验。另一方面，由于小时十位的存在，因此num_list中的最小值必然小于等于2，因此num_list中的最小值填充到任意位置上都不会出现越界的情况。

若遍历完任然没有找到可行的方案，说明只能跨天，此时仅由num_list中的最小值构成的时间是最小的，也就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def nextClosestTime(self, time):
        """
        :type time: str
        :rtype: str
        """

        num_list = [int(time[0]), int(time[1]), int(time[3]), int(time[4])]
        mi = min(num_list)

        for check_pos in range(3, -1, -1):
            if check_pos == 3:
                upper = 10
            elif check_pos == 2:
                upper = 6
            elif check_pos == 1:
                if num_list[0] == 2:
                    upper = 4
                else:
                    upper = 10
            else:
                upper = 3

            candidate = [num for num in num_list if num_list[check_pos] < num < upper]
            if candidate:
                num_list[check_pos] = min(candidate)
                for index in range(check_pos + 1, 4):
                    num_list[index] = mi
                return '%d%d:%d%d' % (num_list[0], num_list[1], num_list[2], num_list[3])
        
        return '%d%d:%d%d' % (mi, mi, mi, mi)
```
