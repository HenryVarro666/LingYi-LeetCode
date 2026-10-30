---
title: "3917. 统计下标的相反奇偶性得分"
aliases: ["yiduobo的每日leetcode 3917.统计下标的相反奇偶性得分"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2034756137963233465"
zhihu_id: "2034756137963233465"
zhihu_title: "yiduobo的每日leetcode 3917.统计下标的相反奇偶性得分"
question_id: "3917"
question: "统计下标的相反奇偶性得分"
problem_url: "https://leetcode.cn/problems/count-indices-with-opposite-parity/"
difficulty: "Easy"
created: "2026-05-04T22:11:37+08:00"
updated: "2026-05-04T22:11:38+08:00"
upvotes: 3
comments: 0
---

# 3917. 统计下标的相反奇偶性得分

> **[yiduobo的每日leetcode 3917.统计下标的相反奇偶性得分](https://zhuanlan.zhihu.com/p/2034756137963233465) · 知乎 · 2026-05-04 · 赞同 3**
> 力扣：[3917. 统计下标的相反奇偶性得分](https://leetcode.cn/problems/count-indices-with-opposite-parity/) · Easy · 灵茶山艾府：[O(n) 做法：枚举左，维护右（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3917.统计下标的相反奇偶性得分

<https://leetcode.cn/problems/count-indices-with-opposite-parity/description/>

题目给出一个长度为n的整数数组nums。

下标i的分数定义为满足以下条件的下标j的数量：

- i \< j \< n
- nums[i]和nums[j]的奇偶性不同

要求返回一个长度为n的整数数组answer，其中answer[i]表示下标i的得分。

对于每个下标，其得分实际上就是其右侧的后缀中奇数或者偶数的数量。于是可以从后往前一趟遍历，使用一个长度为2的数组cnt维护后缀中偶数与奇数的数量。对于当前遍历到的元素v，其得分就是cnt[1 - v % 2]，更新答案后，将cnt[v % 2]加上1然后继续向前遍历即可。

最后附上python代码：

```python
class Solution(object):
    def countOppositeParity(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        cnt = [0, 0]
        res = []
        for v in nums[::-1]:
            v %= 2
            res.append(cnt[1 - v])
            cnt[v] += 1
        
        return res[::-1]
```
