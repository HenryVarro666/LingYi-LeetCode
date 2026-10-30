---
title: "1410. HTML实体解析器"
aliases: ["yiduobo的每日leetcode 1410.HTML实体解析器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/406291059"
zhihu_id: "406291059"
zhihu_title: "yiduobo的每日leetcode 1410.HTML实体解析器"
question_id: "1410"
question: "HTML实体解析器"
problem_url: "https://leetcode.cn/problems/html-entity-parser/"
created: "2021-09-02T23:23:19+08:00"
updated: "2021-09-02T23:23:19+08:00"
upvotes: 0
comments: 0
---

# 1410. HTML实体解析器

> **[yiduobo的每日leetcode 1410.HTML实体解析器](https://zhuanlan.zhihu.com/p/406291059) · 知乎 · 2021-09-02 · 赞同 0**
> 力扣：[1410. HTML实体解析器](https://leetcode.cn/problems/html-entity-parser/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1410.HTML实体解析器

[力扣](https://leetcode-cn.com/problems/html-entity-parser/)

没有什么复杂算法，但是实现起来比较麻烦的题目。直接逐个字符扫描，判断各种转义的情况即可。当然，也可以直接使用语言中的replace操作，只需一行代码就能解决问题。

最后附上python代码：

```python
class Solution(object):
    def entityParser(self, text):
        """
        :type text: str
        :rtype: str
        """

        res = ''
        n = len(text)
        pos = 0
        while pos < n:
            if text[pos] == '&' and pos + 3 < n:
                if text[pos + 1] == 'q' and pos + 5 < n and text[pos + 5] == ';':
                    if text[pos + 2] == 'u' and text[pos + 3] == 'o' and text[pos + 4] == 't':
                        res += '"'
                        pos += 6
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2
                elif text[pos + 1] == 'a':
                    if pos + 4 < n and text[pos + 4] == ';' and text[pos + 2] == 'm' and text[pos + 3] == 'p':
                        res += '&'
                        pos += 5
                    elif pos + 5 < n and text[pos + 5] == ';' and text[pos + 2] == 'p' and text[pos + 3] == 'o' and text[pos + 4] == 's':
                        res += "'"
                        pos += 6
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2

                elif (text[pos + 1] == 'g' or text[pos + 1] == 'l') and pos + 3 < n and text[pos + 3] == ';':
                    if text[pos + 2] == 't':
                        if text[pos + 1] == 'g':
                            res += '>'
                        else:
                            res += '<'
                        pos = pos + 4
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2

                elif text[pos + 1] == 'f' and pos + 6 < n and text[pos + 6] == ';':
                    if text[pos + 2] == 'r' and text[pos + 3] == 'a' and text[pos + 4] == 's' and text[pos + 5] == 'l':
                        res += '/'
                        pos += 7
                    else:
                        res += text[pos]
                        res += text[pos + 1]
                        pos += 2

                else:
                    res += text[pos]
                    pos += 1

            else:
                res += text[pos]
                pos += 1
        
        return res
```
