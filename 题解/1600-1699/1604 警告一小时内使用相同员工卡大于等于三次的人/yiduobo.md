---
title: "1604. 警告一小时内使用相同员工卡大于等于三次的人"
aliases: ["yiduobo的每日leetcode 1604.警告一小时内使用相同员工卡大于等于三次的人"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/433688251"
zhihu_id: "433688251"
zhihu_title: "yiduobo的每日leetcode 1604.警告一小时内使用相同员工卡大于等于三次的人"
question_id: "1604"
question: "警告一小时内使用相同员工卡大于等于三次的人"
problem_url: "https://leetcode.cn/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period/"
created: "2021-11-15T23:50:34+08:00"
updated: "2021-11-15T23:50:34+08:00"
upvotes: 0
comments: 0
---

# 1604. 警告一小时内使用相同员工卡大于等于三次的人

> **[yiduobo的每日leetcode 1604.警告一小时内使用相同员工卡大于等于三次的人](https://zhuanlan.zhihu.com/p/433688251) · 知乎 · 2021-11-15 · 赞同 0**
> 力扣：[1604. 警告一小时内使用相同员工卡大于等于三次的人](https://leetcode.cn/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1604.警告一小时内使用相同员工卡大于等于三次的人

[力扣](https://leetcode-cn.com/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period/)

看这题目描述就知道力扣这公司不能去了。。

回到题目本身。题目明确表示不需要考虑跨天的情况，那么就可以先对每个员工记录其打卡的时间，并接按打卡的时间从小到大进行排序，然后从第二条记录开始向后一趟扫描，每次对比当前打卡时间与上上次的打卡时间的间隔，若这个间隔在一小时内，说明当前这次、上一次以及上上次打卡这三次打卡的时间在一小时内，于是需要将当前员工加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def alertNames(self, keyName, keyTime):
        """
        :type keyName: List[str]
        :type keyTime: List[str]
        :rtype: List[str]
        """

        time_dict = {}
        n = len(keyName)
        for index in range(n):
            name = keyName[index]
            hour, minute = keyTime[index].split(':')
            if name not in time_dict:
                time_dict[name] = []
            time_dict[name].append(int(hour) * 60 + int(minute))
        
        res = []
        for name in sorted(time_dict.keys()):
            if len(time_dict[name]) < 3:
                continue
            time_list = sorted(time_dict[name])
            for index in range(2, len(time_list)):
                if time_list[index] - time_list[index - 2] <= 60:
                    res.append(name)
                    break
        
        return res
```
