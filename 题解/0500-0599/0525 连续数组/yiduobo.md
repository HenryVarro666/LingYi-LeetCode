---
title: "525. 连续数组"
aliases: ["yiduobo的每日leetcode 525.连续数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261131396"
zhihu_id: "261131396"
zhihu_title: "yiduobo的每日leetcode 525.连续数组"
question_id: "525"
question: "连续数组"
problem_url: "https://leetcode.cn/problems/contiguous-array/"
difficulty: "Medium"
created: "2020-10-02T19:36:23+08:00"
updated: "2020-10-02T19:36:23+08:00"
upvotes: 0
comments: 0
---

# 525. 连续数组

> **[yiduobo的每日leetcode 525.连续数组](https://zhuanlan.zhihu.com/p/261131396) · 知乎 · 2020-10-02 · 赞同 0**
> 力扣：[525. 连续数组](https://leetcode.cn/problems/contiguous-array/) · Medium · 灵茶山艾府：[式子变形 + 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

525.连续数组<https://leetcode-cn.com/problems/contiguous-array/>

对于这类求解连续数组的题目，一个常见的思路是将数组区间问题转化为前缀和问题。对于这个题目，要求l到r这一段中0和1的个数相等，可以看做0到l - 1这一段中0和1个数的差值等于0到r这一段中0和1个数的差值，于是就可以使用类似前缀和的做法求解。

具体来说就是维护一个diff数组，其中diff[index]表示nums[0]到nums[index]这一段中0的个数减去1的个数，然后用一个dict保存每种diff第一次出现的位置。接下来从左往右一趟扫描，求解当前的diff[index]。

若diff\[index\]没有在dict中出现过，那么将其加入到dict中。若已经出现过，那么表示从dict\[diff\[index\]\] + 1到index这一段中的0和1数量是相等的，于是可以计算这一段区间的长度并更新答案。

最后附上python代码：

```python
class Solution(object):
    def findMaxLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        prefix_dict = {0: -1}
        now = 0
        res = 0

        for index, num in enumerate(nums):
            if num == 0:
                now += 1
            else:
                now -= 1
            if now in prefix_dict:
                res = max(res, index - prefix_dict[now])
            else:
                prefix_dict[now] = index

        return res
```
