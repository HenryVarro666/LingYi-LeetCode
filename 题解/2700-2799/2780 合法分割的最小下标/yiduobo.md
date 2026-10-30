---
title: "2780. 合法分割的最小下标"
aliases: ["yiduobo的每日leetcode 2780.合法分割的最小下标"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/动态规划", "题单/数学算法", "题单/动态规划/专题-前后缀分解", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655916020"
zhihu_id: "655916020"
zhihu_title: "yiduobo的每日leetcode 2780.合法分割的最小下标"
question_id: "2780"
question: "合法分割的最小下标"
problem_url: "https://leetcode.cn/problems/minimum-index-of-a-valid-split/"
difficulty: "Medium"
rating: 1550
created: "2023-09-13T04:19:25+08:00"
updated: "2023-09-13T04:19:25+08:00"
upvotes: 0
comments: 0
---

# 2780. 合法分割的最小下标

> **[yiduobo的每日leetcode 2780.合法分割的最小下标](https://zhuanlan.zhihu.com/p/655916020) · 知乎 · 2023-09-13 · 赞同 0**
> 力扣：[2780. 合法分割的最小下标](https://leetcode.cn/problems/minimum-index-of-a-valid-split/) · Medium · 灵茶山艾府：[结论证明+枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2780.合法分割的最小下标

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-index-of-a-valid-split/)

首先，如果一个数组中存在支配元素，那么这个支配元素必然是唯一的，因为其出现次数已经超过了数组长度的一半，若存在两个或更多的支配元素，这些元素出现次数之和就会大于数组的长度。

接下来，对于两个子数组而言，若这两个子数组的支配元素相同，那么其必然是整个数组的支配元素，这一点同样可以通过出现次数来进行说明。

有了上面的结论，就可以一趟遍历，找出支配元素x以及其出现的次数tot。接下来再进行一趟遍历，枚举左侧子数组的右边界index，同时在枚举的过程中统计左侧子数组中x出现的次数cnt。

若某个index满足cnt \* 2 > index + 1，且(tot - cnt) \* 2 > n - index - 1，那么index就是对应的答案。若遍历完整个数组还没找到答案，那么说明无法划分子数组，此时应该返回-1。

最后附上python代码：

```python
class Solution(object):
    def minimumIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        x = nums[0]
        cnt = 1
        for v in nums[1:]:
            if v == x:
                cnt += 1
            elif cnt > 0:
                cnt -= 1
            else:
                x = v
                cnt = 1
        
        tot = 0
        for v in nums:
            if v == x:
                tot += 1
        
        cnt = 0
        for index, v in enumerate(nums):
            if v == x:
                cnt += 1
            
            if cnt * 2 > index + 1 and (tot - cnt) * 2 > len(nums) - index - 1:
                return index
        
        return -1
```
