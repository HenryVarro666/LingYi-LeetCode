---
title: "1288. 删除被覆盖区间"
aliases: ["yiduobo的每日leetcode 1288.删除被覆盖区间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/389424504"
zhihu_id: "389424504"
zhihu_title: "yiduobo的每日leetcode 1288.删除被覆盖区间"
question_id: "1288"
question: "删除被覆盖区间"
problem_url: "https://leetcode.cn/problems/remove-covered-intervals/"
difficulty: "Medium"
created: "2021-07-13T22:46:21+08:00"
updated: "2021-07-13T22:46:21+08:00"
upvotes: 0
comments: 0
---

# 1288. 删除被覆盖区间

> **[yiduobo的每日leetcode 1288.删除被覆盖区间](https://zhuanlan.zhihu.com/p/389424504) · 知乎 · 2021-07-13 · 赞同 0**
> 力扣：[1288. 删除被覆盖区间](https://leetcode.cn/problems/remove-covered-intervals/) · Medium · 灵茶山艾府：[为什么要排序？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1288.删除被覆盖区间

[力扣](https://leetcode-cn.com/problems/remove-covered-intervals/)

对于这类区间覆盖类的问题，一般的做法是将区间按某种方法进行排序，然后一趟扫描，对比当前区间与上一个区间然后进行迭代。

注意到题目中的覆盖条件是c \<\= a且b \<\= d，那么对于我们当前扫描到的区间(a, b)以及上一个区间(c, d)，一个自然的想法就是先按照左端从小到达进行排序，这样做的好处是随着扫描的进行，c \<\= a这个条件是必然成立的，此时就只需要对比b和d的大小。

若b \<\= d，那么说明(a, b)被(c, d)覆盖了，此时可以保留(c, d)不动，然后考虑下一个区间。

若b > d，那么说明(a, b)没有被(c, d)覆盖，应该将答案加上1。同时由于后续区间的左端都必然大于等于a，那么若后续的某个区间(e, f)满足c \<\= e且f \<\= d，那么也必然满足a \<\= e且f \<\= d \< b，也就是说若后续的某个区间被(c, d)覆盖，那么其必然也会被(a, b)覆盖，因此对于后续的区间我们只需用(a, b)去检测，那么此时应该将(c, d)置为(a, b)，然后考虑下一个区间。

最后附上python代码：

```python
class Solution(object):
    def removeCoveredIntervals(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """

        sorted_intervals = sorted(intervals, key=lambda d:(d[0], -d[1]))
        res = 1
        last_x, last_y = sorted_intervals[0]
        for x, y in sorted_intervals[1:]:
            if y > last_y:
                last_y = y
                if x != last_x:
                    last_x = x
                    res += 1

        return res
```
