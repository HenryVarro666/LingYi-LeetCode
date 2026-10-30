---
title: "2808. 使循环数组所有元素相等的最少秒数"
aliases: ["yiduobo的每日leetcode 2808.使循环数组所有元素相等的最少秒数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657928864"
zhihu_id: "657928864"
zhihu_title: "yiduobo的每日leetcode 2808.使循环数组所有元素相等的最少秒数"
question_id: "2808"
question: "使循环数组所有元素相等的最少秒数"
problem_url: "https://leetcode.cn/problems/minimum-seconds-to-equalize-a-circular-array/"
difficulty: "Medium"
created: "2023-09-23T06:05:36+08:00"
updated: "2023-09-23T06:05:36+08:00"
upvotes: 0
comments: 0
---

# 2808. 使循环数组所有元素相等的最少秒数

> **[yiduobo的每日leetcode 2808.使循环数组所有元素相等的最少秒数](https://zhuanlan.zhihu.com/p/657928864) · 知乎 · 2023-09-23 · 赞同 0**
> 力扣：[2808. 使循环数组所有元素相等的最少秒数](https://leetcode.cn/problems/minimum-seconds-to-equalize-a-circular-array/) · Medium · 灵茶山艾府：[把问题看成是【扩散】元素（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2808.使循环数组所有元素相等的最少秒数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-seconds-to-equalize-a-circular-array/)

题目要求让循环数组所有值都变为同一个值，那么不妨枚举这个值是什么，然后计算将循环数组变为这个值需要的步数。

不妨设当前的目标值为target，那么问题就相当于从数组中所有原始值为target的位置出发，每一轮向左右两侧进行bfs直到遍历完整个数组位置。若数组中只有一个target，那么轮次就是数组长度除以2，而当数组中target数量大于等于两个时，最后遍历到的位置必然是某两个相邻target之间的正中间位置，而需要步数则是两个下标之间距离除以2。

根据这一点，就可以先一趟遍历，使用哈希表将每个数出现的位置都收集起来，然后遍历目标数target，然后枚举target出现的相邻位置组，并通过上面的结论计算需要的最大步数然后更新答案。另外需要注意这是一个环形数组，因此不要忘了计算头尾两个位置之间距离除以2的结果。

最后附上python代码：

```python
class Solution(object):
    def minimumSeconds(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        pos = {}
        for index, v in enumerate(nums):
            if v not in pos:
                pos[v] = []
            pos[v].append(index)
        
        res = None
        for v in pos:
            if len(pos[v]) == 1:
                if res is None or res > len(nums)/ 2:
                    res = len(nums) / 2
            else:
                ma = (len(nums) - 1 - pos[v][-1] + pos[v][0] + 1) / 2
                for index in range(1, len(pos[v])):
                    ma = max(ma, (pos[v][index] - pos[v][index - 1]) / 2)
                
                if res is None or res > ma:
                    res = ma
        
        return res
```
