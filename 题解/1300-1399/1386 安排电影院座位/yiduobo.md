---
title: "1386. 安排电影院座位"
aliases: ["yiduobo的每日leetcode 1386.安排电影院座位"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/402845850"
zhihu_id: "402845850"
zhihu_title: "yiduobo的每日leetcode 1386.安排电影院座位"
question_id: "1386"
question: "安排电影院座位"
problem_url: "https://leetcode.cn/problems/cinema-seat-allocation/"
difficulty: "Medium"
created: "2021-08-23T23:00:21+08:00"
updated: "2021-08-23T23:00:21+08:00"
upvotes: 1
comments: 0
---

# 1386. 安排电影院座位

> **[yiduobo的每日leetcode 1386.安排电影院座位](https://zhuanlan.zhihu.com/p/402845850) · 知乎 · 2021-08-23 · 赞同 1**
> 力扣：[1386. 安排电影院座位](https://leetcode.cn/problems/cinema-seat-allocation/) · Medium · 灵茶山艾府：[用位运算简化判断逻辑（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1386.安排电影院座位

<https://leetcode-cn.com/problems/cinema-seat-allocation/>

首先，由于这里的行数非常多，因此我们不能考虑每一行。注意到每一行最多安排两组家庭，因此最多只能安排n \* 2组家庭，先初始化答案为n \* 2。

接下来，我们只需要考虑有预定位置的那些行。注意到最左侧和最右侧的位置是不能安排家庭的，因此对于reservedSeats中最左侧和最右侧的位置是无需考虑的。而对于其他的座位，我们按照行聚合，得到每一行的预定情况，接下来枚举预定的每一行：

1、首先我们先将答案减去2，表示最差情况下这一行无法安排。接下来再考察这一行的具体预定情况，看看能否安排一组家庭。具体来说，对于这一行2-9这一共8个位置，我们预定的位置的分布情况，再看看能否安排一组家庭。

2、若该行已预订的座位超过4个，那么该行无法再安排家庭，否则就将预定的座位从小到大进行排序，然后考察一下的情况：

2-1）若预定的最左侧位置大于5，那么我们可以安排2、3、4、5四个位置，将答案加上1

2-2）若预定的最右侧位置小于6，那么我们可以安排6、7、8、9四个位置，将答案加上1

2-3）若上面两种情况都不满足，那么我们只能尝试安排4、5、6、7这四个位置，那么首先最左侧的位置必须小于4，最右侧的位置必须大于7，而此时根据预定座位的数目可以再分成几种情况：

若当前行仅有两个位置被预定，也就是最左侧和最右侧的位置，那么说明此时可以安排中间四个位置，将答案加上1

若当前行有三个位置被预定，那么需要判断中间那个被预定的位置是否小于4或者大于7，若满足，将答案加上1

若当前行有四个位置被预定，想要在中间安排一组家庭，预定的位置就必须在2、3、8、9才行，若满足，将答案加上1

最后附上python代码：

```python
class Solution(object):
    def maxNumberOfFamilies(self, n, reservedSeats):
        """
        :type n: int
        :type reservedSeats: List[List[int]]
        :rtype: int
        """

        res = n * 2
        reserved_dict = {}
        for x, y in reservedSeats:
            if y != 1 and y != 10:
                if x not in reserved_dict:
                    reserved_dict[x] = []
                reserved_dict[x].append(y)
        
        for x in reserved_dict:
            res -= 2
            reserved_list = sorted(reserved_dict[x])
            if len(reserved_list) > 4:
                continue
            
            if len(reserved_list) == 1:
                res += 1
            elif reserved_list[0] > 5:
                res += 1
            elif reserved_list[-1] < 6:
                res += 1
            elif reserved_list[0] < 4 and reserved_list[-1] > 7:
                if len(reserved_list) == 2:
                    res += 1
                elif len(reserved_list) == 3 and (reserved_list[1] < 4 or reserved_list[1] > 7):
                    res += 1
                elif reserved_list[1] == 3 and reserved_list[2] == 8:
                    res += 1
        
        return res
```
