---
title: "395. 至少有K个重复字符的最长子串"
aliases: ["yiduobo的每日leetcode 395.至少有K个重复字符的最长子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/179297564"
zhihu_id: "179297564"
zhihu_title: "yiduobo的每日leetcode 395.至少有K个重复字符的最长子串"
question_id: "395"
question: "至少有K个重复字符的最长子串"
problem_url: "https://leetcode.cn/problems/longest-substring-with-at-least-k-repeating-characters/"
created: "2020-08-10T23:25:29+08:00"
updated: "2020-08-10T23:25:29+08:00"
upvotes: 0
comments: 0
---

# 395. 至少有K个重复字符的最长子串

> **[yiduobo的每日leetcode 395.至少有K个重复字符的最长子串](https://zhuanlan.zhihu.com/p/179297564) · 知乎 · 2020-08-10 · 赞同 0**
> 力扣：[395. 至少有K个重复字符的最长子串](https://leetcode.cn/problems/longest-substring-with-at-least-k-repeating-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

395.至少有K个重复字符的最长子串<https://leetcode-cn.com/problems/longest-substring-with-at-least-k-repeating-characters/>

第一眼看上去感觉可以用分治法来做，即对于s中出现次数少于k次的字符，显然这些字符是不可能出现在最终答案中的，因此可以使用这些字符对s进行分割，然后对分割结果按同样的做法进行验证，直到其中所有字符出现的次数都大于等于k次为止。记录下最长的合法子串即为答案。

不过注意到题目保证了s中只有小写字符，因此我在这里采用的是枚举答案中不同字符的个数，然后使用滑动窗口的方式来找是否存在符合条件的子串。

首先，从1到26枚举允许出现的不同字符的数量char_cnt。

接下来使用两个指针l和r维护滑动窗口，并使用一个char_set来储存l到r这一段中每个字符出现的次数。不断将r往右移动，直到s[r]不在char_set中，且char_set中的字符数量已经达到了char_cnt。

当得到一组l和r之后，检测l到r这一段中字符数量是否达到了char_cnt个，且每个字符出现的次数是否达到了k次。这里的判断可以使用类似前缀和的思路来做预处理，即预处理出一个前缀和数组f，其中f[char][index]表示s的前index个字符中，char出现的次数。这个可以从左往右一趟扫描预处理出来。有了f之后，我们就可以通过f[char][r] - f[char][l - 1]得出l到r之间字符char出现的次数了，于是就可以在O(char_cnt)的时间内判断当前l到r是否合法。

在判断完当前的l到r之后，需要将l往右移动，直到l到r之间出现的不同字符数量小于char_cnt个。当s[l]被移除时，如果f[char][r] - f[char][l] \= 0，说明l +1到r之间已经不存在s[l]了，此时需要将s[l]从char_set中移除，同时说明此时l到r之间不同字符的数量已经小于char_cnt了。

由于最坏情况下需要枚举26次，每次扫描的时间复杂度为O(26n)，于是最终的时间复杂度为O(26^2 \* n)

需要注意的是，对于不同字符数量char_cnt而言，这里并不满足二分的性质，例如abab，在k\=2时有解，但在k\=1时无解，因此不能使用二分来确定char_cnt的大小，只能老老实实从1到26枚举。

最后附上python代码：

```python
class Solution(object):
    def longestSubstring(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        if not s:
            return 0

        sum_dict = {}
        for char in s:
            sum_dict[char] = [0]
        sum_dict[s[0]] = [1]

        for char in s[1:]:
            for key in sum_dict:
                sum_dict[key].append(sum_dict[key][-1])
            sum_dict[char][-1] += 1

        res = 0
        for char_cnt in range(len(sum_dict), 0, -1):
            char_set = set()
            l = 0
            r = 0
            while l < r or r < len(s):
                while r < len(s) and (len(char_set) < char_cnt or s[r] in char_set):
                    char_set.add(s[r])
                    r += 1

                if len(char_set) < char_cnt:
                    break

                if len(char_set) == char_cnt and res < r - l:
                    flag = True
                    for char in char_set:
                        if l == 0:
                            cnt = sum_dict[char][r - 1]
                        else:
                            cnt = sum_dict[char][r - 1] - sum_dict[char][l - 1]
                        if cnt < k:
                            flag = False
                            break
                    if flag:
                        res = r - l

                while l < r and len(char_set) >= char_cnt:
                    if sum_dict[s[l]][l] == sum_dict[s[l]][r - 1]:
                        char_set.remove(s[l])
                    l += 1

        return res
```
