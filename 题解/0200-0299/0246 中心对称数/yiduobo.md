---
title: "246. 中心对称数"
aliases: ["yiduobo的每日leetcode 246.中心对称数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591897029"
zhihu_id: "591897029"
zhihu_title: "yiduobo的每日leetcode 246.中心对称数"
question_id: "246"
question: "中心对称数"
problem_url: "https://leetcode.cn/problems/strobogrammatic-number/"
created: "2022-12-14T23:44:20+08:00"
updated: "2022-12-14T23:44:20+08:00"
upvotes: 0
comments: 0
---

# 246. 中心对称数

> **[yiduobo的每日leetcode 246.中心对称数](https://zhuanlan.zhihu.com/p/591897029) · 知乎 · 2022-12-14 · 赞同 0**
> 力扣：[246. 中心对称数](https://leetcode.cn/problems/strobogrammatic-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

246.中心对称数

[力扣](https://leetcode.cn/problems/strobogrammatic-number/)

题目定义的中心对称数可以分成两类，第一类是自身与自身对称，一共有0、1、8这三种；第二类则是与另一个数对称，只有6和9这一对。需要注意2和5并不是中心对称数，因为2翻转180度之后是翻过来的5。

接下来只需使用两个指针left和right，从两侧向中心一趟遍历，判断当前的num[left]和num[right]是否符合上面这几种情况，若不符合，那么就直接返回false。若能成功遍历完成，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def isStrobogrammatic(self, num):
        """
        :type num: str
        :rtype: bool
        """

        left = 0
        right = len(num) - 1
        single_set = set(['0', '1', '8'])
        pair_set = set(['6', '9'])
        while left <= right:
            if num[left] in single_set:
                if num[right] != num[left]:
                    return False
            elif num[left] in pair_set:
                if num[right] not in pair_set or num[left] == num[right]:
                    return False
            else:
                return False
            
            left += 1
            right -= 1
        
        return True
```
