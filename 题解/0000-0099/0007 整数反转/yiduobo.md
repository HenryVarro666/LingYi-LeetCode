---
title: "7. 整数反转"
aliases: ["yiduobo的每日leetcode 7.整数反转"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/113385545"
zhihu_id: "113385545"
zhihu_title: "yiduobo的每日leetcode 7.整数反转"
question_id: "7"
question: "整数反转"
problem_url: "https://leetcode.cn/problems/reverse-integer/"
created: "2020-03-15T19:35:17+08:00"
updated: "2020-03-15T19:35:17+08:00"
upvotes: 0
comments: 0
---

# 7. 整数反转

> **[yiduobo的每日leetcode 7.整数反转](https://zhuanlan.zhihu.com/p/113385545) · 知乎 · 2020-03-15 · 赞同 0**
> 力扣：[7. 整数反转](https://leetcode.cn/problems/reverse-integer/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

7.整数反转<https://leetcode-cn.com/problems/reverse-integer/>

比较基础的题目，每次mod 10取最后一位k，然后反转的结果y \= y \* 10 + k就行了。主要是要注意最大和最小的边界判断，即每次取模之后都考虑此时y是否大于边界除以10，或者y等于边界除以10且k在边界个位数的范围之外。不选择直接计算y然后判断是否越界的原因是计算y可能已经导致了越界，而使用上面的判断则保证y不会越界。

另外使用python时需要特别注意的是，当负数整除10的时候，若无法整除则会向下减一；当负数mod 10的时候，若模不等于0则会加上10补成正数。例如样例中的-123，就有

-123/10 \= -13，就是-12 - 1 \= -13

-123 % 10 \= 7，就是-3 + 10 \= 7

所以在处理负数的时候，需要判断每次取模的结果是否为0，然后进行相应的操作。

最后附上python代码：

```python
class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        max_bound = 214748364
        min_bound = -214748364

        negative_flag = x < 0
        y = 0
        while x != 0:
            k = x % 10
            x /= 10
            if negative_flag:
                if k != 0:
                    k -= 10
                    x += 1
                if y < min_bound or (y == min_bound and k < -8):
                    return 0
            else:
                if y > max_bound or (y == max_bound and k > 7):
                    return 0
            
            y = y * 10 + k
        return y
```
