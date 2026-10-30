---
title: "420. 强密码检验器"
aliases: ["yiduobo的每日leetcode 420.强密码检验器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/193135720"
zhihu_id: "193135720"
zhihu_title: "yiduobo的每日leetcode 420.强密码检验器"
question_id: "420"
question: "强密码检验器"
problem_url: "https://leetcode.cn/problems/strong-password-checker/"
created: "2020-08-21T23:31:29+08:00"
updated: "2020-08-21T23:31:29+08:00"
upvotes: 0
comments: 0
---

# 420. 强密码检验器

> **[yiduobo的每日leetcode 420.强密码检验器](https://zhuanlan.zhihu.com/p/193135720) · 知乎 · 2020-08-21 · 赞同 0**
> 力扣：[420. 强密码检验器](https://leetcode.cn/problems/strong-password-checker/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

420.强密码检验器<https://leetcode-cn.com/problems/strong-password-checker/>

题目难度其实不大，就是细节需要想清楚。

首先，可以通过一趟扫描确定s中是否有大写字母、小写字母以及数字，同时可以统计出连续出现相同字符3次或以上的子串的长度与数量。

接下来，对于s的长度，设为l，那么：

1、若l小于6，那么需要补充6 - l个字符，此时可以顺便填充缺失的种类。

此时的连续字符串无需担心，因为当连续出现小于等于4次时，例如aaaa，可以插入一个字符成为aaXaa，而当连续出现5次时，必然只会是大写字符、小写字符或者数字中的一种，于是需要额外填补2个字符，正好也可以将这5个连续字符隔开。

于是，此时的答案就是max(6 - l, cate_loss_cnt)

2、若l大于6且l小于等于20，那么此时只需要解决重复出现以及缺失种类的情况。

那么对于重复出现的情况，例如XXXXXX...，可以将其在第3、6、9...个字符替换掉，最终就变成了XXYXXY...

那么对于所有重复出现次数超过3次的字串，将它们的长度记录在same_list中，那么最终就需要替换掉sum(same[i] / 3)个字符，将其记为deal3。

同时，在进行替换的过程中，可以顺带处理缺失种类。

于是，此时的答案就是max(deal3, cate_loss_cnt)

3、若l的长度大于20，那么需要删去l - 20个字符，设为del_cnt。

在删除的过程中可以顺带处理重复出现的情况，此时应该对于重复次数mod3进行讨论。分别统计same_list中的长度为3的取模情况，分别记为mod3_cnt[0]，mod3_cnt[1]与mod3_cnt[2]，表示长度为3m，3m + 1以及3m + 2出现的次数。

1）当重复字符子串长度为3m时，本来应该进行m次替换，但此时可以删去一个字符，然后替换m - 1次。于是当del_cnt \<\= mod3_cnt[0]时，可以在长度为3m的串中选出del_cnt个串，分别删去一个字符，此时s的长度就达标了。不过需要注意的是，这里的删除操作与cate_loss的替换操作是可能产生冲突的，例如现在只存在一个重复字符串XXX，且此时s的长度为21，同时缺少小写字符，那么此时XXX只能选择删去一个字符满足s的长度要求，或者替换一个字符满足种类要求。于是此时可以顺带进行的操作次数就是max(deal3 - del_cnt, cate_loss)，因此最终的答案就是max(deal3 - del_cnt, cate_loss) + l - 20

2）当重复字符子串长度为3m + 1时，与上面类似，不过这里需要进行两次删除操作才能节省一次替换操作，于是应该优先对于长度为3m的情况进行处理。当长度为3m的情况全部处理掉之后，应该就剩下del_cnt - mod3_cnt[0]个字符需要处理，将其记为新的del_cnt。同样的，需要处理的重复字符串操作次数也从deal3变成了deal3 - mod3_cnt[0]。

那么，若del_cnt \<\= mod3_cnt[1] \* 2时，就可以在长度3m + 1的串中选出del_cnt / 2个串，分别删去两个字符，此时s的长度就达标了。同样的，这里的删除操作可能与cate_loss冲突，于是最终答案就是max(deal3 - del_cnt / 2，cate_loss) + l - 20

3）若通过上面两步还未处理完成，那么对于剩下的长度为3m + 2的子串，则需要三次删除操作才能节省一次替换操作，其他的则与上面的类似，此时del_cnt应该减去mod3_cnt[1] \* 2，那么最终答案就是max(deal3 - del_cnt / 3, cate_loss) + l - 20

最后附上代码：

```python
class Solution(object):
    def strongPasswordChecker(self, s):
        """
        :type s: str
        :rtype: int
        """

        lower_flag = upper_flag = digit_flag = 1
        same_list = []
        now = None
        cnt = 0

        for char in s:
            if char >= 'a' and char <= 'z':
                lower_flag = 0
            elif char >= 'A' and char <= 'Z':
                upper_flag = 0
            elif char >= '0' and char <= '9':
                digit_flag = 0
            
            if now is None or now != char:
                now = char
                if cnt >= 3:
                    same_list.append(cnt)
                cnt = 1
            else:
                cnt += 1

        if cnt >= 3:
            same_list.append(cnt)

        cate_loss = lower_flag + upper_flag + digit_flag
        if len(s) < 6:
            return max(6 - len(s), cate_loss)

        else:
            deal3 = 0
            mod3_cnt = [0, 0, 0]
            for same in same_list:
                deal3 += same / 3
                mod3_cnt[same % 3] += 1
            
            if len(s) <= 20:
                return max(deal3, cate_loss)
            else:
                del_cnt = len(s) - 20
                if del_cnt <= mod3_cnt[0]:
                    return max(deal3 - del_cnt, cate_loss) + len(s) - 20

                del_cnt -= mod3_cnt[0]
                deal3 -= mod3_cnt[0]
                if del_cnt <= mod3_cnt[1] * 2:
                    return max(deal3 - del_cnt / 2, cate_loss) + len(s) - 20

                del_cnt -= mod3_cnt[1] * 2
                deal3 -= mod3_cnt[1]
                return max(deal3 - del_cnt / 3, cate_loss) + len(s) - 20
```
