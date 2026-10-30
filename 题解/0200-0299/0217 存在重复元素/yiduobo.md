---
title: "217. 存在重复元素"
aliases: ["yiduobo的每日leetcode 217.存在重复元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148267563"
zhihu_id: "148267563"
zhihu_title: "yiduobo的每日leetcode 217.存在重复元素"
question_id: "217"
question: "存在重复元素"
problem_url: "https://leetcode.cn/problems/contains-duplicate/"
difficulty: "Easy"
created: "2020-06-14T19:19:39+08:00"
updated: "2020-06-14T19:19:39+08:00"
upvotes: 0
comments: 0
---

# 217. 存在重复元素

> **[yiduobo的每日leetcode 217.存在重复元素](https://zhuanlan.zhihu.com/p/148267563) · 知乎 · 2020-06-14 · 赞同 0**
> 力扣：[217. 存在重复元素](https://leetcode.cn/problems/contains-duplicate/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

217.存在重复元素<https://leetcode-cn.com/problems/contains-duplicate/>

比较基础的题目，排序后查找或者使用树、哈希表之类的都行，我在这里用的set。

最后附上python代码：

```python
class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        num_set = set()
        for num in nums:
            if num in num_set:
                return True
            num_set.add(num)

        return False
```
