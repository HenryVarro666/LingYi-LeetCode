---
title: "1868. 两个行程编码数组的积"
aliases: ["yiduobo的每日leetcode 1868.两个行程编码数组的积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622411195"
zhihu_id: "622411195"
zhihu_title: "yiduobo的每日leetcode 1868.两个行程编码数组的积"
question_id: "1868"
question: "两个行程编码数组的积"
problem_url: "https://leetcode.cn/problems/product-of-two-run-length-encoded-arrays/"
created: "2023-04-16T23:25:36+08:00"
updated: "2023-04-16T23:25:36+08:00"
upvotes: 0
comments: 0
---

# 1868. 两个行程编码数组的积

> **[yiduobo的每日leetcode 1868.两个行程编码数组的积](https://zhuanlan.zhihu.com/p/622411195) · 知乎 · 2023-04-16 · 赞同 0**
> 力扣：[1868. 两个行程编码数组的积](https://leetcode.cn/problems/product-of-two-run-length-encoded-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1868.两个行程编码数组的积

[力扣](https://leetcode.cn/problems/product-of-two-run-length-encoded-arrays/)

直接套用二路归并的思路，不过在执行过程中除了需要记录两路的下标p1以及p2之外，在这里还需要额外维护当前p1和p2对应的数值中还剩余几个数没有被使用过，分别记为cnt1和cnt2。

接下来，只需要取cnt1和cnt2中的较小值cnt，将encode1[p1]的val以及encode2[p2]的val相乘作为新的val，将这一组[val, cnt]加入到答案中。在这里需要特别注意的是，若这个新的val与答案数组中最后的val相同，那么只需要cnt累加到答案数组的最后，否则就需要额外添加一组[val, cnt]。

若此时的cnt1为0，那么就将p1向后移动，然后将cnt1更新为encode1[p1]的freq；类似的，若此时的cnt2为0，那么就将p2向后移动，然后将cnt2更新为encode2[p2]的freq。

由于题目保证了两个数组的完整长度相同，那么p1和p2必然是同时到达数组末尾的，不需要考虑仅有一方消耗完的情况。

最后附上python代码：

```python
class Solution(object):
    def findRLEArray(self, encoded1, encoded2):
        """
        :type encoded1: List[List[int]]
        :type encoded2: List[List[int]]
        :rtype: List[List[int]]
        """

        p1 = p2 = 0
        cnt1, cnt2 = encoded1[0][1], encoded2[0][1]

        res = []
        while p1 < len(encoded1) and p2 < len(encoded2):
            v = encoded1[p1][0] * encoded2[p2][0]
            cnt = min(cnt1, cnt2)

            cnt1 -= cnt
            cnt2 -= cnt

            if cnt1 == 0:
                p1 += 1
                if p1 < len(encoded1):
                    cnt1 = encoded1[p1][1]
            
            if cnt2 == 0:
                p2 += 1
                if p2 < len(encoded2):
                    cnt2 = encoded2[p2][1]
            
            if res and res[-1][0] == v:
                res[-1][1] += cnt
            else:
                res.append([v, cnt])
        
        return res
```
