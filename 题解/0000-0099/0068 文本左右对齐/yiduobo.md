---
title: "68. 文本左右对齐"
aliases: ["yiduobo的每日leetcode 68.文本左右对齐"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/面试经典-150-题", "题单/滑动窗口与双指针/六-分组循环", "题单/常用数据结构/编程能力强化训练", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/130822815"
zhihu_id: "130822815"
zhihu_title: "yiduobo的每日leetcode 68.文本左右对齐"
question_id: "68"
question: "文本左右对齐"
problem_url: "https://leetcode.cn/problems/text-justification/"
difficulty: "Hard"
created: "2020-04-15T13:56:49+08:00"
updated: "2020-04-15T13:56:49+08:00"
upvotes: 0
comments: 0
---

# 68. 文本左右对齐

> **[yiduobo的每日leetcode 68.文本左右对齐](https://zhuanlan.zhihu.com/p/130822815) · 知乎 · 2020-04-15 · 赞同 0**
> 力扣：[68. 文本左右对齐](https://leetcode.cn/problems/text-justification/) · Hard · 灵茶山艾府：[分组循环，把困难题变成简单题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

68.文本左右对齐<https://leetcode-cn.com/problems/text-justification/>

考察细节的贪心题。

每一行都尽可能加入词，需要注意从当前行加入的第二个词开始就需要至少一个空格来区分。

确定好一行里面词的个数之后，可以计算出有多少空格剩余，然后讲这些空格平均分配。这里需要注意只有一个词的情况。

另外，如果当前行加入了最后一个词，那么这一行不需要分配空格，直接输出即可。

最后附上python代码，其中第二个while循环为在当前行尽量加入更多的词，之后的if则是判断是否是最后一个词，else则是分配空格的过程：

```python
class Solution(object):
    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """

        len_list = [len(word) for word in words]

        left = 0
        res = []
        while left < len(words):
            sum_len = len_list[left]
            right = left + 1
            while right < len(words) and sum_len + len_list[right] + 1 <= maxWidth:
                sum_len += len_list[right] + 1
                right += 1

            if right == len(words):
                tmp_res = ' '.join(words[left : right])
                tmp_res += ' ' * (maxWidth - len(tmp_res))
                res.append(tmp_res)
                break
            else:
                num_word = right - left
                other_space = maxWidth - sum_len
                tmp_res = words[left]

                if num_word == 1:
                    tmp_res += ' ' * other_space
                else:
                    num_space = 1 + other_space / (num_word - 1)
                    other_space %= (num_word - 1)
                    for index in range(1, num_word):
                        if index <= other_space:
                            tmp_res += ' '
                        tmp_res += ' ' * num_space + words[left + index]

                res.append(tmp_res)
                left = right
        return res
```
