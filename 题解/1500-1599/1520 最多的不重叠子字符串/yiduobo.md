---
title: "1520. 最多的不重叠子字符串"
aliases: ["yiduobo的每日leetcode 1520.最多的不重叠子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/depth-first-search", "leetcode/graph", "leetcode/binary-search", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/421620220"
zhihu_id: "421620220"
zhihu_title: "yiduobo的每日leetcode 1520.最多的不重叠子字符串"
question_id: "1520"
question: "最多的不重叠子字符串"
problem_url: "https://leetcode.cn/problems/maximum-number-of-non-overlapping-substrings/"
difficulty: "Hard"
rating: 2363
created: "2021-10-15T00:00:04+08:00"
updated: "2021-10-15T00:00:04+08:00"
upvotes: 0
comments: 0
---

# 1520. 最多的不重叠子字符串

> **[yiduobo的每日leetcode 1520.最多的不重叠子字符串](https://zhuanlan.zhihu.com/p/421620220) · 知乎 · 2021-10-15 · 赞同 0**
> 力扣：[1520. 最多的不重叠子字符串](https://leetcode.cn/problems/maximum-number-of-non-overlapping-substrings/) · Hard · 灵茶山艾府：[有向图建模+合并区间+无重叠区间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1520.最多的不重叠子字符串

[力扣](https://leetcode-cn.com/problems/maximum-number-of-non-overlapping-substrings/)

根据题目中的条件2，那么实际上对于每种字符，最终只会有一个合法且长度最短的字符串包含了所有的这些字符。若将这个字符串的起始和结尾视为一个区间，那么最终就会得到最多26个区间，然后要求尽可能多地选出其中不重叠的区间。于是现在问题就转化成了两步：

1、如何高效对每个字符char求解最短且合法的字符串，使得所有的char都出现在该字符串中

2、对于步骤1中求得的最多26个字符串，将其视为区间并从中尽可能多地选出区间

首先考虑问题1。一个自然的想法就是对于每种字符，先找到该字符第一次和最后一次出现的位置，分别记为l和r。那么对于l到r之间的所有字符，同样是需要找到这个字符第一次和最后一次出现的位置，并用这两个位置来更新l和r。若这一轮l和r被更新过，说明区间扩展了，新加入了字符，需要再次进行扩展，直到l和r定住不动位置。

在具体实现上，可以先一趟扫描，在统计每个字符第一次和最后一次出现位置的同时，顺便计算每个字符出现次数的前缀和。那么对于当前的l和r而言，其中各个字符出现的次数就可以通过前缀和在O(1)的时间复杂度内求解。若某个字符char出现次数为0，说明无需考虑char，否则就需要用char第一次和最后一次出现的位置来更新l和r，并重复这个过程直到l和r不再变化。时间复杂度方面，由于每个字符最多被扩展一次，但每次扩展都需要遍历所有的字符，因此理论上这一步的时间复杂度为O(26n + 26^2)，其中26n为遍历统计的时间复杂度，而后面的26^2则为计算各个区间的时间复杂度。

得到各个区间之后，接下来考虑问题2。

首先可以明确的一点是，这些区间只可能出现互补相交，或者一个区间是另一个区间的子区间这两种情况，因为若出现常规情况下的区间[l1, r1]与区间[l2, r2]由于l1 \< l2 \<\= r1 \< r2相交的话，那么对于l2到r1之间的这些字符而言：

1、若其仅出现在l2到r1之间的话，那么l1到r1完全可以分割成l1到l2 - 1以及l2到r1这两个区间，但由于l1到r1是扩展出来的，因此分割的情况必然是不合法的

2、若其也出现在l1到l2 - 1之间的话，那么对于区间l2到r2而言，l2到r1之间的部分字符出现在了l2的左侧，那么l2到r2同样是不合法的区间

综合起来，就说明最终这些要么全包围，要么不相交。于是就有了一种做法。对于这些区间，按其左边界从小到大进行排序，并记录待比较区间的边界now_l和now_r。接下来对于后续的区间：

1、若当前区间的左边界ll > now_r，那么说明当前区间后续所有区间的左边界都会大于now_r，也就是说待比较区间[now_l, now_r]与后面所有区间都不相交，于是可以将其加入到答案中，并更新now_l，now_r为l和r

2、若当前区间的左边界l小于等于now_r，说明当前区间将被now_l和now_r全面覆盖住。此时必然有r \<\= now_r，且当前区间l到r的长度小于等于now_l到now_r的长度，也就是说此时选择当前区间[l, r]必然是比选择[now_l, now_r]更优的，因此此时直接将now_l，now_r更新为l和r然后考虑后续区间即可

需要特别注意的是，在遍历完成后，还需要将当前最后一个区间，也就是当前的[now_l, now_r]加入到答案当中。

最后附上python代码：

```python
class Solution(object):
    def maxNumOfSubstrings(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        cnt_list = [{}]
        pos_dict = {}
        for index, char in enumerate(s):
            cnt_list.append(cnt_list[-1].copy())
            cnt_list[-1][char] = cnt_list[-1].get(char, 0) + 1
        
            if char not in pos_dict:
                pos_dict[char] = [index + 1, index + 1]
            else:
                pos_dict[char][1] = index + 1
        
        intervals = []
        for asc in range(97, 123):
            char = chr(asc)
            if char in pos_dict:
                l, r = pos_dict[char]
                while True:
                    new_l, new_r = l, r
                    for char in cnt_list[new_r]:
                        if cnt_list[new_r][char] - cnt_list[new_l - 1].get(char, 0) > 0:
                            if pos_dict[char][0] < new_l or pos_dict[char][1] > new_r:
                                new_l, new_r = min(new_l, pos_dict[char][0]), max(new_r, pos_dict[char][1])
                    
                    if l == new_l and r == new_r:
                        break
                    l, r = new_l, new_r

                intervals.append([l, r])
        
        intervals = sorted(intervals, key=lambda d:d[0])
        res = []
        now_l, now_r = intervals[0]
        for l, r in intervals[1:]:
            if l > now_r:
                res.append(s[now_l - 1:now_r])

            now_l, now_r = l, r
        
        res.append(s[now_l - 1 : now_r])
        return res
```
