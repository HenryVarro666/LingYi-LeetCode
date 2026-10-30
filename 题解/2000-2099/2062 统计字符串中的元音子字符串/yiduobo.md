---
title: "2062. 统计字符串中的元音子字符串"
aliases: ["yiduobo的每日leetcode 2062.统计字符串中的元音子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/514539382"
zhihu_id: "514539382"
zhihu_title: "yiduobo的每日leetcode 2062.统计字符串中的元音子字符串"
question_id: "2062"
question: "统计字符串中的元音子字符串"
problem_url: "https://leetcode.cn/problems/count-vowel-substrings-of-a-string/"
difficulty: "Easy"
created: "2022-05-14T23:48:29+08:00"
updated: "2022-05-14T23:48:29+08:00"
upvotes: 0
comments: 0
---

# 2062. 统计字符串中的元音子字符串

> **[yiduobo的每日leetcode 2062.统计字符串中的元音子字符串](https://zhuanlan.zhihu.com/p/514539382) · 知乎 · 2022-05-14 · 赞同 0**
> 力扣：[2062. 统计字符串中的元音子字符串](https://leetcode.cn/problems/count-vowel-substrings-of-a-string/) · Easy · 灵茶山艾府：[O(n) 滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2062.统计字符串中的元音子字符串

[力扣](https://leetcode.cn/problems/count-vowel-substrings-of-a-string/)

由于题目的数据规模比较小，直接枚举每个子字符串然后统计是可行的做法，不过更好的做法则是利用滑动窗口。

使用变量l表示当前窗口的左边界，min_r和max_r分别表示窗口的最小右边界和最大右边界。随着l的向后移动，要么找不出合法的min_r和max_r，要么min_r和max_r会在上一轮的基础上也跟着向后移动。这样一来，就可以在均摊O(1)的时间复杂度内找出每个l对应的min_r和max_r。具体来说：

1、不断向右移动左边界l，直到word[l]是一个元音字符

2、若此时的min_r \< l，则需要先置min_r \= l。接下来若l到min_r之间的子字符串没有涵盖所有的5个元音字符，且word[min_r]是一个元音字符，那么就将min_r向后移动。重复此过程直到word[min_r]不是元音字符，或者l到min_r之间以及涵盖了所有的5个元音字符

3、若l到min_r之间没有涵盖所有的5个元音字符，那么说明l到min_r之间的字符都不可用，此时直接将l置为min_r，然后回到步骤1重新开始执行

4、若l到min_r之间涵盖了所有的5个元音字符，那么说明l到min_r这一段是一个合法的子字符。若此时的max_r \< min_r，则需要先置max_r \= min_r。接下来不断向右移动max_r，直到word[max_r]不是一个元音字符。此时以l为左边界的合法子字符串，其最小右边界为min_r，最大右边界为max_r，因此一共有max_r - min_r + 1种合法的子字符串。使用这个值更新答案，然后将l向右移动一步，回到步骤1重新开始执行

这样一来，就得到了一个时间复杂度为O(n)的算法。

最后附上python代码：

```python
class Solution(object):
    def countVowelSubstrings(self, word):
        """
        :type word: str
        :rtype: int
        """

        l = 0
        min_r = 0
        max_r = 0
        n = len(word)
        cnt_dict = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
        res = 0
        flag = False
        while l < n:
            while l < n and word[l] not in cnt_dict:
                l += 1
                flag = False

            if l == n:
                break

            if min_r < l:
                min_r = l
            
            while min_r < n and word[min_r] in cnt_dict and not flag:
                cnt_dict[word[min_r]] += 1
                min_r += 1
                flag = True
                for cnt in cnt_dict.values():
                    if cnt == 0:
                        flag = False
                        break

            if not flag:
                for char in word[l : min_r]:
                    cnt_dict[char] -= 1
                l = min_r
                continue

            if max_r < min_r:
                max_r = min_r
            while max_r < n and word[max_r] in cnt_dict:
                max_r += 1

            res += max_r - min_r + 1

            cnt_dict[word[l]] -= 1
            if cnt_dict[word[l]] == 0:
                flag = False
            l += 1
        
        return res
```
