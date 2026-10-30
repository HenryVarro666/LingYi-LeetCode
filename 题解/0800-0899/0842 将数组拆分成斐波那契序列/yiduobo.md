---
title: "842. 将数组拆分成斐波那契序列"
aliases: ["yiduobo的每日leetcode 842.将数组拆分成斐波那契序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/347511002"
zhihu_id: "347511002"
zhihu_title: "yiduobo的每日leetcode 842.将数组拆分成斐波那契序列"
question_id: "842"
question: "将数组拆分成斐波那契序列"
problem_url: "https://leetcode.cn/problems/split-array-into-fibonacci-sequence/"
created: "2021-01-28T18:08:33+08:00"
updated: "2021-01-28T18:08:33+08:00"
upvotes: 0
comments: 0
---

# 842. 将数组拆分成斐波那契序列

> **[yiduobo的每日leetcode 842.将数组拆分成斐波那契序列](https://zhuanlan.zhihu.com/p/347511002) · 知乎 · 2021-01-28 · 赞同 0**
> 力扣：[842. 将数组拆分成斐波那契序列](https://leetcode.cn/problems/split-array-into-fibonacci-sequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

842.将数组拆分成斐波那契序列

[力扣](https://leetcode-cn.com/problems/split-array-into-fibonacci-sequence/)

并没有什么特别好的思路，不过好在这里给出的S长度比较短，因此可以直接枚举斐波那契数列的前两项，然后计算后面项的值并检测是否能与S匹配上。

需要特别注意的是，枚举的前两项值不能超过2^31 - 1，同时若长度超过1，那么必须满足最高位非0。另外，后续递推项的值也不能超过2^31 - 1。

最后附上python代码：

```python
class Solution(object):
    def splitIntoFibonacci(self, S):
        """
        :type S: str
        :rtype: List[int]
        """

        n = len(S)
        for i in range(n - 2):
            if i > 0 and S[0] == '0':
                break
            a = int(S[:i + 1])
            if a > 2147483647:
                break
            for j in range(i + 1, n - 1):
                if j - i > 1 and S[i + 1] == '0':
                    break
                b = int(S[i + 1:j + 1])
                if b > 2147483647:
                    break
                pos = j + 1
                flag = True
                res = [a, b]
                while pos < n:
                    res.append(res[-1] + res[-2])
                    if res[-1] > 2147483647:
                        flag = False
                        break
                    l = len(str(res[-1]))
                    if pos + l - 1 >= n or int(S[pos : pos + l]) != res[-1]:
                        flag = False
                        break
                    pos = pos + l
                
                if flag:
                    return res
        
        return []
```
