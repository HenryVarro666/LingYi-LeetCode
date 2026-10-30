---
title: "2047. 句子中的有效单词数"
aliases: ["yiduobo的每日leetcode 2047.句子中的有效单词数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/simulation", "leetcode/zheng-ze-biao-da-shi"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/511238020"
zhihu_id: "511238020"
zhihu_title: "yiduobo的每日leetcode 2047.句子中的有效单词数"
question_id: "2047"
question: "句子中的有效单词数"
problem_url: "https://leetcode.cn/problems/number-of-valid-words-in-a-sentence/"
difficulty: "Easy"
created: "2022-05-08T22:00:30+08:00"
updated: "2022-05-08T22:00:30+08:00"
upvotes: 0
comments: 0
---

# 2047. 句子中的有效单词数

> **[yiduobo的每日leetcode 2047.句子中的有效单词数](https://zhuanlan.zhihu.com/p/511238020) · 知乎 · 2022-05-08 · 赞同 0**
> 力扣：[2047. 句子中的有效单词数](https://leetcode.cn/problems/number-of-valid-words-in-a-sentence/) · Easy · 灵茶山艾府：[Go 简洁写法，附详细注释](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2047.句子中的有效单词数

[力扣](https://leetcode-cn.com/problems/number-of-valid-words-in-a-sentence/)

题目要求按空格分隔出各个token，但空格的数量不定，因此如果想用split就必须靠正则来匹配，否则就需要一趟遍历来做。我在这里采取的遍历的做法。

首先，从当前位置开始找到第一个不是空格的字符，这就是一个token的开头。接下来需要遍历这个token中的字符，同时在这个过程中对各种情况进行判断。方便起见需要两个标记flag和hyphen_flag，其中flag表示当前这个token是否可能是一个有效单词，hyphen_flag表示当前token中是否出现过一个有效的连字符。

对于当前字符：

1、若flag为false，说明token已经无效，那么直接跳过该字符不进行处理

2、若当前字符为数字，那么将flag置为false

3、若当前字符为连字符：

3-1）若hyphen_flag为true，说明当前token中已经有一个合法连字符了，那么当前出现了第二个连字符，说明token必然无效，此时置flag为false

3-2）若hyphen_flag为false，且当前字符不是字符串的首字符或末尾字符，同时当前字符两边的字符都是小写字母，那么就说明当前的连字符是token中第一个有效的连字符，此时应该将hyphen_flag置为true

4、若当前字符为标点符号，且当前字符不是字符串的末尾字符，同时当前字符的下一个字符不是空格，那么当前字符就不是一个合法的标点，此时应该将flag置为false

无论是上面哪种情况，处理完当前字符后都应该向后继续遍历，直到来到字符的末尾或者遇到空格。遍历停止时，说明当前的token已经完结，此时可以通过flag来确定当前的token是否是有效的单词，并更新答案。接下来从当前位置开始继续向后，找到第一个不是空格的字符，然后重复上面过程直到处理完全部的token。

最后附上python代码：

```python
class Solution(object):
    def countValidWords(self, sentence):
        """
        :type sentence: str
        :rtype: int
        """

        res = 0
        p = 0
        n = len(sentence)
        while p < n:
            while p < n and sentence[p] == ' ':
                p += 1
            
            if p == n:
                break

            flag = True
            hyphen_flag = False

            while p < n and sentence[p] != ' ':
                if not flag:
                    pass
                elif sentence[p] >= '0' and sentence[p] <= '9':
                    flag = False

                elif sentence[p] == '-':
                    if hyphen_flag:
                        flag = False
                    elif p > 0 and sentence[p - 1] >= 'a' and sentence[p - 1] <= 'z' and p + 1 < n and sentence[p + 1] >= 'a' and sentence[p + 1] <= 'z':
                        hyphen_flag = True
                    else:
                        flag = False

                elif sentence[p] == '!' or sentence[p] == '.' or sentence[p] == ',':
                    if p + 1 < n and sentence[p + 1] != ' ':
                        flag = False
                
                p += 1

            if flag:
                res += 1
        
        return res
```
