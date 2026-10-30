---
title: "899. 有序队列"
aliases: ["yiduobo的每日leetcode 899.有序队列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353236423"
zhihu_id: "353236423"
zhihu_title: "yiduobo的每日leetcode 899.有序队列"
question_id: "899"
question: "有序队列"
problem_url: "https://leetcode.cn/problems/orderly-queue/"
created: "2021-02-26T22:48:29+08:00"
updated: "2021-02-26T22:48:29+08:00"
upvotes: 1
comments: 0
---

# 899. 有序队列

> **[yiduobo的每日leetcode 899.有序队列](https://zhuanlan.zhihu.com/p/353236423) · 知乎 · 2021-02-26 · 赞同 1**
> 力扣：[899. 有序队列](https://leetcode.cn/problems/orderly-queue/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

899.有序队列

[力扣](https://leetcode-cn.com/problems/orderly-queue/)

当k \= 1时，只能一位位地移动然后进行对比，选出其中字典序最小的。

当k >\= 2时，情况就不一样了。任意取S中的两个位置p和q，不妨设满足p \< q，那么当前的S可以表示为：

S[0] \~ S[p - 1]—>S[p]—>S[p + 1] \~ S[q - 1]—>S[q]—>S[q + 1] \~ S[-1]

接下来我们可以进行下列操作：

1、将S[0] \~ S[p - 1]，S[p]以及S[p + 1] \~ S[q - 1]都移动到末尾，可以得到

S[q]—>S[q + 1] \~ S[-1]—>S[0] \~ S[p - 1]—>S[p]—>S[p + 1] \~ S[q - 1]

2、将S[q]固定在第1个字符上，然后通过第2个字符将S[q + 1] \~ S[-1]以及S[0] \~ S[p - 1]移动到末尾，可以得到

S[q]—>S[p]—>S[p + 1] \~ S[q - 1]—>S[q + 1] \~ S[-1]—>S[0] \~ S[p - 1]

3、再将S[p]固定在第2个字符时，然后通过第1个字符将S[q]以及S[p + 1] \~ S[q - 1]移动到末尾，可以得到

S[q + 1]—>S[p]—>S[q + 2] \~ S[-1]—>S[0] \~ S[p - 1]—>S[q]—>S[p + 1] \~ S[q - 1]

4、最后，按照S[p]，S[q + 1]，S[q + 2] \~ S[-1]的顺序将这些字符移动到末尾，可以得到

S[0] \~ S[p - 1]—>S[q]—>S[p + 1] \~ S[q - 1]—>S[p]—>S[q + 1] \~ S[-1]

可以发现，经过上面的一系列操作，我们将S中p和q位置上的字符进行了交换。换言之，当k>\=2时，我们就有了交换S中任意两个字符的能力，因此当k>\=2时，答案就是将S中的字符按字典序排序后输出。

最后附上python代码：

```python
class Solution(object):
    def orderlyQueue(self, S, K):
        """
        :type S: str
        :type K: int
        :rtype: str
        """

        if K >= 2:
            return ''.join(sorted(list(S)))
        
        n = len(S)
        S += S
        res_pos = 0
        for index in range(1, n):
            if S[res_pos:res_pos + n] > S[index:index + n]:
                res_pos = index
        
        return S[res_pos:res_pos + n]
```
