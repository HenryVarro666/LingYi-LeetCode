---
title: "1394. 找出数组中的幸运数"
aliases: ["yiduobo的每日leetcode 1394.找出数组中的幸运数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/404326198"
zhihu_id: "404326198"
zhihu_title: "yiduobo的每日leetcode 1394.找出数组中的幸运数"
question_id: "1394"
question: "找出数组中的幸运数"
problem_url: "https://leetcode.cn/problems/find-lucky-integer-in-an-array/"
difficulty: "Easy"
created: "2021-08-27T21:49:01+08:00"
updated: "2021-08-27T21:49:01+08:00"
upvotes: 1
comments: 0
---

# 1394. 找出数组中的幸运数

> **[yiduobo的每日leetcode 1394.找出数组中的幸运数](https://zhuanlan.zhihu.com/p/404326198) · 知乎 · 2021-08-27 · 赞同 1**
> 力扣：[1394. 找出数组中的幸运数](https://leetcode.cn/problems/find-lucky-integer-in-an-array/) · Easy · 灵茶山艾府：[两种方法：哈希表 / 数组（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1394.找出数组中的幸运数

[力扣](https://leetcode-cn.com/problems/find-lucky-integer-in-an-array/)

比较基础的题目，统计每个数出现的次数，然后遍历每个数，找出符合条件的数即可。

最后附上python代码：

```python
class Solution(object):
    def findLucky(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        cnt_list = [0] * 501
        for num in arr:
            cnt_list[num] += 1
        
        for num in range(500, 0, -1):
            if cnt_list[num] == num:
                return num
        
        return -1
```
