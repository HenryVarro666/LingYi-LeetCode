---
title: "3365. 重排子字符串以形成目标字符串"
aliases: ["yiduobo的每日leetcode 3365.重排子字符串以形成目标字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27738775882"
zhihu_id: "27738775882"
zhihu_title: "yiduobo的每日leetcode 3365.重排子字符串以形成目标字符串"
question_id: "3365"
question: "重排子字符串以形成目标字符串"
problem_url: "https://leetcode.cn/problems/rearrange-k-substrings-to-form-target-string/"
difficulty: "Medium"
rating: 1514
created: "2025-03-04T00:28:56+08:00"
updated: "2025-03-04T00:28:56+08:00"
upvotes: 1
comments: 0
---

# 3365. 重排子字符串以形成目标字符串

> **[yiduobo的每日leetcode 3365.重排子字符串以形成目标字符串](https://zhuanlan.zhihu.com/p/27738775882) · 知乎 · 2025-03-04 · 赞同 1**
> 力扣：[3365. 重排子字符串以形成目标字符串](https://leetcode.cn/problems/rearrange-k-substrings-to-form-target-string/) · Medium · 灵茶山艾府：[哈希表/排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3365.重排子字符串以形成目标字符串

[3365. 重排子字符串以形成目标字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/rearrange-k-substrings-to-form-target-string/description/)

题目给出两个字符串s和t，这两个字符串互为字母异味词，即将某个字符串中的字符重新排列后可以得到另一个字符串。

现在要求判断能否将s分割成k个等长的子串，重新排列这些子串后再重新连接这些子串，可以使得得到的新字符串与t相同。

不妨设s的长度为n，由于题目要求分割的子串长度相同，那么划分方案就只能是按n // k为一组分割出k个子串。方便起见，在这里记length \= n // k。

在这些子串在重新排列后，第一个子串需要与t中的前length个字符相同，第二个子串需要与t中的第length到第length \* 2 - 1个字符相同，以此类推。换言之，如果在这里将t也同样按length个字符一组分割成k个子串，问题就变成了将s分割成k个长度length的子串，问能否将这k个子串重新排列后变得和t分割出来的k个子串相同。

更进一步的，如果给出的是两个长度为k的整数数组，问能否将第一个数组重新排列后变为第二个数组，对于这个问题使用排序或者哈希表就可以轻松解决。而对于本题，只需将划分出来的子串视为独立的元素，就同样可以使用排序或者哈希表来进行判断了。

最后附上python代码：

```python
class Solution(object):
    def isPossibleToRearrange(self, s, t, k):
        """
        :type s: str
        :type t: str
        :type k: int
        :rtype: bool
        """
        
        n = len(s)
        length = n // k

        parts_s = []
        parts_t = []
        for index in range(k):
            parts_s.append(s[index * length : (index + 1) * length])
            parts_t.append(t[index * length : (index + 1) * length])
        
        return sorted(parts_s) == sorted(parts_t)
```
