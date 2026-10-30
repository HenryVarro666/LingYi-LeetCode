---
title: "1763. 最长的美好子字符串"
aliases: ["yiduobo的每日leetcode 1763.最长的美好子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460086331"
zhihu_id: "460086331"
zhihu_title: "yiduobo的每日leetcode 1763.最长的美好子字符串"
question_id: "1763"
question: "最长的美好子字符串"
problem_url: "https://leetcode.cn/problems/longest-nice-substring/"
created: "2022-01-20T23:46:37+08:00"
updated: "2022-01-20T23:46:37+08:00"
upvotes: 0
comments: 0
---

# 1763. 最长的美好子字符串

> **[yiduobo的每日leetcode 1763.最长的美好子字符串](https://zhuanlan.zhihu.com/p/460086331) · 知乎 · 2022-01-20 · 赞同 0**
> 力扣：[1763. 最长的美好子字符串](https://leetcode.cn/problems/longest-nice-substring/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1763.最长的美好子字符串

[力扣](https://leetcode-cn.com/problems/longest-nice-substring/)

由于这里字符串的长度很短，因此直接枚举所有子字符串然后检测也是可以的。不过注意到这里的字符全都是大写字符和小写字符，因此可以枚举答案中包含字符种类的数量，然后利用这个数量限制使用双指针来求解。具体来说是使用一个数组cnt_list记录当前区间内各个字符大写和小写出现的次数，并使用两个变量char_cnt和full_cnt分别记录字符的种数以及既有大写字符又有小写字符的字符种数。

枚举答案中字符种数target_cnt，然后使用两个指针l和r来寻找合法的答案。每次将r向后移动，此时应该使用s[r]来更新cnt_list，并根据具体情况决定是否需要更新char_cnt和full_cnt。由于这次移动可能会使得char_cnt超过target_cnt，那么还需要根据char_cnt和target_cnt的大小来向右移动l，并在过程中更新cnt_list、char_cnt以及full_cnt。当char_cnt合法后，判断当前的full_cnt是否恰好等于target_cnt，若等于，说明当前l到r就是一个合法的子字符串，那么使用l到r这一段来更新答案。

重复上面的过程直到r移动到字符串的末尾。

具体实现上，我将cnt_list组织成长度为2的子数组的形式，然后将a到z映射到cnt_list下标的0到25，然后将大写字母映射到子数组的下标0，小写字母映射到下标1，这样一来后续判断起来就方便一些。

最后附上python代码：

```python
class Solution(object):
    def longestNiceSubstring(self, s):
        """
        :type s: str
        :rtype: str
        """

        n = len(s)
        mapping_num = {}
        mapping_pos = {}
        for index in range(26):
            mapping_num[chr(index + 65)] = index
            mapping_num[chr(index + 97)] = index
            mapping_pos[chr(index + 65)] = 0
            mapping_pos[chr(index + 97)] = 1

        res_l = res_r = None
        max_len = 0

        for target_cnt in range(1, 26):
            l = r = 0
            cnt_list = [[0, 0] for _ in range(26)]
            char_cnt = 1
            full_cnt = 0
            num = mapping_num[s[r]]
            pos = mapping_pos[s[r]]
            cnt_list[num][pos] += 1

            while r + 1 < n:
                r += 1
                num = mapping_num[s[r]]
                pos = mapping_pos[s[r]]
                if cnt_list[num][pos] == 0:
                    if cnt_list[num][1 - pos] == 0:
                        char_cnt += 1
                    else:
                        full_cnt += 1
                cnt_list[num][pos] += 1

                while l < r and char_cnt > target_cnt:
                    num = mapping_num[s[l]]
                    pos = mapping_pos[s[l]]
                    if cnt_list[num][pos] == 1:
                        if cnt_list[num][1 - pos] == 0:
                            char_cnt -= 1
                        else:
                            full_cnt -= 1
                    
                    cnt_list[num][pos] -= 1
                    l += 1
                
                if full_cnt == target_cnt:
                    if r - l + 1 > max_len:
                        max_len = r - l + 1
                        res_l, res_r = l, r

        if max_len == 0:
            return ""
        return s[res_l : res_r + 1]
```
