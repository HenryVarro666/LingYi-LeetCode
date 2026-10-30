---
title: "1588. 所有奇数长度子数组的和"
aliases: ["yiduobo的每日leetcode 1588.所有奇数长度子数组的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430998264"
zhihu_id: "430998264"
zhihu_title: "yiduobo的每日leetcode 1588.所有奇数长度子数组的和"
question_id: "1588"
question: "所有奇数长度子数组的和"
problem_url: "https://leetcode.cn/problems/sum-of-all-odd-length-subarrays/"
created: "2021-11-09T00:04:33+08:00"
updated: "2021-11-09T00:04:33+08:00"
upvotes: 0
comments: 0
---

# 1588. 所有奇数长度子数组的和

> **[yiduobo的每日leetcode 1588.所有奇数长度子数组的和](https://zhuanlan.zhihu.com/p/430998264) · 知乎 · 2021-11-09 · 赞同 0**
> 力扣：[1588. 所有奇数长度子数组的和](https://leetcode.cn/problems/sum-of-all-odd-length-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1588.所有奇数长度子数组的和

[力扣](https://leetcode-cn.com/problems/sum-of-all-odd-length-subarrays/)

由于题目的规模很小，因此直接使用暴力法也是可以的，不过这里子数组形成的和的形状是比较有意思的，可以使用一些算法来高效求解。

首先不妨撇开奇数长度子数组和，来观察各种长度子数组的和是怎么排布的。

不妨设长度为k的子数组和为s[k]，先考察arr足够长的情况：

1、当k等于1时：

s[k]显然就等于arr[0] + arr[1] + ... + arr[n - 1]

2、当k等于2时：

s[k] \= (arr[0] + arr[1]) + (arr[1] + arr[2]) + ... + (arr[n - 3] + arr[n - 2]) + (arr[n - 2] + arr[n - 1])

可以发现，此时除arr[0]以及arr[n - 1]之外，其他位置上的数都出现了两次，那么重新整理之后就有

s[k] \= (arr[0] + arr[1] + ... + arr[n - 1]) + (arr[1] + arr[2] + ... + arr[n - 2])

3、当k等于3时：

s[k] \= (arr[0] + arr[1] + arr[2]) + (arr[1] + arr[2] + arr[3]) + (arr[2] + arr[3] + arr[4]) + ...

\+ (arr[n - 4] + arr[n - 3] + arr[n - 2]) + (arr[n - 3] + arr[n - 2] + arr[n - 1])

类似的，arr[0]以及arr[n - 1]仅出现一次，arr[1]以及arr[n - 2]则只出现两次，而其他位置上的数都出现了三次，因此整理后就有

s[k] \= (arr[0] + arr[1] + ... + arr[n - 1]) + (arr[1] + arr[2] + ... + arr[n - 2]) + (arr[2] + arr[3] + ... + arr[n - 3])

此时对于s[0]、s[1]、s[2]，可以发现满足

s[k] \= s[k - 1] + (arr[k - 1] + arr[k] + ... + arr[n - k])

而对于后面这里的子段和，则可以利用前缀和来进行优化，于是最终就有

s[k] \= s[k - 1] + prefix[n - k] - prefix[k - 2]

当然，上面考虑的是充分展开的情况，更准确的说，是k满足k \* 2 - 1 \<\= n的情况。因为只有满足了这个条件，才能容纳下至少k个长度为k的子数组，从而使得上面的计算式子成立。而相对应的，在未能充分展开的情况下，长度为k的子数组就最多只有n - k + 1个，也就是重叠部分出现次数最多只有n - k + 1次，不过好在这恰好是s[n - k + 1]代表的含义。

到了这里，就得到了一种O(n)的做法。

首先计算数组的前缀和prefix，并利用前缀和计算出所有的s[0]到s[n - 1]。

接下来枚举1到n之间的所有奇数index。若index \* 2 - 1 \<\= n，那么将答案加上s[index]，否则将答案加上s[n - index + 1]。

我在实现的时候s数组的下标是从0开始的，因此最终累加时需要注意减1的偏移。最后附上python代码：

```python
class Solution(object):
    def sumOddLengthSubarrays(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        prefix = [arr[0]]
        for num in arr[1:]:
            prefix.append(prefix[-1] + num)
        
        s = [prefix[-1]]
        n = len(arr)
        l = 0
        r = n - 1
        while l < r:
            s.append(s[-1] + prefix[r - 1] - prefix[l])
            l += 1
            r -= 1
        
        res = 0
        for index in range(1, n + 1, 2):
            if index + index - 1 <= n:
                res += s[index - 1]
            else:
                res += s[n - index]
        
        return res
```
