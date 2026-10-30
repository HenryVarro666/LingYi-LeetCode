---
title: "1313. 解压缩编码列表"
aliases: ["yiduobo的每日leetcode 1313.解压缩编码列表"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392613935"
zhihu_id: "392613935"
zhihu_title: "yiduobo的每日leetcode 1313.解压缩编码列表"
question_id: "1313"
question: "解压缩编码列表"
problem_url: "https://leetcode.cn/problems/decompress-run-length-encoded-list/"
created: "2021-07-23T22:19:32+08:00"
updated: "2021-07-23T22:19:32+08:00"
upvotes: 0
comments: 0
---

# 1313. 解压缩编码列表

> **[yiduobo的每日leetcode 1313.解压缩编码列表](https://zhuanlan.zhihu.com/p/392613935) · 知乎 · 2021-07-23 · 赞同 0**
> 力扣：[1313. 解压缩编码列表](https://leetcode.cn/problems/decompress-run-length-encoded-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1313.解压缩编码列表

[力扣](https://leetcode-cn.com/problems/decompress-run-length-encoded-list/)

比较基础的题目，从头开始向后两两扫描，按题目给出的方式解码后输出即可。

最后附上python代码：

```python
class Solution(object):
    def decompressRLElist(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        res = []
        for index in range(0, n, 2):
            res.extend([nums[index + 1]] * nums[index])
        
        return res
```
