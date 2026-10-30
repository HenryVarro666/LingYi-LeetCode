---
title: "81. 搜索旋转排序数组II"
aliases: ["yiduobo的每日leetcode 81.搜索旋转排序数组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134170456"
zhihu_id: "134170456"
zhihu_title: "yiduobo的每日leetcode 81.搜索旋转排序数组II"
question_id: "81"
question: "搜索旋转排序数组 II"
problem_url: "https://leetcode.cn/problems/search-in-rotated-sorted-array-ii/"
difficulty: "Medium"
created: "2020-04-21T23:22:19+08:00"
updated: "2020-04-21T23:22:19+08:00"
upvotes: 1
comments: 0
---

# 81. 搜索旋转排序数组II

> **[yiduobo的每日leetcode 81.搜索旋转排序数组II](https://zhuanlan.zhihu.com/p/134170456) · 知乎 · 2020-04-21 · 赞同 1**
> 力扣：[81. 搜索旋转排序数组 II](https://leetcode.cn/problems/search-in-rotated-sorted-array-ii/) · Medium · 灵茶山艾府：[基于 33 题的简洁写法，只需增加一个 if（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

81.搜索旋转排序数组II <https://leetcode-cn.com/problems/search-in-rotated-sorted-array-ii/>

1.0版本的传送门在这里([yiduobo：yiduobo的每日leetcode 33.搜算旋转排序数组](https://zhuanlan.zhihu.com/p/120368744))

这里题目表示可以包含重复的数字，那么在进行二分时就无法确定当前部分是否有过旋转操作了。例如[0, 0, 0, 0, 0, 0, 1]这个数组，旋转成[0, 1, 0, 0, 0, 0, 0]之后，此时进行二分会发现二分的边界全都是0，根本无从判断那个部分是经历过旋转操作的，因此1.0版本中的二分法在这里是行不通的。

因此，这里最好的时间复杂度就是O(n)，一边扫描判断即可。

最后附上python代码：

```python
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: bool
        """

        for num in nums:
            if num == target:
                return True

        return False
```

当然，这个问题主要考察的是思路的变化。
