---
title: "2731. 移动机器人"
aliases: ["yiduobo的每日leetcode 2731.移动机器人"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652431972"
zhihu_id: "652431972"
zhihu_title: "yiduobo的每日leetcode 2731.移动机器人"
question_id: "2731"
question: "移动机器人"
problem_url: "https://leetcode.cn/problems/movement-of-robots/"
difficulty: "Medium"
rating: 1923
created: "2023-08-26T01:07:37+08:00"
updated: "2023-08-26T01:07:37+08:00"
upvotes: 0
comments: 0
---

# 2731. 移动机器人

> **[yiduobo的每日leetcode 2731.移动机器人](https://zhuanlan.zhihu.com/p/652431972) · 知乎 · 2023-08-26 · 赞同 0**
> 力扣：[2731. 移动机器人](https://leetcode.cn/problems/movement-of-robots/) · Medium · 灵茶山艾府：[脑筋急转弯+排序统计（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2731.移动机器人

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/movement-of-robots/)

由于题目中的机器人之间是没有差异的，那么当两个机器人相遇时，完全可以将二者互换后再折返，这样一来就相当于什么都没有发生。换言之，本题中的机器人就可以认为是各走各的互不干扰，于是可以一趟遍历，计算出所有机器人的最终坐标。

接下来需要计算两两间的距离之和，在这里不妨先将机器人按最终坐标从小到大进行排序然后再从中找规律。可以发现，排序后下标为k的机器人，其左侧还有下标0到下标k - 1这一共k个机器人，那么这个下标为k的机器人就会被当做被减数k次。同样的，对于排序后下标为n - k - 1的机器人，其右侧还有下标n - k到下标n - 1这一共k个机器人，那么这个下标为n - k - 1的机器人就会被当做减数k次。综合起来，就可以从1到n - 1枚举这个k，首先将k个排序后的nums[k]累加到答案中，再将k个排序后的nums[-k - 1]从答案中减去。

最后附上python代码：

```python
class Solution(object):
    def sumDistance(self, nums, s, d):
        """
        :type nums: List[int]
        :type s: str
        :type d: int
        :rtype: int
        """

        for index, char in enumerate(s):
            if char == 'R':
                nums[index] += d
            else:
                nums[index] -= d
        
        nums.sort()
        res = 0
        mod = 10 ** 9 + 7
        for index in range(1, len(nums)):
            res = (res + nums[index] * index) % mod
            res = (res - nums[-index - 1] * index % mod + mod) % mod
        
        return res
```
