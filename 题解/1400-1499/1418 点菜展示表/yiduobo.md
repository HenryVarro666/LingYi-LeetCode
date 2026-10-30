---
title: "1418. 点菜展示表"
aliases: ["yiduobo的每日leetcode 1418.点菜展示表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/407471300"
zhihu_id: "407471300"
zhihu_title: "yiduobo的每日leetcode 1418.点菜展示表"
question_id: "1418"
question: "点菜展示表"
problem_url: "https://leetcode.cn/problems/display-table-of-food-orders-in-a-restaurant/"
created: "2021-09-06T17:28:31+08:00"
updated: "2021-09-06T17:28:31+08:00"
upvotes: 0
comments: 0
---

# 1418. 点菜展示表

> **[yiduobo的每日leetcode 1418.点菜展示表](https://zhuanlan.zhihu.com/p/407471300) · 知乎 · 2021-09-06 · 赞同 0**
> 力扣：[1418. 点菜展示表](https://leetcode.cn/problems/display-table-of-food-orders-in-a-restaurant/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1418.点菜展示表

[力扣](https://leetcode-cn.com/problems/display-table-of-food-orders-in-a-restaurant/)

比较基础的题目。直接一趟扫描，分桌子统计每张桌子点到菜，并记录下所有点的菜的集合。接下来对集合中的菜按字典序进行排序，这里得到的顺序就是最终答案中菜的排列顺序。接下来按桌号从小到大一趟遍历，统计这种桌子上每种菜出现的次数，并填充到答案中的对应位置上即可。

最后附上python代码：

```python
class Solution(object):
    def displayTable(self, orders):
        """
        :type orders: List[List[str]]
        :rtype: List[List[str]]
        """

        table_dict = {}
        f_set = set()
        for c, t, f in orders:
            t = int(t)
            if t not in table_dict:
                table_dict[t] = []
            table_dict[t].append(f)
            if f not in f_set:
                f_set.add(f)
        
        f_num = len(f_set)
        sorted_f = sorted(list(f_set))
        f_mapping = {f : index + 1 for index, f in enumerate(sorted_f)}
        res = [['Table'] + sorted_f]
        
        for table in sorted(table_dict.keys()):
            tmp = [table] + [0] * f_num
            for f in table_dict[table]:
                tmp[f_mapping[f]] += 1
            
            res.append([str(x) for x in tmp])
        
        return res
```
