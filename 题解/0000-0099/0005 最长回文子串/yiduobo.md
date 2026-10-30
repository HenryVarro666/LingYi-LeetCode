---
title: "5. 最长回文子串"
aliases: ["yiduobo的每日leetcode 5.最长回文子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/string", "leetcode/enumeration", "题单/动态规划", "题单/字符串", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/八-区间-DP", "题单/字符串/三-Manacher-算法-回文串", "题单/LeetCode-热题-100/多维动态规划", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/113060786"
zhihu_id: "113060786"
zhihu_title: "yiduobo的每日leetcode 5.最长回文子串"
question_id: "5"
question: "最长回文子串"
problem_url: "https://leetcode.cn/problems/longest-palindromic-substring/"
difficulty: "Medium"
created: "2020-03-14T00:09:40+08:00"
updated: "2020-03-14T00:09:40+08:00"
upvotes: 1
comments: 0
---

# 5. 最长回文子串

> **[yiduobo的每日leetcode 5.最长回文子串](https://zhuanlan.zhihu.com/p/113060786) · 知乎 · 2020-03-14 · 赞同 1**
> 力扣：[5. 最长回文子串](https://leetcode.cn/problems/longest-palindromic-substring/) · Medium · 灵茶山艾府：[两种方法：中心扩展法 / Manacher 算法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

5.最长回文子串<https://leetcode-cn.com/problems/longest-palindromic-substring/>

**O(n^2)的做法：**

枚举每个中心点，然后从中心点往两边比较字符是否相同。对于偶串的情况，可以在每个字符之间插入特殊字符，强行转换成奇串。例如abba，插入后变成a\#b\#b\#a，那么最长回文子串就是以第二个\#为中心比较得到的。

从头开始遍历每个字符，然后往两边比较的次数最坏情况下是从1开始，递增到n/2，所以总的时间复杂度就是O(n^2)。

**后缀数组O(nlogn)/O(n)：**

后缀数组在处理字符串问题上非常强大，其利用到了字符串后缀之间的性质。后缀的就是字面上的意思，例如abac，有四个后缀，分别为

最后一位的c

最后两位的ac

最后三位的bac

最后四位的abac

后缀数组就是将这些后缀组织起来之后，通过字典顺序排序得到的数组。其生成方式有倍增 O(nlogn)和DC3 O(n)两种方法。然后因为后缀之间的性质，可以在O(n)的时间内得到**相邻两个后缀的最长公共前缀**是多长。

对于这个回文问题，经典的做法是将原串倒装之后加上分隔符接在后面，例如上面的abac，变形之后成为abac\$caba，那么可以发现，位于**\$两侧的两个后缀的最长公共前缀**即为最长公共子串，在这里为abac\$caba与aba的最长公共前缀aba。

后缀数组的具体实现在这里不展开，因为这篇题解主要还是讲的下面更优美的马拉车算法。

**马拉车算法O(n)：**

马拉车算法的主要思路为，对于一个大回文区间，如果其中心点左侧存在小回文区间，那么其右侧对应位置必然也存在同样的小回文区间。需要注意的是，为了有中心点这个概念，依然需要使用暴力法中的插入特殊字符，来将答案转化成奇串。

例如eabafcfabag，这里以c为中心，半径为5的串abafcfaba为大回文串，当我们知道以第一个b为中心，半径为2的串aba为小回文串，那么大回文串对称位置的第二个b为中心，半径为2的串也一定是小回文串。因此，在知道大回文区间的情况下，现存的小回文区间可以通过过去已知的小回文区间得知，这样可以保证从左往右扩展时每个字符仅计算一次，因此最终时间复杂度为O(n)。

那么我们可以维护一个最右的回文区间，然后以f[i]表示以位置i为中心的，最长回文串的半径，从左往右计算f数组的值。

例如当前最靠右的回文区间以mid为中心，右边界为right，那么对于在mid到right之间的i，根据mid的对称位置为j \= mid - (i - mid) \= mid \* 2 - i，可以得到f[i] \= min(f[j], right - i)。这里取min的意思是需要严格保证左右两个小回文区间都处于大回文区间内，才有对称的性质。如果f[i]超出了右边界，那么说明以i为中心，f[i]为半径的串超出right的部分不再等于以j为中心，f[j]为半径的串超出左侧边界的部分(因为大回文区间的边界表明这两部分不相等)，即以i为中心，半径为f[i]的串不再具有回文性质。

通过对称性质更新得到f[i]之后，还需要尝试继续往right外面扩展。因为大回文在right右侧不匹配，不代表小回文区间也无法继续往后匹配。扩展完毕之后，需要维护mid与right，更新最右回文区间的位置。

最后附上python代码：

其中index \< right分支下的语句即为通过对称小回文区间更新f[i]，while循环为继续往外扩展，最后的right \< index + f[index]则是更新最右回文区间的位置。

需要特别小心的是，最后通过f数组获取答案时，需要仔细计算去掉特殊字符后的长度。

```python
class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        s = '!' + '#'.join(list(s)) + '@'
        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(s) - 1, 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index
    
        max_len = 0
        max_pos = 0
        for index in range(1, len(s) - 1, 1):
            if s[index] == '#':
                now_len = f[index] / 2 * 2
            else:
                now_len = (f[index] - 1) / 2 * 2 + 1
            if now_len > max_len:
                max_len = now_len
                max_pos = index
        return s[max_pos - f[max_pos] + 1 : max_pos + f[max_pos]].replace('#', '')
```
