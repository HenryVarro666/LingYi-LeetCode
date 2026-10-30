---
title: "1432. 改变一个整数能得到的最大差值"
aliases: ["yiduobo的每日leetcode 1432.改变一个整数能得到的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/409164648"
zhihu_id: "409164648"
zhihu_title: "yiduobo的每日leetcode 1432.改变一个整数能得到的最大差值"
question_id: "1432"
question: "改变一个整数能得到的最大差值"
problem_url: "https://leetcode.cn/problems/max-difference-you-can-get-from-changing-an-integer/"
difficulty: "Medium"
rating: 1427
created: "2021-09-10T22:49:11+08:00"
updated: "2021-09-10T22:49:11+08:00"
upvotes: 1
comments: 0
---

# 1432. 改变一个整数能得到的最大差值

> **[yiduobo的每日leetcode 1432.改变一个整数能得到的最大差值](https://zhuanlan.zhihu.com/p/409164648) · 知乎 · 2021-09-10 · 赞同 1**
> 力扣：[1432. 改变一个整数能得到的最大差值](https://leetcode.cn/problems/max-difference-you-can-get-from-changing-an-integer/) · Medium · 灵茶山艾府：[贪心 O(log num) 做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1432.改变一个整数能得到的最大差值

[力扣](https://leetcode-cn.com/problems/max-difference-you-can-get-from-changing-an-integer/)

为了使得a和b的差值最大，那么我们可以让a尽可能大，让b尽可能小。

为了让a尽可能大，我们应当将位数最高，且不是9的数作为x，将9作为y来进行替换。

为了让b尽可能小，我们应当将位数最高，且不是0的数替换成0。但是还有一个条件是替换后的数字不能有前导0，因此在这里需要做一些调整。首先还是考察最高位，若最高位不是1，那么我们就将其作为x，将1作为y来进行替换，否则我们一次考察后续位上的数字：

1、若当前处理的数字与最高位不同，且不为0，那么此时将其替换为0之后不会出现前导0的情况，因此我们可以将当前位上的数字作为x，将0作为y来进行替换

2、若当前位上的数字大于1，那么我们可以将其作为x，将1作为y来进行替换

得到替换后的结果后，计算二者的差值输出即可。

最后附上python代码：

```python
class Solution(object):
    def maxDiff(self, num):
        """
        :type num: int
        :rtype: int
        """
        
        num_list = []
        tmp = num
        while tmp:
            num_list.append(tmp % 10)
            tmp /= 10
        
        num_list.reverse()
        
        xa = ya = None
        xb = yb = None
        for index, now_num in enumerate(num_list):
            if now_num != 9 and xb is None:
                xb = now_num
                yb = 9
            
            if xa is None:
                if index == 0 and now_num != 1:
                    xa = now_num
                    ya = 1
                elif index > 0:
                    if  now_num != num_list[0] and now_num != 0:
                        xa = now_num
                        ya = 0
                    elif now_num > 1:
                        xa = now_num
                        ya = 1
        
        a = b = 0
        for now_num in num_list:
            a *= 10
            if xa == now_num:
                a += ya
            else:
                a += now_num
            
            b *= 10
            if xb == now_num:
                b += yb
            else:
                b += now_num
            
        return b - a
```
