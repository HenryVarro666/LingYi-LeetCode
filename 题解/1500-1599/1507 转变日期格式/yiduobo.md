---
title: "1507. 转变日期格式"
aliases: ["yiduobo的每日leetcode 1507.转变日期格式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/419688716"
zhihu_id: "419688716"
zhihu_title: "yiduobo的每日leetcode 1507.转变日期格式"
question_id: "1507"
question: "转变日期格式"
problem_url: "https://leetcode.cn/problems/reformat-date/"
created: "2021-10-10T00:00:36+08:00"
updated: "2021-10-10T00:00:36+08:00"
upvotes: 0
comments: 0
---

# 1507. 转变日期格式

> **[yiduobo的每日leetcode 1507.转变日期格式](https://zhuanlan.zhihu.com/p/419688716) · 知乎 · 2021-10-10 · 赞同 0**
> 力扣：[1507. 转变日期格式](https://leetcode.cn/problems/reformat-date/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1507.转变日期格式

[力扣](https://leetcode-cn.com/problems/reformat-date/)

比较基础的题目，直接按对应的月份和日期转换即可。需要注意个位数月份和天数的前导0不要丢了。

最后附上python代码：

```python
class Solution(object):
    def reformatDate(self, date):
        """
        :type date: str
        :rtype: str
        """

        day, month, year = date.split(' ')
        
        month_dict = {'Jan': 1,
                      'Feb': 2,
                      'Mar': 3,
                      'Apr': 4,
                      'May': 5,
                      'Jun': 6,
                      'Jul': 7,
                      'Aug': 8,
                      'Sep': 9,
                      'Oct': 10,
                      'Nov': 11,
                      'Dec': 12}

        if day[1] >= '0' and day[1] <= '9':
            day = int(day[:2])
        else:
            day = int(day[0])

        month = month_dict[month]
        
        return '%s-%02d-%02d' % (year, month, day)
```
