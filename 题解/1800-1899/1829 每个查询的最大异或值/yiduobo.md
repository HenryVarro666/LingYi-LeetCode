---
title: "1829. 每个查询的最大异或值"
aliases: ["yiduobo的每日leetcode 1829.每个查询的最大异或值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/467480069"
zhihu_id: "467480069"
zhihu_title: "yiduobo的每日leetcode 1829.每个查询的最大异或值"
question_id: "1829"
question: "每个查询的最大异或值"
problem_url: "https://leetcode.cn/problems/maximum-xor-for-each-query/"
created: "2022-02-14T23:14:01+08:00"
updated: "2022-02-14T23:14:01+08:00"
upvotes: 0
comments: 0
---

# 1829. 每个查询的最大异或值

> **[yiduobo的每日leetcode 1829.每个查询的最大异或值](https://zhuanlan.zhihu.com/p/467480069) · 知乎 · 2022-02-14 · 赞同 0**
> 力扣：[1829. 每个查询的最大异或值](https://leetcode.cn/problems/maximum-xor-for-each-query/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1829.每个查询的最大异或值

[力扣](https://leetcode-cn.com/problems/maximum-xor-for-each-query/)

题目中给出了数位的上限maximumBit，那么每一轮最终的目标就是maximumBit个1，在十进制表示下就是target \= 2^maximumBit - 1。由于每一轮都可以自由控制k的大小，因此每一轮都必然可以让结果成为target。

对于第index轮而言，要求的是

nums[0] ^ nums[1] ^ ... ^ num[n - index] ^ k \= target

也就是说对应的k为

k \= target ^ nums[0] ^ nums[1] ^ ... ^ nums[n - index]

注意到这里nums的处理是从后向前逐渐减少的前缀异或，那么在这里就可以倒过来处理，将其转化成正常向后增加的前缀异或。在计算前缀异或的同时得到对应的k并加入到答案中，全部处理完毕后再将答案翻转过来即可。

最后附上python代码：

```python
class Solution(object):
    def getMaximumXor(self, nums, maximumBit):
        """
        :type nums: List[int]
        :type maximumBit: int
        :rtype: List[int]
        """

        res = []
        now = 0
        target = (1 << maximumBit) - 1
        for num in nums:
            now ^= num
            res.append(target ^ now)
        
        res.reverse()
        return res
```
