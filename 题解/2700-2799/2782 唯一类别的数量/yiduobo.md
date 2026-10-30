---
title: "2782. 唯一类别的数量"
aliases: ["yiduobo的每日leetcode 2782.唯一类别的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656138763"
zhihu_id: "656138763"
zhihu_title: "yiduobo的每日leetcode 2782.唯一类别的数量"
question_id: "2782"
question: "唯一类别的数量"
problem_url: "https://leetcode.cn/problems/number-of-unique-categories/"
created: "2023-09-14T03:07:36+08:00"
updated: "2023-09-14T03:07:36+08:00"
upvotes: 0
comments: 0
---

# 2782. 唯一类别的数量

> **[yiduobo的每日leetcode 2782.唯一类别的数量](https://zhuanlan.zhihu.com/p/656138763) · 知乎 · 2023-09-14 · 赞同 0**
> 力扣：[2782. 唯一类别的数量](https://leetcode.cn/problems/number-of-unique-categories/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2782.唯一类别的数量

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/number-of-unique-categories/)

使用一个数组sample来保存每种类别的一个实例，接下来从0开始进行遍历。对于当前遍历到的元素a，检测sample中是否存在某个元素b与a是同一类别。若不存在这样的b，说明a是一个新类别的元素，此时应该将a加入到sample中，反之则无需进行任何操作。

遍历完成后，sample的长度即为最终答案。

最后附上python代码：

```python
# Definition for a category handler.
# class CategoryHandler:
#     def haveSameCategory(self, a, b):
#         pass
class Solution(object):
    def numberOfCategories(self, n, categoryHandler):
        """
        :type n: int
        :type categoryHandler: CategoryHandler
        :rtype: int
        """

        sample = []
        for a in range(n):
            flag = True
            for b in sample:
                if categoryHandler.haveSameCategory(a, b):
                    flag = False
                    break
            
            if flag:
                sample.append(a)
        
        return len(sample)
```
