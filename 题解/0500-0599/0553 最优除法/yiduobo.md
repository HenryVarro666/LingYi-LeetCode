---
title: "553. 最优除法"
aliases: ["yiduobo的每日leetcode 553.最优除法"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/264806210"
zhihu_id: "264806210"
zhihu_title: "yiduobo的每日leetcode 553.最优除法"
question_id: "553"
question: "最优除法"
problem_url: "https://leetcode.cn/problems/optimal-division/"
created: "2020-10-11T14:07:56+08:00"
updated: "2020-10-11T14:07:56+08:00"
upvotes: 0
comments: 0
---

# 553. 最优除法

> **[yiduobo的每日leetcode 553.最优除法](https://zhuanlan.zhihu.com/p/264806210) · 知乎 · 2020-10-11 · 赞同 0**
> 力扣：[553. 最优除法](https://leetcode.cn/problems/optimal-division/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

553.最优除法<https://leetcode-cn.com/problems/optimal-division/>

乍一看以为是搜索回溯的题目，但是仔细一想应该用数学方法来处理。

对于a/b/c/...这个式子而言，第一项a必然是分子的一个乘数，而第二项b必然是分母的一个乘数。由于题目保证这里面的数都是正整数，那么要是最后的结果最大，我们就需要尽可能地将从c开始的所有数乘到分子上去。一个直观的想法就是将其改成形如a/(b/c/...)这样的式子。

另外，需要注意判断只有a和只有a、b的情况。

最后附上python代码：

```python
class Solution(object):
    def optimalDivision(self, nums):
        """
        :type nums: List[int]
        :rtype: str
        """

        if len(nums) == 1:
            return str(nums[0])
        
        if len(nums) == 2:
            return str(nums[0]) + '/' + str(nums[1])
        
        return str(nums[0]) + '/(' + '/'.join([str(x) for x in nums[1:]]) + ')'
```
