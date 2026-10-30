---
title: "635. 设计日志存储系统"
aliases: ["yiduobo的每日leetcode 635.设计日志存储系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602716053"
zhihu_id: "602716053"
zhihu_title: "yiduobo的每日leetcode 635.设计日志存储系统"
question_id: "635"
question: "设计日志存储系统"
problem_url: "https://leetcode.cn/problems/design-log-storage-system/"
created: "2023-02-02T01:10:15+08:00"
updated: "2023-02-02T01:10:15+08:00"
upvotes: 0
comments: 0
---

# 635. 设计日志存储系统

> **[yiduobo的每日leetcode 635.设计日志存储系统](https://zhuanlan.zhihu.com/p/602716053) · 知乎 · 2023-02-02 · 赞同 0**
> 力扣：[635. 设计日志存储系统](https://leetcode.cn/problems/design-log-storage-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

635.设计日志存储系统

[力扣](https://leetcode.cn/problems/design-log-storage-system/)

动态区间查找问题，而且区间值的取值范围很广。对于这类问题，王道做法自然是平衡二叉树，不过在这里由于数据规模较小，直接使用O(n^2)的暴力算法也是可行的。

对于时间字符串的处理，则可以先将其转化为时间戳再进行比较。

其中对于granularity的处理，在确定了精确到哪一级之后，可以将start_time在这一级之后的时间都置为最小时间，将end_time在这一级之后的时间都置为最大时间。

例如样例一中的Year，就是将start_time从2016:01:01:01:01:01变为2016:01:01:00:00:00，将end_time从2017:01:01:23:00:00变为2017:12:31:23:59:59。而对于样例二中的Hour，则将start_time边为2016:01:01:01:00:00，将end_time变为2017:01:01:23:59:59。

在这里需要特别注意的是，日期这一项的最大值受月份的影响，其中对于二月，还需要考虑闰年的影响。

计算好修正之后的start_time和end_time后，同样将其转化为时间戳，然后遍历所有日志，找出时间戳位于二者之间的日志即可。

最后附上python代码：

```python
import time

class LogSystem(object):

    def __init__(self):
        self.log_list = []
        self.small_month = set(['04', '06', '09', '11'])
        self.cut_pos = {'Year': 0, 'Month': 1, 'Day': 2, 'Hour': 3, 'Minute': 4, 'Second': 5}

    def put(self, id, timestamp):
        """
        :type id: int
        :type timestamp: str
        :rtype: None
        """
        t = time.mktime(time.strptime(timestamp, '%Y:%m:%d:%H:%M:%S'))
        self.log_list.append([t, id])

    def retrieve(self, start, end, granularity):
        """
        :type start: str
        :type end: str
        :type granularity: str
        :rtype: List[int]
        """

        start_parts = start.split(':')
        end_parts = end.split(':')

        min_list = ['01', '01', '00', '00', '00']
        max_list = ['12', '31', '23', '59', '59']

        if end_parts[1] == '02':
            y = int(end_parts[0])
            if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
                max_list[1] = '29'
            else:
                max_list[1] = '28'
        elif end_parts[1] in self.small_month:
            max_list[1] = '30'

        p = self.cut_pos[granularity]

        st = time.mktime(time.strptime(':'.join(start_parts[:p + 1] + min_list[p:]), '%Y:%m:%d:%H:%M:%S'))
        et = time.mktime(time.strptime(':'.join(end_parts[:p + 1] + max_list[p:]), '%Y:%m:%d:%H:%M:%S'))
        

        res = []
        for t, id in self.log_list:
            if st <= t <= et:
                res.append(id)
        return res
        

# Your LogSystem object will be instantiated and called as such:
# obj = LogSystem()
# obj.put(id,timestamp)
# param_2 = obj.retrieve(start,end,granularity)
```
