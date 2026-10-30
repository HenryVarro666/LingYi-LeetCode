---
title: "3518. 最小回文排列II"
aliases: ["yiduobo的每日leetcode 3518.最小回文排列II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902543867833738719"
zhihu_id: "1902543867833738719"
zhihu_title: "yiduobo的每日leetcode 3518.最小回文排列II"
question_id: "3518"
question: "最小回文排列 II"
problem_url: "https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/"
difficulty: "Hard"
rating: 2375
created: "2025-05-08T21:47:20+08:00"
updated: "2025-05-08T21:47:20+08:00"
upvotes: 0
comments: 0
---

# 3518. 最小回文排列II

> **[yiduobo的每日leetcode 3518.最小回文排列II](https://zhuanlan.zhihu.com/p/1902543867833738719) · 知乎 · 2025-05-08 · 赞同 0**
> 力扣：[3518. 最小回文排列 II](https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/) · Hard · 灵茶山艾府：[试填法 + 组合数学 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3518.最小回文排列II

[3518. 最小回文排列 II - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-palindromic-rearrangement-ii/description/)

题目给出一个回文字符串s以及一个整数k，其中k的大小在1到10^6之间。现在要求将s中的字符重新排列，得到字典序第k小的回文排列。如果不存在，则返回空字符串。

本题与上一题类似，不过需要计算的是字典序第k小的字符串，也就是需要将s的前半段重新排布，得到字典序第k小的字符串。

对于这类找第k小的问题，都可以采用类似康托展开之于全排列问题的处理方法，从最高位开始逐位填充。对于当前填充的字符，计算剩下字符可以形成的不同排列数量，然后根据这个数量与k的大小确定当前为是否应该填充这个字符。

对于本题，则是从最高位开始，尝试构造答案字符串的前半部分。首先使用一个哈希表cnt计算每种字符串出现的次数，接下来从最高位开始向下遍历。对于当前遍历到的位置p，再遍历'a'到'z'中的所有字符尝试填充。当然前提是当前cnt中还具有该字符。

接下来对于遍历到的第index种字符，先将其在cnt中出现的次数减去1，接下来就需要计算当前cnt中的这些字符放置在剩下的n // 2 - p - 1位中可以得到的不同排列数量。如果这个排列方案数tot大于等于k，那么说明当前位置就应该填充第index种字符，否则就应该将k减去tot，然后继续考察下一种填充的字符。若找不到可用的填充字符，那么说明无解，直接返回空字符。

接下来的问题就是如何计算剩下字符可以得到的不同排列数量。

对于这个问题，比较常规的计算方法是去重法。首先，这一共n // 2 - p - 1个字符一共可以形成(n // 2 - p - 1)！种排列，但是其中某些排列会出现重复，重复的根源则是cnt中相同的字符互换位置。具体来说，对于第x种字符，若其一共有cnt[x]个，那么对于每种字符的排列，这t个字符互换位置就一共会使得这种字符排列被计算cnt[x]！次，因此需要用总次数除以这个cnt[x]！。

不过对于本题，由于数据规模的问题，使用去重法免不了要计算大的阶乘，涉及到高精度的乘法和除法操作，写起来很麻烦。

另一种方法则是选位置法。遍历cnt中的每种字符，对于当前字符，不妨设其一共有t个，且当前剩下的位置有length个，那么此时就需要从这length个位置中选出t个来填充这些字符，因此一共有C(length, t)种选择的方案。将C(length, t)累乘到总的方案数tot中，然后对于剩下的字符，计算将这些字符填充到剩下的length - t个位置中的方案数然后累乘起来即可。

对于选位置法，涉及到了组合数的计算，看上去依然需要使用高精度乘法和除法，不过对于C(length, t)的计算，可以先利用组合数的性质，让t取min(t, length - t)，理由是C(length, t)和C(length, length - t)是相等的。接下来对于C(length, t)的计算，一般的计算方法是从1遍历到t，对于当前遍历到的因子x，将最终结果乘以(length - x + 1)，再除以x。由于在计算之前已经保证了t \<\= length // 2，因此(length - x + 1)必然是大于x的，也就是说这个组合数随着计算的进行是越来越大的。另一方面，由于本题中k的大小不超过10^6，而本题中填充字符时只需检测剩下字符可以形成的排列数目是否大于等于剩下的k，因此通过上面这个组合数计算填充方案时如果已经大于等于k了，那么就不需要继续向下计算了，直接返回可以填充的信号就可以了。这样一来，就避开了高精度的计算。

填充完前半段之后，只需将其翻转就得到了答案字符串的后半段，依然是根据s的奇偶性判断是否存在中间字符mid，然后拼接前半段与后半段得到最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def smallestPalindrome(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """
        
        n = len(s)
        cnt = [0] * 26
        for char in s[:n // 2]:
            cnt[ord(char) - 97] += 1
        
        def calc(cnt, length):
            tot = 1
            for index in range(26):
                if cnt[index] > 0:
                    t = min(cnt[index], length - cnt[index])
                    for x in range(1, t + 1):
                        tot = tot * (length - x + 1) // x
                        if tot >= k:
                            return k
                    length -= cnt[index]
            
            return tot

        left = []
        for p in range(n // 2):
            choose = None
            for index in range(26):
                if cnt[index] == 0:
                    continue

                cnt[index] -= 1
                tot = calc(cnt, n // 2 - p - 1)
                if tot >= k:
                    choose = index
                    break
                
                k -= tot
                cnt[index] += 1

            if choose is None:
                return ""
            else:
                left.append(chr(choose + 97))

        for index in range(26):
            if cnt[index] > 0:
                left.append(chr(index + 97))
                break

        left = ''.join(left)
        right = left[::-1]
        mid = ''
        if n % 2 == 1:
            mid = s[n // 2]
        return left + mid + right
```
