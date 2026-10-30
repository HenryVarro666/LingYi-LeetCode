---
title: "3880. 两个值之间的最小绝对差值"
aliases: ["yiduobo的每日leetcode 3880.两个值之间的最小绝对差值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2021745847470170429"
zhihu_id: "2021745847470170429"
zhihu_title: "yiduobo的每日leetcode 3880.两个值之间的最小绝对差值"
question_id: "3880"
question: "两个值之间的最小绝对差值"
problem_url: "https://leetcode.cn/problems/minimum-absolute-difference-between-two-values/"
difficulty: "Easy"
rating: 1257
created: "2026-03-30T00:36:51+08:00"
updated: "2026-03-30T00:36:52+08:00"
upvotes: 0
comments: 0
---

# 3880. 两个值之间的最小绝对差值

> **[yiduobo的每日leetcode 3880.两个值之间的最小绝对差值](https://zhuanlan.zhihu.com/p/2021745847470170429) · 知乎 · 2026-03-30 · 赞同 0**
> 力扣：[3880. 两个值之间的最小绝对差值](https://leetcode.cn/problems/minimum-absolute-difference-between-two-values/) · Easy · 灵茶山艾府：[O(n) 做法：枚举右，维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3880.两个值之间的最小绝对差值

<https://leetcode.cn/problems/minimum-absolute-difference-between-two-values/description/>

题目给出一个仅包含0、1、2的整数数组nums。

对于一组下标对(p, q)，若nums[p]为1，同时nums[q]为2，那么就称下标对(p, q)为有效的。

现在要求找出所有有效下标对中p和q之间的最小绝对差。若不存在有效下标对，则返回-1。

对于一组合法的(p, q)，若p \< q，那么q必然是与q左侧最后一次出现的p，也就是1上次出现的位置对应的p组队才是最优的；反之，若p > q，那么p必然是与p左侧最后一次出现的q，也就是2上次出现的位置对应的q组队才是最优的。

基于这一点，就可以使用两个变量last_one和last_two，记录1和2最后一次出现的位置。接下来一趟遍历，对于当前遍历到的nums[index]，若其遍历到的是1或者2，则更新last_one或者last_two为index，然后使用last_one与last_two的绝对差更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minAbsoluteDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        last_one = None
        last_two = None

        res = -1
        for index, v in enumerate(nums):
            if v == 1 or v == 2:
                if v == 1:
                    last_one = index
                else:
                    last_two = index
            
                if last_one is not None and last_two is not None:
                    dis = abs(last_one - last_two)
                    if res == -1 or res > dis:
                        res = dis
        
        return res
```
