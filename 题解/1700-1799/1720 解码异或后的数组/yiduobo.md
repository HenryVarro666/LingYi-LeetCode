---
title: "1720. 解码异或后的数组"
aliases: ["yiduobo的每日leetcode 1720.解码异或后的数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/451019238"
zhihu_id: "451019238"
zhihu_title: "yiduobo的每日leetcode 1720.解码异或后的数组"
question_id: "1720"
question: "解码异或后的数组"
problem_url: "https://leetcode.cn/problems/decode-xored-array/"
created: "2021-12-29T00:31:41+08:00"
updated: "2021-12-29T00:31:41+08:00"
upvotes: 0
comments: 0
---

# 1720. 解码异或后的数组

> **[yiduobo的每日leetcode 1720.解码异或后的数组](https://zhuanlan.zhihu.com/p/451019238) · 知乎 · 2021-12-29 · 赞同 0**
> 力扣：[1720. 解码异或后的数组](https://leetcode.cn/problems/decode-xored-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1720.解码异或后的数组

[力扣](https://leetcode-cn.com/problems/decode-xored-array/)

由于异或运算满足交换律，另外还满足a^a \= 0，那么对于encode[i] \= arr[i] ^ arr[i + 1]这个式子而言，可以在两侧都异或上arr[i]，那么就有encode[i] ^ arr[i] \= arr[i] ^ arr[i + 1] ^ arr[i] \= (arr[i] ^ arr[i]) ^ arr[i + 1] \= arr[i + 1]，也就是说通过encode[i]与arr[i]可以计算出arr[i + 1]。

题目在这里给出了encode数组和arr[0]，那么可以通过上面的式子一趟扫描，逐个求出arr中的数。

最后附上python代码：

```python
class Solution(object):
    def decode(self, encoded, first):
        """
        :type encoded: List[int]
        :type first: int
        :rtype: List[int]
        """

        res = [first]
        for num in encoded:
            res.append(res[-1] ^ num)
        
        return res
```
