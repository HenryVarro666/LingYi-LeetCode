---
title: "659. 分割数组为连续子序列"
aliases: ["yiduobo的每日leetcode 659.分割数组为连续子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/284099334"
zhihu_id: "284099334"
zhihu_title: "yiduobo的每日leetcode 659.分割数组为连续子序列"
question_id: "659"
question: "分割数组为连续子序列"
problem_url: "https://leetcode.cn/problems/split-array-into-consecutive-subsequences/"
created: "2020-11-10T22:57:31+08:00"
updated: "2020-11-10T22:57:31+08:00"
upvotes: 1
comments: 0
---

# 659. 分割数组为连续子序列

> **[yiduobo的每日leetcode 659.分割数组为连续子序列](https://zhuanlan.zhihu.com/p/284099334) · 知乎 · 2020-11-10 · 赞同 1**
> 力扣：[659. 分割数组为连续子序列](https://leetcode.cn/problems/split-array-into-consecutive-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

659.分割数组为连续子序列

[力扣](https://leetcode-cn.com/problems/split-array-into-consecutive-subsequences/)

首先，可以明确的一点就是对于一个数x而言，若现在已经有了以x - 1为结尾的连续子序列，那么我们应该将x加入其中。因为除了将x加入到以x - 1为结尾的连续子序列之外，我们就只能另起一条以x开头的新子序列了，而这条新的子序列只有在长度大于等于3时才合法，但即使是长度不够，这条新的子序列依然是可以接在以x - 1为结尾的连续子序列后面的。

有了上面的结论，我们就可以首先统计出每个数出现的次数，然后按从小到大的顺序遍历每个数。当然，这里的nums已经是有序的，省去了排序的工作。我们维护一个dict，其中dict[x]表示以x为结尾的合法子序列的数目。

接下来，对于遍历到的每个x：

1、若x已经被用完，那么我们直接考察下一个数。这里用完可能是因为在x - 2时已经用了一个x - 1和一个x用来组成以子序列。

2、若x没有用被完，且现在存在以x - 1为结尾的合法连续子序列。根据最开始的结论，我们应该将x加入其中一个以x - 1为结尾的子序列，此时x的数量减一，同时有一个以x - 1为结尾的子序列被转化为了以x为结尾的子序列。

3、若x没有被用完，且现在没有以x - 1为结尾的合法子序列。那么此时我们就只能靠x + 1以及x + 2组成全新的子序列。此时则需要判断是否还有没有完的x + 1和x + 2，若还有，那么就分别取一个然后构造出一个以x + 2为结尾的子序列；若没有，那么此时的x将无处安置，直接返回false即可。

如果能成功遍历完所有数字，说明所有数都有地方去，此时返回true。

```python
class Solution(object):
    def isPossible(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1

        last_dict = {}
        for num in nums:
            if num_dict[num] == 0:
                continue

            if last_dict.get(num - 1, 0) > 0:
                last_dict[num - 1] -= 1
                last_dict[num] = last_dict.get(num, 0) + 1
                num_dict[num] -= 1
            elif num_dict.get(num + 1, 0) > 0 and num_dict.get(num + 2, 0) > 0:
                last_dict[num + 2] = last_dict.get(num + 2, 0) + 1
                num_dict[num] -= 1
                num_dict[num + 1] -= 1
                num_dict[num + 2] -= 1
            else:
                return False

        return True
```
