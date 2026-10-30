---
title: "1734. 解码异或后的排列"
aliases: ["yiduobo的每日leetcode 1734.解码异或后的排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452672111"
zhihu_id: "452672111"
zhihu_title: "yiduobo的每日leetcode 1734.解码异或后的排列"
question_id: "1734"
question: "解码异或后的排列"
problem_url: "https://leetcode.cn/problems/decode-xored-permutation/"
created: "2022-01-02T22:22:47+08:00"
updated: "2022-01-02T22:22:47+08:00"
upvotes: 0
comments: 0
---

# 1734. 解码异或后的排列

> **[yiduobo的每日leetcode 1734.解码异或后的排列](https://zhuanlan.zhihu.com/p/452672111) · 知乎 · 2022-01-02 · 赞同 0**
> 力扣：[1734. 解码异或后的排列](https://leetcode.cn/problems/decode-xored-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1734.解码异或后的排列

[力扣](https://leetcode-cn.com/problems/decode-xored-permutation/)

注意到题目给出的encoded[i] \= perm[i] ^ perm[i + 1]，又由于n是个奇数，那么就可以将encoded[1]、encoded[3]、...、encoded[n - 2]这些奇数项拎出来异或在一起，就有

x \= encoded[1] ^ encoded[3] ^ ... ^ encoded[n - 2] \=

(perm[1] ^ perm[2]) ^ (perm[3] ^ perm[4]) ^ ... ^ (perm[n - 2] ^ perm[n - 1]) \=

perm[1] ^ perm[2] ^ ... ^ perm[n - 2] ^ perm[n - 1]

由于perm是n的某个排列，因此

y \= perm[0] ^ perm[1] ^ perm[2] ^ ... ^ perm[n - 1]

\= 1 ^ 2 ^ ... ^ n

对于x和y这两个式子，二者只差了一项perm[0]，那么将二者异或起来，就有

perm[0] \= x ^ y \= encoded[1] ^ encoded[3] ^ ... ^ encoded[n - 2] ^ 1 ^ 2 ^ ... ^ n

至此就计算出了perm[0]。接下来就可以从头开始向后扫描encoded，根据当前的encoded[i]以及perm[i]计算出后续所有的perm[i + 1]了。

最后附上python代码：

```python
class Solution(object):
    def decode(self, encoded):
        """
        :type encoded: List[int]
        :rtype: List[int]
        """

        n = len(encoded) + 1

        res = [0]
        for index in range(1, n + 1):
            res[0] ^= index
        for index in range(1, n - 1, 2):
            res[0] ^= encoded[index]
        for num in encoded:
            res.append(res[-1] ^ num)
        
        return res
```
