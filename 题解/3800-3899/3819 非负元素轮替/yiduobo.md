---
title: "3819. 非负元素轮替"
aliases: ["yiduobo的每日leetcode 3819.非负元素轮替"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1998873200818411256"
zhihu_id: "1998873200818411256"
zhihu_title: "yiduobo的每日leetcode 3819.非负元素轮替"
question_id: "3819"
question: "非负元素轮替"
problem_url: "https://leetcode.cn/problems/rotate-non-negative-elements/"
difficulty: "Medium"
created: "2026-01-25T21:55:14+08:00"
updated: "2026-01-25T21:55:14+08:00"
upvotes: 0
comments: 0
---

# 3819. 非负元素轮替

> **[yiduobo的每日leetcode 3819.非负元素轮替](https://zhuanlan.zhihu.com/p/1998873200818411256) · 知乎 · 2026-01-25 · 赞同 0**
> 力扣：[3819. 非负元素轮替](https://leetcode.cn/problems/rotate-non-negative-elements/) · Medium · 灵茶山艾府：[模拟，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3819.非负元素轮替

<https://leetcode.cn/problems/rotate-non-negative-elements/description/>

题目给出一个整数数组nums以及一个整数k。

现在要求将数组中所有的非负元素，按照循环的方式向左轮替k个位置，负数元素则保持不变。

问处理后的数组是什么。

按照题目的描述，仅对非负元素做轮替操作，因此可以先一趟遍历，将nums中的非负元素提取出来，得到数组pos。

若pos为空，说明没有元素需要操作，此时直接返回nums即可。

反之，则需要对pos进行轮替操作。

首先，可以将k对len(pos)取模，因为pos向左轮替len(pos)个位置后pos保持不变，因此可以先让k对len(pos)取模。

接下来，需要对pos中的元素向左轮替k个位置，也就是pos[k]变为pos[0]、pos[k + 1]变为pos[1]、...，以此类推。将最后的pos[n - 1]移动到pos[n - k - 1]之后，就需要从头开始，将pos[0]移动到pos[n - k]、pos[1]移动到pos[n - k + 1]、...，以此类推。换言之，在这里就是将pos迭代为pos[k:] + pos[:k]。

得到轮替后的pos后，再次遍历nums，构造答案数组。若当前遍历到的元素v大于等于0，则将剩下的pos中的首个元素加入到答案中，否则将v加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def rotateElements(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        pos = []
        for v in nums:
            if v >= 0:
                pos.append(v)
        
        if not pos:
            return nums

        k %= len(pos)
        pos = pos[k:] + pos[:k]
        res = []
        p = 0
        for v in nums:
            if v < 0:
                res.append(v)
            else:
                res.append(pos[p])
                p += 1
        
        return res
```
