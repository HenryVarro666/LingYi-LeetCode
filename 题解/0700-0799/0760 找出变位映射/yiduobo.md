---
title: "760. 找出变位映射"
aliases: ["yiduobo的每日leetcode 760.找出变位映射"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/606096459"
zhihu_id: "606096459"
zhihu_title: "yiduobo的每日leetcode 760.找出变位映射"
question_id: "760"
question: "找出变位映射"
problem_url: "https://leetcode.cn/problems/find-anagram-mappings/"
created: "2023-02-14T00:37:34+08:00"
updated: "2023-02-14T00:37:34+08:00"
upvotes: 0
comments: 0
---

# 760. 找出变位映射

> **[yiduobo的每日leetcode 760.找出变位映射](https://zhuanlan.zhihu.com/p/606096459) · 知乎 · 2023-02-14 · 赞同 0**
> 力扣：[760. 找出变位映射](https://leetcode.cn/problems/find-anagram-mappings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

760.找出变位映射

[力扣](https://leetcode.cn/problems/find-anagram-mappings/)

首先对nums2进行一趟遍历，使用哈希表记录nums2中每个数出现的所有下标位置，接下来对nums1进行一趟遍历，根据哈希表中记录的位置填充最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def anagramMappings(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        pos = {}
        for index, num in enumerate(nums2):
            if num not in pos:
                pos[num] = []
            pos[num].append(index)
        
        res = []
        for num in nums1:
            res.append(pos[num][-1])
            pos[num].pop()
        
        return res
```
