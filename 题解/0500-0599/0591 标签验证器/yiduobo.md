---
title: "591. 标签验证器"
aliases: ["yiduobo的每日leetcode 591.标签验证器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/267932156"
zhihu_id: "267932156"
zhihu_title: "yiduobo的每日leetcode 591.标签验证器"
question_id: "591"
question: "标签验证器"
problem_url: "https://leetcode.cn/problems/tag-validator/"
created: "2020-10-22T23:37:18+08:00"
updated: "2020-10-22T23:37:18+08:00"
upvotes: 0
comments: 0
---

# 591. 标签验证器

> **[yiduobo的每日leetcode 591.标签验证器](https://zhuanlan.zhihu.com/p/267932156) · 知乎 · 2020-10-22 · 赞同 0**
> 力扣：[591. 标签验证器](https://leetcode.cn/problems/tag-validator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

591.标签验证器<https://leetcode-cn.com/problems/tag-validator/>

看着题目描述一大堆，实际上还没有带括号的四则运算难做。

对于这类线性的可能出现套娃的字符串处理问题，一般就是一趟扫描判断各种情况，遇到套娃时则交个栈来处理。

具体对于这一题，有下面几种情况：

1、当前字符为'\<'，且下一个字符为'!'：

此时为cdata的起始字符，因此可以寻找cdata的结束字符'\]\]>'。

若找不到，说明是非法情况，返回false。

若能找到，那么就判断中间这一段是否包含字符串'\[CDATA\['，若不包含，说明是非法情况，返回false。若包含，那么说明这里出现了一串cdata，我们可以直接跳过这一段，接下来从'\]\]>'的下一个字符继续往后扫描即可。

2、当前字符为'\<'，且下一个字符不是'!'：

此时可能是起始标签\<tag_name>，也可能是结束标签\</tag_name>，或者是非法情况。那么我们首先判断下一个字符是否为'/'，来确定当前标签是起始标签还是结束标签。

接下来，寻找第一个'>'，若找不到，那么就是非法情况，返回false。找到第一个'>'之后，就可以确定tag_name是什么。判断其长度是否合法，同时扫描tag_name判断其中每个字符是否都是大写字符。若tag_name不合法，那么返回false。

检验完tag_name之后，若当前标签为起始标签，那么说明后续将出现一段tag_content，而这里是可能出现标签套娃的，因此需要将当前的tag_name压入栈中，然后继续往后处理。若当前标签为结束标签，那么就检测栈顶元素是否和当前的tag_name一致。如果不一致，说明tag匹配失败，返回false，否则将栈顶元素弹出，说明当前的标签是合法的闭合标签。

3、其他字符：

此时若栈为空，且之前出现过tag，说明当前字符出现在闭合标签之外，为非法情况，返回false。否则当前字符必然是tag_content中的一个字符，直接略过往后继续扫描即可。

为了处理这种情况，需要额外维护一个变量tag_flag，用来标记当前是否一个存在闭合标签。这个标签初始值为false，只有在情况2中，结束标签成功进行匹配时才能置为true。

扫描完成后，若栈非空，说明没有结束标签，返回false。若tag_flag为假，说明不存在闭合标签，返回false。若栈为空且tag_flag为真，才能返回true。

最后附上python代码：

```python
class Solution(object):
    def isValid(self, code):
        """
        :type code: str
        :rtype: bool
        """

        l = len(code)
        pos = 0
        stack = []
        tag_flag = False
        if code[0] != '<':
            return False
        while pos < l:
            if not stack and tag_flag:
                return False
            if code[pos] == '<':
                if stack and pos + 1 < l and code[pos + 1] == '!':
                    cdata_right = code.find(']]>', pos + 2)
                    if cdata_right < 0:
                        return False
                    if code[pos + 2: cdata_right].find("[CDATA[") != 0:
                        return False
                    pos = cdata_right + 1
                else:
                    if pos + 1 < l and code[pos + 1] == '/':
                        tag_end = True
                        tag_name_left = pos + 2
                    else:
                        tag_end = False
                        tag_name_left = pos + 1
                    
                    tag_name_right = code.find('>', tag_name_left)
                    if tag_name_right < 0:
                        return False
                    tag_len = tag_name_right - tag_name_left 
                    if tag_len < 1 or tag_len > 9:
                        return False
                    for index in range(tag_name_left, tag_name_right):
                        if code[index] < 'A' or code[index] > 'Z':
                            return False
                    
                    if tag_end:
                        if not stack or stack[-1] != code[tag_name_left:tag_name_right]:
                            return False
                        stack.pop()
                    else:
                        tag_flag = True
                        stack.append(code[tag_name_left:tag_name_right])
                
                    pos = tag_name_right + 1
            else:
                pos += 1

        if stack:
            return False
        return tag_flag
```
