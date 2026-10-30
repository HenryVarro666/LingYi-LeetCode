---
title: "1736. 替换隐藏数字得到的最晚时间"
aliases: ["yiduobo的每日leetcode 1736.替换隐藏数字得到的最晚时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452879446"
zhihu_id: "452879446"
zhihu_title: "yiduobo的每日leetcode 1736.替换隐藏数字得到的最晚时间"
question_id: "1736"
question: "替换隐藏数字得到的最晚时间"
problem_url: "https://leetcode.cn/problems/latest-time-by-replacing-hidden-digits/"
created: "2022-01-03T18:53:49+08:00"
updated: "2022-01-03T18:53:50+08:00"
upvotes: 0
comments: 0
---

# 1736. 替换隐藏数字得到的最晚时间

> **[yiduobo的每日leetcode 1736.替换隐藏数字得到的最晚时间](https://zhuanlan.zhihu.com/p/452879446) · 知乎 · 2022-01-03 · 赞同 0**
> 力扣：[1736. 替换隐藏数字得到的最晚时间](https://leetcode.cn/problems/latest-time-by-replacing-hidden-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1736.替换隐藏数字得到的最晚时间

[力扣](https://leetcode-cn.com/problems/latest-time-by-replacing-hidden-digits/)

24小时表示的时间里面，由于存在20、21、22、23这几个小时，因此小时的两位之间是有某种限制关系的。相对的，分钟的两位取值相对是独立的。

对于本题，先考察小时：

1、若时间形如??:YY，那么应该将小时替换成23

2、若时间形如?X:YY，那么此时需要根据X的大小进行判断。若X\<\=3，那么就可以写成2X:YY这种形式，否则只能写成1X:YY这种形式

3、若时间形如X?:YY，那么此时也需要根据X的大小进行判断。若X \= 2，那么小时只能是23，也就是说只能写成23:YY这种形式，其他情况下为了尽可能大，应该写成X9:YY这种形式

接下来考察分钟。由于这两位相对独立，因此若分钟的十位数隐藏，那么应该将其替换成5。同样的，若个位数隐藏，应该将其替换成9。

最后附上python代码：

```python
class Solution(object):
    def maximumTime(self, time):
        """
        :type time: str
        :rtype: str
        """

        time_list = list(time)

        if time_list[0] == '?':
            if time_list[1] == '?':
                time_list[0] = '2'
                time_list[1] = '3'
            elif time_list[1] <= '3':
                time_list[0] = '2'
            else:
                time_list[0] = '1'
        elif time_list[1] == '?':
            if time_list[0] == '2':
                time_list[1] = '3'
            else:
                time_list[1] = '9'
        
        if time_list[3] == '?':
            time_list[3] = '5'
        
        if time_list[4] == '?':
            time_list[4] = '9'
        
        return ''.join(time_list)
```
