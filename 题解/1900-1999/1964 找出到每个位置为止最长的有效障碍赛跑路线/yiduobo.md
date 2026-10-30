---
title: "1964. 找出到每个位置为止最长的有效障碍赛跑线路"
aliases: ["yiduobo的每日leetcode 1964.找出到每个位置为止最长的有效障碍赛跑线路"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/494722290"
zhihu_id: "494722290"
zhihu_title: "yiduobo的每日leetcode 1964.找出到每个位置为止最长的有效障碍赛跑线路"
question_id: "1964"
question: "找出到每个位置为止最长的有效障碍赛跑路线"
problem_url: "https://leetcode.cn/problems/find-the-longest-valid-obstacle-course-at-each-position/"
difficulty: "Hard"
rating: 1933
created: "2022-04-07T20:54:42+08:00"
updated: "2022-04-07T20:54:42+08:00"
upvotes: 0
comments: 0
---

# 1964. 找出到每个位置为止最长的有效障碍赛跑线路

> **[yiduobo的每日leetcode 1964.找出到每个位置为止最长的有效障碍赛跑线路](https://zhuanlan.zhihu.com/p/494722290) · 知乎 · 2022-04-07 · 赞同 0**
> 力扣：[1964. 找出到每个位置为止最长的有效障碍赛跑路线](https://leetcode.cn/problems/find-the-longest-valid-obstacle-course-at-each-position/) · Hard · 灵茶山艾府：[计算每个前缀的最长非降子序列的长度](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1964.找出到每个位置为止最长的优先障碍赛跑线路

[力扣](https://leetcode-cn.com/problems/find-the-longest-valid-obstacle-course-at-each-position/)

题目实际上就是要找出以每个位置为结尾的最长上升子序列的长度，由于本题的数据规模较大，因此只能采用O(nlogn)的贪心加二分的做法。

具体思路也比较简单，对于当前位置上的数x：

如果其能加入到现有的最长上升子序列的尾部，那么就将其加进去并更新答案。

如果不能，那么在当前的最长上升子序列中必然存在至少一个数大于当前位置上的数。找到其中最小的那个，设其在当前最长上升子序列中的位置为p，那么x就可以加在当前最长上升子序列中第p - 1个数的后面，因此此时应该使用p + 1来更新答案。另一方面，对于x后面的数而言，使用x来替代最长上升子序列中第p个数显然是更优的选择，因此在这里还需要用x来替代最长上升子序列中p这个位置上的数。

对于找p的操作，则可以利用当前最长上升子序列的有序性，使用二分法在logn的时间内找到p。

最后附上python代码：

```python
class Solution(object):
    def longestObstacleCourseAtEachPosition(self, obstacles):
        """
        :type obstacles: List[int]
        :rtype: List[int]
        """

        res = [1]
        now = [obstacles[0]]
        for obstacle in obstacles[1:]:
            if obstacle >= now[-1]:
                res.append(len(now) + 1)
                now.append(obstacle)
            else:
                l = 0
                r = len(now) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if now[mid] <= obstacle:
                        l = mid + 1
                    else:
                        r = mid
                
                res.append(l + 1)
                now[l] = obstacle

        return res
```
