---
title: "1331. 数组序号转换"
aliases: ["yiduobo的每日leetcode 1331.数组序号转换"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/binary-search", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394985717"
zhihu_id: "394985717"
zhihu_title: "yiduobo的每日leetcode 1331.数组序号转换"
question_id: "1331"
question: "数组序号转换"
problem_url: "https://leetcode.cn/problems/rank-transform-of-an-array/"
difficulty: "Easy"
created: "2021-07-31T17:26:18+08:00"
updated: "2021-07-31T17:26:18+08:00"
upvotes: 0
comments: 0
---

# 1331. 数组序号转换

> **[yiduobo的每日leetcode 1331.数组序号转换](https://zhuanlan.zhihu.com/p/394985717) · 知乎 · 2021-07-31 · 赞同 0**
> 力扣：[1331. 数组序号转换](https://leetcode.cn/problems/rank-transform-of-an-array/) · Easy · 灵茶山艾府：[【模板】离散化的两种写法：二分查找 / 哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1331.数组序号转换

[力扣](https://leetcode-cn.com/problems/rank-transform-of-an-array/)

比较基础的题目，将原数组从小到大进行排序，然后依次对第一次出现的数字进行编号，并建立数字到编号的映射，然后通过映射将原数组转化为序号数组返回即可。

最后附上python代码：

```python
class Solution(object):
    def arrayRankTransform(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        pos_dict = {}
        now = None
        cnt = 0
        for num in sorted(arr):
            if num != now:
                cnt += 1
                pos_dict[num] = cnt
                now = num
        
        return [pos_dict[num] for num in arr]
```
