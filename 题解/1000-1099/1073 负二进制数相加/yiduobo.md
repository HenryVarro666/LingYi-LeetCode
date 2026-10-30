---
title: "1073. 负二进制数相加"
aliases: ["yiduobo的每日leetcode 1073.负二进制数相加"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372593024"
zhihu_id: "372593024"
zhihu_title: "yiduobo的每日leetcode 1073.负二进制数相加"
question_id: "1073"
question: "负二进制数相加"
problem_url: "https://leetcode.cn/problems/adding-two-negabinary-numbers/"
created: "2021-05-15T19:34:50+08:00"
updated: "2021-05-15T19:34:50+08:00"
upvotes: 0
comments: 0
---

# 1073. 负二进制数相加

> **[yiduobo的每日leetcode 1073.负二进制数相加](https://zhuanlan.zhihu.com/p/372593024) · 知乎 · 2021-05-15 · 赞同 0**
> 力扣：[1073. 负二进制数相加](https://leetcode.cn/problems/adding-two-negabinary-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1073.负二进制数相加

[力扣](https://leetcode-cn.com/problems/adding-two-negabinary-numbers/)

又是负二进制进位相关的问题，可以利用之前1017题推到出来的结论，即对于某一位需要进位的p，若第p + 1位上不等于0，那么就将第p + 1位减去1，同时将第p位减去2；若第p + 1位上等于0，那么需要将第p + 1位以及第p + 2位都加上1，同时将第p位减去2。

具体推到证明可以参考之前的

[yiduobo：yiduobo的每日leetcode 1017.负二进制转换](https://zhuanlan.zhihu.com/p/368104812)

回到本题，有了上面的结论，就可以直接将arr1和arr2相加，然后从低位到高位一趟遍历完成进位，最后去除掉高位的前导0即可。

最后附上python代码：

```python
class Solution(object):
    def addNegabinary(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: List[int]
        """

        m = len(arr1)
        n = len(arr2)
        res = [0] * max(m, n)
        for index in range(m):
            res[m - index - 1] += arr1[index]
        for index in range(n):
            res[n - index - 1] += arr2[index]
        
        p = 0
        while p < len(res):
            if res[p] > 1:
                if p + 1 < len(res) and res[p + 1] > 0:
                    res[p + 1] -= 1
                else:
                    if p + 1 < len(res):
                        res[p + 1] += 1
                    else:
                        res.append(1)
                    if p + 2 < len(res):
                        res[p + 2] += 1
                    else:
                        res.append(1)

                res[p] -= 2
            
            p += 1

        
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        res.reverse()
        return res
```
