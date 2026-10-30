---
title: "1442. 形成两个异或相等数组的三元组数目"
aliases: ["yiduobo的每日leetcode 1442.形成两个异或相等数组的三元组数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/410401463"
zhihu_id: "410401463"
zhihu_title: "yiduobo的每日leetcode 1442.形成两个异或相等数组的三元组数目"
question_id: "1442"
question: "形成两个异或相等数组的三元组数目"
problem_url: "https://leetcode.cn/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/"
created: "2021-09-14T21:05:07+08:00"
updated: "2021-09-14T21:05:07+08:00"
upvotes: 0
comments: 0
---

# 1442. 形成两个异或相等数组的三元组数目

> **[yiduobo的每日leetcode 1442.形成两个异或相等数组的三元组数目](https://zhuanlan.zhihu.com/p/410401463) · 知乎 · 2021-09-14 · 赞同 0**
> 力扣：[1442. 形成两个异或相等数组的三元组数目](https://leetcode.cn/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1442.形成两个异或相等数组的三元组数目

[力扣](https://leetcode-cn.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/)

题目要求找出三元组(i, j, k)的数目，其中i \< j \<\= k

a \= arr[i] ^ arr[i + 1] ^ ... ^ arr[j - 1]

b \= arr[j] ^ arr[j + 1] ^ ... ^ arr[k]

且要求a \= b

根据异或的性质，a \= b也就意味着a ^ b \= 0。带回原式，就有

arr[i] ^ arr[i + 1] ^ ... ^ arr[j - 1] ^ arr[j] ^ ... ^ arr[k] \= 0

这是一个区间异或的形式，更进一步的，可以转化成一个前缀异或问题，即

prefix[k] \= arr[0] ^ arr[1] ^ ... ^ arr[i - 1] ^ arr[i] ^ arr[i + 1] ^ ... ^ arr[k]

prefix[i - 1] \= arr[0] ^ arr[1] ^ ... ^ arr[i - 1]

那么就有prefix[k] ^ prefix[i - 1] \= arr[i] ^ arr[i + 1] ^ ... ^ arr[k] \= 0

于是就可以使用哈希表统计每种异或值出现的位置，然后分析每种情况下可以得到的合法三元组数目。具体来说，就是一趟扫描，设当前处理到index这个为，且当前的前缀异或now。接下来枚举之前所有前缀异或为now的置为p，那么就有

arr[p] ^ arr[p + 1] ^ ... ^ arr[index] \= 0

于是我们可以将其拆分成若干个(i, j, k)三元组，此时的i为p，k为index，而j则可以由多种选择，分别为

j \= p + 1，那么就有arr[p] \= arr[p + 1] ^ ... ^ arr[index]

j \= p + 2，那么就有arr[p] ^ arr[p + 1] \= arr[p + 2] ^ ... ^ arr[index]

j \= p + 3，那么就有arr[p] ^ arr[p + 1] ^ arr[p + 2] \= arr[p + 3] ^ ... ^ arr[index]

...

j \= index，那么就有arr[p] ^ arr[p + 1] ^ ... ^ arr[index - 1] \= arr[index]

可以形成index - (p + 1) + 1一共index - p种合法的答案。计算完毕后，将index也加入到哈希表中即可。

最后附上python代码：

```python
class Solution(object):
    def countTriplets(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        pos_dict = {}
        pos_dict[0] = [0]
        now = 0
        res = 0
        for index, num in enumerate(arr):
            now ^= num
            if now not in pos_dict:
                pos_dict[now] = [index + 1]
            else:
                for last_pos in pos_dict[now]:
                    if index + 1 - last_pos >= 2:
                        res += index - last_pos
                pos_dict[now].append(index + 1)

        return res
```
