---
title: "722. 删除注释"
aliases: ["yiduobo的每日leetcode 722.删除注释"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/333970198"
zhihu_id: "333970198"
zhihu_title: "yiduobo的每日leetcode 722.删除注释"
question_id: "722"
question: "删除注释"
problem_url: "https://leetcode.cn/problems/remove-comments/"
created: "2020-12-07T23:00:58+08:00"
updated: "2020-12-07T23:00:58+08:00"
upvotes: 1
comments: 0
---

# 722. 删除注释

> **[yiduobo的每日leetcode 722.删除注释](https://zhuanlan.zhihu.com/p/333970198) · 知乎 · 2020-12-07 · 赞同 1**
> 力扣：[722. 删除注释](https://leetcode.cn/problems/remove-comments/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

722.删除注释

[力扣](https://leetcode-cn.com/problems/remove-comments/)

题目给出的数据是按行分好的数组，若在处理某行的过程中发现了行注释，那么可以直接跳过这一行；如果发现了块注释，则需要维护一个变量表示当前是否处于块注释当中。因此我们需要一个变量flag表示当前是否处于块注释中，然后遍历数组中的每一行的每个字符，对于当前字符：

1、若是这是新的一行，且当前未处于块注释当中，而且上一行非空：

此时需要另起一行，在这里的表现就是在答案数组的末尾添加一个空字符串。

2、若当前flag为true，表示处于块注释中：

2-1、当前字符为星号：

此时需要判断下一个字符是否为斜杠，若是斜杠，说明块注释结束了，设置flag为false，然后从斜杠之后的下一个字符开始继续往后遍历。若不是斜杠，那么该字符应该被注释掉，直接从下一个字符开始往后继续遍历。

2-2、当前字符不为星号：

该字符将被注释掉，从下一个字符开始往后继续遍历。

3、若当前flag为false，表示为处于块注释中：

3-1、当前字符为斜杠，且下一个字符为斜杠：

此时出现了行注释，那么跳过改行从下一行开始往后遍历。

3-2、当前字符为斜杠，且下一个字符为星号：

此时出现了块注释，那么设置flag为true，然后从星号的下一个字符开始往后继续遍历。

3-3、其他情况：

此时为正常文本，将其加入到最后一行，也就是答案数组的末尾字符串中即可。

最后附上python代码：

```python
class Solution(object):
    def removeComments(self, source):
        """
        :type source: List[str]
        :rtype: List[str]
        """

        part_flag = False
        res = []
        for line in source:
            p = 0
            if res == [] or (res[-1] != '' and not part_flag):
                res.append('')
            while p < len(line):
                if part_flag:
                    if line[p] == '*' and p + 1 < len(line) and line[p + 1] == '/':
                        p += 1
                        part_flag = False
                    p += 1

                elif line[p] == '/' and p + 1 < len(line):
                    if line[p + 1] == '/':
                        break
                    elif line[p + 1] == '*':
                        part_flag = True
                        p += 1
                    else:
                        res[-1] += line[p]
                    p += 1

                else:
                    res[-1] += line[p]
                    p += 1
        
        return res
```
