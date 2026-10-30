---
title: "4074. 和为目标值的最大乘积对"
aliases: ["yiduobo的每日leetcode 4074.和为目标值的最大乘积对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2093143182733268266"
zhihu_id: "2093143182733268266"
zhihu_title: "yiduobo的每日leetcode 4074.和为目标值的最大乘积对"
question_id: "4074"
question: "和为目标值的最大乘积对"
problem_url: "https://leetcode.cn/problems/maximum-product-pair-with-target-sum/"
created: "2026-10-13T01:06:10+08:00"
updated: "2026-10-13T01:06:13+08:00"
upvotes: 2
comments: 0
---

# 4074. 和为目标值的最大乘积对

> **[yiduobo的每日leetcode 4074.和为目标值的最大乘积对](https://zhuanlan.zhihu.com/p/2093143182733268266) · 知乎 · 2026-10-13 · 赞同 2**
> 力扣：[4074. 和为目标值的最大乘积对](https://leetcode.cn/problems/maximum-product-pair-with-target-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4074.和为目标值的最大乘积对

<https://leetcode.cn/problems/maximum-product-pair-with-target-sum/description/>

题目给出一个整数数组nums以及一个整数target。

对于一个二元组(i, j)，若nums[i]与nums[j]之和为target，且nums[i] > nums[j]，那么就称其为有效的。

要求返回一个乘积最大的有效二元组，若存在多个二元组的乘积同为最大，可以返回任意一个，若不存在，则返回[-1, -1]。

对于题目中有效二元组的条件，nums[i] > nums[j]这一条实际上可以理解成只要这两个元素不相等就行了，这样一来就一定有一个较小另一个较小，此时让较大的这一方作为nums[i]就行了。

基于这一点，就可以使用一个哈希表pos记录前缀中每种元素出现的位置，接下来一趟遍历，对于当前遍历到的v，若target - v与v不同且出现在pos中，那么就说当前下标index与target - v出现的位置，即pos[target - v]可以形成有效的二元组，此时则应该对比v \* (target - v)与当前答案二元组乘积的大小。若更大，则需要更新答案。至于index与pos[target - v]这两个下标谁来当i谁来当j，则需要通过对比v和target - v的大小来决定。

最后附上python代码：

```python
class Solution(object):
    def maxProductPair(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        
        pos = {}
        res = [-1, -1]
        for index, v in enumerate(nums):
            if (target - v) in pos and v != target - v and (res[0] == -1 or nums[res[0]] * nums[res[1]] < v * (target - v)):
                if v > target - v:
                    res = [index, pos[target - v]]
                else:
                    res = [pos[target - v], index]
            
            pos[v] = index
        
        return res
```
