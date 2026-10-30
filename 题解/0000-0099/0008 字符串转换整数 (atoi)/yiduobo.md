---
title: "8. 字符串转换整数(atoi)"
aliases: ["yiduobo的每日leetcode 8.字符串转换整数(atoi)"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/常用数据结构", "题单/常用数据结构/三-栈", "题单/常用数据结构/编程能力强化训练"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/113690139"
zhihu_id: "113690139"
zhihu_title: "yiduobo的每日leetcode 8.字符串转换整数(atoi)"
question_id: "8"
question: "字符串转换整数 (atoi)"
problem_url: "https://leetcode.cn/problems/string-to-integer-atoi/"
difficulty: "Medium"
created: "2020-03-16T21:56:09+08:00"
updated: "2020-03-16T21:56:09+08:00"
upvotes: 0
comments: 0
---

# 8. 字符串转换整数(atoi)

> **[yiduobo的每日leetcode 8.字符串转换整数(atoi)](https://zhuanlan.zhihu.com/p/113690139) · 知乎 · 2020-03-16 · 赞同 0**
> 力扣：[8. 字符串转换整数 (atoi)](https://leetcode.cn/problems/string-to-integer-atoi/) · Medium · 灵茶山艾府：[只使用 32 位整数的写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

8.字符串转换整数(atoi)<https://leetcode-cn.com/problems/string-to-integer-atoi/>

比较基础的题目。扫描str找到非空字符如果不符合要求，就返回0，否则往后按位累加，直到非数字字符出现，同时在累加的过程中需要注意判断是否越界，这里可以直接运用上一题判断是否越界的逻辑。

最后附上python代码：

```python
class Solution(object):
    def myAtoi(self, str):
        """
        :type str: str
        :rtype: int
        """
        int_max = 2147483647
        int_min = -2147483648

        x = None
        negative_flag = 1
        for index in range(len(str)):
            if x is None:
                if str[index] == ' ':
                    continue
                elif str[index] == '-':
                    negative_flag = -1
                    x = 0
                elif str[index] == '+':
                    negative_flag = 1
                    x = 0
                elif str[index] >= '0' and str[index] <= '9':
                    x = negative_flag * int(str[index])
                else:
                    return 0
            else:
                if str[index] >= '0' and str[index] <= '9':
                    if x > 214748364 or (x == 214748364 and int(str[index]) > 7):
                        return int_max
                    elif x < -214748364 or (x == -214748364 and int(str[index]) > 8):
                        return int_min
                    else:
                        x = x * 10 + negative_flag * int(str[index])
                else:
                    break
        if x is None:
            x = 0
        return x
```
