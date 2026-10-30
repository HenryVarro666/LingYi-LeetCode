---
title: "3582. 为视频标题生成标签"
aliases: ["yiduobo的每日leetcode 3582.为视频标题生成标签"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1938363693839672309"
zhihu_id: "1938363693839672309"
zhihu_title: "yiduobo的每日leetcode 3582.为视频标题生成标签"
question_id: "3582"
question: "为视频标题生成标签"
problem_url: "https://leetcode.cn/problems/generate-tag-for-video-caption/"
difficulty: "Easy"
created: "2025-08-11T22:28:51+08:00"
updated: "2025-08-11T22:28:51+08:00"
upvotes: 0
comments: 0
---

# 3582. 为视频标题生成标签

> **[yiduobo的每日leetcode 3582.为视频标题生成标签](https://zhuanlan.zhihu.com/p/1938363693839672309) · 知乎 · 2025-08-11 · 赞同 0**
> 力扣：[3582. 为视频标题生成标签](https://leetcode.cn/problems/generate-tag-for-video-caption/) · Easy · 灵茶山艾府：[库函数模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3582.为视频标题生成标签

[3582. 为视频标题生成标签 - 力扣（LeetCode）](https://leetcode.cn/problems/generate-tag-for-video-caption/description/)

题目给出一个字符串caption，表示视频的标题，caption仅由小写字符和空格组成。现在要求按以下步骤按顺序生成视频的有效标签：

1、将所有单词组合为单个驼峰命名字符串，并在前面加上'\#'

2、移除所有不是英文字母的字符，但保留第一个字符'\#'

3、将结果截断为最多100个字符

要求返回生成后的标签。

题目保证caption中没有空格以外的其他非英文字母的字符，因此可以直接通过split分离其中的单词，接下来初始化答案字符串为'\#'，然后遍历这些单词，将其中的字符逐个添加到答案字符串中，直到遍历完所有的单词或者答案字符串的长度到达100。需要注意在这里除第一个单词外，其他单词的首字符大写，其他字符都需要小写。

最后附上python代码：

```python
class Solution(object):
    def generateTag(self, caption):
        """
        :type caption: str
        :rtype: str
        """
        
        res = ['#']
        for word in caption.split():
            for index, char in enumerate(word):
                if index == 0:
                    if len(res) == 1:
                        res.append(lower(char))
                    else:
                        res.append(upper(char))
                else:
                    res.append(lower(char))

                if len(res) == 100:
                    break
            
            if len(res) == 100:
                break
        
        return ''.join(res)
```
