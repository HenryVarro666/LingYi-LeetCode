---
title: "393. UTF-8编码验证"
aliases: ["yiduobo的每日leetcode 393.UTF-8编码验证"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/176972947"
zhihu_id: "176972947"
zhihu_title: "yiduobo的每日leetcode 393.UTF-8编码验证"
question_id: "393"
question: "UTF-8编码验证"
problem_url: "https://leetcode.cn/problems/utf-8-validation/"
created: "2020-08-09T21:03:24+08:00"
updated: "2020-08-09T21:03:24+08:00"
upvotes: 0
comments: 0
---

# 393. UTF-8编码验证

> **[yiduobo的每日leetcode 393.UTF-8编码验证](https://zhuanlan.zhihu.com/p/176972947) · 知乎 · 2020-08-09 · 赞同 0**
> 力扣：[393. UTF-8编码验证](https://leetcode.cn/problems/utf-8-validation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

393.UTF-8编码验证<https://leetcode-cn.com/problems/utf-8-validation/>

按照utf8的规则从左往右逐个检测，具体为：

用data分别与128、64、32、16、8做与运算，判断当前utf8字符属于下列哪一种

1、data & 128 \= 0，即0XXXXXXX

表示当前utf8字符仅包含当前字节

2、不满足情况1，且data & 64 \= 0，即10XXXXXX

非法情况

3、不满足情况1和2，且data & 32 \= 0，即110XXXXX

表示当前utf8字符包含两个字节，除当前字节外后续还需要检测一个字节

4、不满足情况1到3，且data & 16 \= 0，即1110XXXX

表示当前utf8字符包含三个字节，除当前字节外后续还需要检测两个字节

5、不满足情况1到4，且data & 8 \= 0，即11110XXX

表示当前utf8字符包含四个字节，除当前字节外后续还需要检测三个字节

6、不满足情况1到5，且data & 8 !\= 0，即11111XXX

非法情况

当出现非法情况时，直接返回false，否则还需要根据上述操作得到的后续需要检测的字节长度继续进行检测。具体做法为对后续检测长度内的data分别与128、64做与运算，判断是否满足10XXXXXX这种形式。

当处理完一个utf8字符之后，重复上述过程直到处理到data末尾或者出现非法情况为止。

最后附上python代码：

```python
class Solution(object):
    def validUtf8(self, data):
        """
        :type data: List[int]
        :rtype: bool
        """

        now = 0
        while now < len(data):
            if data[now] & 128 == 0:
                now += 1
            else:
                if data[now] & 64 == 0:
                    return False
                if data[now] & 32 == 0:
                    check_len = 1
                elif data[now] & 16 == 0:
                    check_len = 2
                elif data[now] & 8 == 0:
                    check_len = 3
                else:
                    return False
                
                now += 1
                while now < len(data) and check_len > 0:
                    if data[now] & 128 != 0 and data[now] & 64 == 0:
                        now += 1
                        check_len -= 1
                    else:
                        return False

                if check_len > 0:
                    return False

        return True
```
