---
title: "2006. 差的绝对值为K的数对数目"
aliases: ["yiduobo的每日leetcode 2006.差的绝对值为K的数对数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/503280330"
zhihu_id: "503280330"
zhihu_title: "yiduobo的每日leetcode 2006.差的绝对值为K的数对数目"
question_id: "2006"
question: "差的绝对值为 K 的数对数目"
problem_url: "https://leetcode.cn/problems/count-number-of-pairs-with-absolute-difference-k/"
difficulty: "Easy"
created: "2022-04-22T19:50:22+08:00"
updated: "2022-04-22T19:50:22+08:00"
upvotes: 0
comments: 0
---

# 2006. 差的绝对值为K的数对数目

> **[yiduobo的每日leetcode 2006.差的绝对值为K的数对数目](https://zhuanlan.zhihu.com/p/503280330) · 知乎 · 2022-04-22 · 赞同 0**
> 力扣：[2006. 差的绝对值为 K 的数对数目](https://leetcode.cn/problems/count-number-of-pairs-with-absolute-difference-k/) · Easy · 灵茶山艾府：[O(n) 做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2006.差的绝对值为K的数对数目

[力扣](https://leetcode-cn.com/problems/count-number-of-pairs-with-absolute-difference-k/)

比较基础的题目，一趟遍历，使用一个哈希表cnt_dict统计每个数出现的次数。

接下来再遍历哈希表中的所有数。对于当前遍历到的数num，与其差的绝对值为K的数可能是num - K或者num + K。为了避免重复，此时只需要考虑num与num + K，因为num与num - K的情况在遍历到num - K时就考虑过了。

对于num和num + K，二者分别出现了cnt_dict[num]以及cnt_dict[num + K]次，那么二者的乘积就是可以形成的合法数对的数目，将这些乘积累加起来就是最终的答案。

最后附上python代码：

```python
class Solution(object):
    def countKDifference(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        for num in cnt_dict:
            res += cnt_dict[num] * cnt_dict.get(num + k, 0)
        
        return res
```
