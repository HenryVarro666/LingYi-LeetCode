---
title: "777. 在LR字符串中交换相邻字符"
aliases: ["yiduobo的每日leetcode 777.在LR字符串中交换相邻字符"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/339901859"
zhihu_id: "339901859"
zhihu_title: "yiduobo的每日leetcode 777.在LR字符串中交换相邻字符"
question_id: "777"
question: "在 LR 字符串中交换相邻字符"
problem_url: "https://leetcode.cn/problems/swap-adjacent-in-lr-string/"
difficulty: "Medium"
rating: 2337
created: "2020-12-27T16:43:02+08:00"
updated: "2020-12-27T16:43:02+08:00"
upvotes: 0
comments: 0
---

# 777. 在LR字符串中交换相邻字符

> **[yiduobo的每日leetcode 777.在LR字符串中交换相邻字符](https://zhuanlan.zhihu.com/p/339901859) · 知乎 · 2020-12-27 · 赞同 0**
> 力扣：[777. 在 LR 字符串中交换相邻字符](https://leetcode.cn/problems/swap-adjacent-in-lr-string/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

777.在LR字符串中交换相邻字符

[力扣](https://leetcode-cn.com/problems/swap-adjacent-in-lr-string/)

首先，题目中的L和R是不能进行交换的，因此如果单独把start和end中L和R扣出来，那么这个序列是不能动的，因此我们可以将其分离出来，然后以每个L或R作为gate，统计gate之间的X个数，长度为k的LR序列一共可以将X分为k + 1段，这个X段的长度可以为0。

对于样例中的RXXLRXRXL以及XRLXXRRLX，二者的LR序列都是RLRRL，各个gate之间的X个数则分别是

start：0, 2, 0, 1, 1, 0

end： 1, 0, 2, 0, 0, 1

统计完成后，若start的LR序列和end的LR序列不一致，那么必然无法从start转换成end，直接返回false。否则，我们就需要想办法将start的X序列转换成end的X序列。

那么从头开始往后扫描start和end中每个对应的part，对于当前part：

1、若start中的X个数等于end中的X个数，那么不需要进行任何操作

2、若start中的X个数小于end中的X个数，设这个差值为delta，那么需要从start的下一个part中薅delta个X过来。若当前part的gate不为R，那么没办法从下一个part中获取到X，于是返回false，否则就从下一个part中拿delta的X，此时需要将下一个part中的cnt个数减去delta。

3、若start中的X个数大于end中的X个数，此时与情况2相似，不过是需要将多出的X送给下一个part，那么此时就需要对应的gate为L。若为L，下一个part中的cnt应该加上delta，否则直接返回false。

当处理完前k个part之后，最后剩下的第k + 1个part必然是一样的，因为start和end的长度一致，LR序列一致，同时前k个part匹配上了，因此最后剩下的part也是一致的，此时就可以返回true了。

最后附上python代码：

```python
class Solution(object):
    def canTransform(self, start, end):
        """
        :type start: str
        :type end: str
        :rtype: bool
        """

        cnt = 0
        s_cnt = []
        s_gate = []
        for char in start:
            if char == 'X':
                cnt += 1
            else:
                s_cnt.append(cnt)
                cnt = 0
                s_gate.append(char)
        s_cnt.append(cnt)

        cnt = 0
        e_cnt = []
        e_gate = []
        for char in end:
            if char == 'X':
                cnt += 1
            else:
                e_cnt.append(cnt)
                cnt = 0
                e_gate.append(char)
        e_cnt.append(cnt)

        if s_gate != e_gate:
            return False

        for index in range(len(s_gate)):
            if s_cnt[index] < e_cnt[index]:
                if s_gate[index] == 'R':
                    s_cnt[index + 1] -= (e_cnt[index] - s_cnt[index])
                else:
                    return False
            elif s_cnt[index] > e_cnt[index]:
                if s_gate[index] == 'L':
                    s_cnt[index + 1] += (s_cnt[index] - e_cnt[index])
                else:
                    return False
        
        return True
```
