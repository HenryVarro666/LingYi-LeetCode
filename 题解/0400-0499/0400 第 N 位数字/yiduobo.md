---
title: "400. 第N个数字"
aliases: ["yiduobo的每日leetcode 400.第N个数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/181717447"
zhihu_id: "181717447"
zhihu_title: "yiduobo的每日leetcode 400.第N个数字"
question_id: "400"
question: "第 N 位数字"
problem_url: "https://leetcode.cn/problems/nth-digit/"
difficulty: "Medium"
created: "2020-08-12T22:50:32+08:00"
updated: "2020-08-12T22:50:32+08:00"
upvotes: 1
comments: 0
---

# 400. 第N个数字

> **[yiduobo的每日leetcode 400.第N个数字](https://zhuanlan.zhihu.com/p/181717447) · 知乎 · 2020-08-12 · 赞同 1**
> 力扣：[400. 第 N 位数字](https://leetcode.cn/problems/nth-digit/) · Medium · 灵茶山艾府：[数学做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

400.第N个数字<https://leetcode-cn.com/problems/nth-digit/>

找规律的题目。

对于一位数，只有1-9共9个数字。

对于两位数，一共有10-99共90个数，因此一共有2\*90\=180个数字。

对于三位数，一共有100-999共900个数，因此一共有3\*900\=2700个数字。

那么对于k位数，一共用9\*10^(k-1)个数，因此一共有k \* 9 \* 10^(k-1)个数字。

设1位数到k位数的数字总和为f[k]，那么通过f[k]就能知道第N个数字的位数，通过N-f[k] - 1则可以知道N在所有k位数中的排位p，即从10^(k-1)开始数的第p个数字。

接下来，已知每个数的位数为k位，那么通过p/k和p%k就能找到具体的数字了。

需要注意的，这里的p是从高位往低位开始数的，因此最后如果要通过不断除10模10来获取从高到低的第n个数字的话，那么这里需要优先使用k - n + 1来计算该数字是从低到高的位数。

最后附上python代码：

```python
class Solution(object):
    def findNthDigit(self, n):
        """
        :type n: int
        :rtype: int
        """

        prev_cnt = 0
        cnt = 9
        res_len = 1
        while cnt < n:
            res_len += 1
            prev_cnt = cnt
            cnt += 9 * (10 ** (res_len - 1)) * res_len
        
        n -= prev_cnt + 1
        res = 10 ** (res_len - 1)
        offset = n / res_len
        n %= res_len
        res += offset
        n = res_len - n - 1

        while n:
            n -= 1
            res /= 10
    
        return res % 10
```
