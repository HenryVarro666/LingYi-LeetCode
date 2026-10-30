---
title: "135. 分发糖果"
aliases: ["yiduobo的每日leetcode 135.分发糖果"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/面试经典-150-题", "题单/滑动窗口与双指针/六-分组循环", "题单/贪心算法/五-思维题", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141642285"
zhihu_id: "141642285"
zhihu_title: "yiduobo的每日leetcode 135.分发糖果"
question_id: "135"
question: "分发糖果"
problem_url: "https://leetcode.cn/problems/candy/"
difficulty: "Hard"
created: "2020-05-17T23:05:31+08:00"
updated: "2020-05-17T23:05:31+08:00"
upvotes: 0
comments: 0
---

# 135. 分发糖果

> **[yiduobo的每日leetcode 135.分发糖果](https://zhuanlan.zhihu.com/p/141642285) · 知乎 · 2020-05-17 · 赞同 0**
> 力扣：[135. 分发糖果](https://leetcode.cn/problems/candy/) · Hard · 灵茶山艾府：[分组循环，把困难题变成简单题，一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

135.分发糖果<https://leetcode-cn.com/problems/candy/>

对于一个小朋友来说，如果评分高于左侧小朋友，那么拿的糖果数也要比左侧小朋友多，右侧也是同样的逻辑。

于是可以先假设每个小朋友拿了一颗糖果，从左往右扫描一趟，先计算出每个小朋友与其左侧小朋友的比较时所需的最少糖果数，然后再从右往左扫描一趟，计算出与右侧小朋友比较所需的最少糖果数，最后取其中的较大值作为最终拿到的糖果数即可。

最后附上python代码：

```python
class Solution(object):
    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """

        if not ratings:
            return 0

        left_level = [1] * len(ratings)
        right_level = [1] * len(ratings)

        for index in range(1, len(ratings)):
            if ratings[index] > ratings[index - 1]:
                left_level[index] = left_level[index - 1] + 1
        
        for index in range(len(ratings) - 2, -1, -1):
            if ratings[index] > ratings[index + 1]:
                right_level[index] = right_level[index + 1] + 1
        
        res = 0
        for index in range(len(ratings)):
            res += max(left_level[index], right_level[index])

        return res
```
