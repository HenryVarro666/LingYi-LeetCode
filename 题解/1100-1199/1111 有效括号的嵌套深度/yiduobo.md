---
title: "1111. 有效括号的嵌套深度"
aliases: ["yiduobo的每日leetcode 1111.有效括号的嵌套深度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/375236958"
zhihu_id: "375236958"
zhihu_title: "yiduobo的每日leetcode 1111.有效括号的嵌套深度"
question_id: "1111"
question: "有效括号的嵌套深度"
problem_url: "https://leetcode.cn/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/"
difficulty: "Medium"
rating: 1749
created: "2021-05-25T21:55:19+08:00"
updated: "2021-05-25T21:55:19+08:00"
upvotes: 0
comments: 0
---

# 1111. 有效括号的嵌套深度

> **[yiduobo的每日leetcode 1111.有效括号的嵌套深度](https://zhuanlan.zhihu.com/p/375236958) · 知乎 · 2021-05-25 · 赞同 0**
> 力扣：[1111. 有效括号的嵌套深度](https://leetcode.cn/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/) · Medium · 灵茶山艾府：[一图秒懂（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1111.有效括号的嵌套深度

[力扣](https://leetcode-cn.com/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/)

题目要求将括号序列分成合法的两部分，使得这两部分的最大深度最小。为了将原始括号序列中的所有深度较深的括号对分开，一个很直观的想法是按照奇偶来进行划分。不妨规定从外向内的层数从0开始计数，那么对于一个深度为k的括号序列，我们需要想办法将其第0、2、4、...这些偶数层分到A组，将1、3、5、...这些奇数层分到B组，这样一来就可以使得最终答案的最大深度最小。

仔细观察括号序列，可以发现对于左括号而言，所有偶数层的左括号的下标都是偶数，而所有奇数层的左括号下标都是奇数。仔细思考一下可以发现这是很自然的事情。设当前是第k层的左括号，那么其前方必然存在若干组匹配的括号，以及第0、1、2、...、k - 1层未匹配的左括号，一共有k个，因此当前括号前方一共就有k + 2n个括号，因此其在数组中的下标就是k+ 2n，其中n是之前匹配的括号组数。那么当k为偶数时，下标也是偶数，k为奇数时，下标也是奇数。

同样地，也可以在右括号上找规律。对于一个偶数层的右括号而言，设其是第k层的右括号，那么其前方必然存在若干组匹配的括号，以及第0、1、2、...、k - 1层未匹配的左括号，还需要加上第k层的左括号，因此下标就是k + 2n + 1，那么当k为偶数时下标为奇数，而k为奇数时下标为偶数。

有了上面的结论，我们就可以直接一趟扫描，按下标奇偶以及当前括号的左右很快判断出当前括号的层数，并进行相应的划分。

最后附上python代码：

```python
class Solution(object):
    def maxDepthAfterSplit(self, seq):
        """
        :type seq: str
        :rtype: List[int]
        """

        res = []
        for index, char in enumerate(seq):
            if char == '(':
                if index % 2 == 0:
                    res.append(0)
                else:
                    res.append(1)
            else:
                if index % 2 == 0:
                    res.append(1)
                else:
                    res.append(0)
        
        return res
```
