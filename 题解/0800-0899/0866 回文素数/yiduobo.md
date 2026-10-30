---
title: "866. 回文素数"
aliases: ["yiduobo的每日leetcode 866.回文素数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349916983"
zhihu_id: "349916983"
zhihu_title: "yiduobo的每日leetcode 866.回文素数"
question_id: "866"
question: "回文素数"
problem_url: "https://leetcode.cn/problems/prime-palindrome/"
created: "2021-02-10T20:49:52+08:00"
updated: "2021-02-10T20:49:52+08:00"
upvotes: 0
comments: 0
---

# 866. 回文素数

> **[yiduobo的每日leetcode 866.回文素数](https://zhuanlan.zhihu.com/p/349916983) · 知乎 · 2021-02-10 · 赞同 0**
> 力扣：[866. 回文素数](https://leetcode.cn/problems/prime-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

866.回文素数

[力扣](https://leetcode-cn.com/problems/prime-palindrome/)

这个问题有两个解决思路，一种是从N开始向上枚举素数，然后判断素数是否为回文数；另一种是从N开始向上枚举回文数，然后判断回文数是否为素数。

我在这里采用的是第二种做法。

首先，对于位数为偶数的回文数，其必然是11的倍数，其中只有11为素数，其他都是合数，因此在N>11时就不需要考虑位数为偶数的回文数了。

接下来，对于位数为奇数的回文数，其必然是ab...zMz...ba的形式，那么我就应当先确定ab...z的部分，然后从0到9枚举中间的M。枚举完一轮M之后，则将ab...z加上1，然后继续枚举M，直到找到一个素数。

剩下的问题就是如何确定枚举的起点了。对于给出的N，若其小于等于11，那么在这里从N开始向上逐个判断就行了，因此只讨论N大于11的情况：

1、根据上面位数为偶数的回文数必然除11外都不是素数可知，若N的位数为偶数，设其长度为L，那么下一个可能是素数的回文数必然是100...001，这里有L - 1个0，那么上面的ab...z就是100...00，这里0的个数为L/2 - 1，而M就是从0开始。

2、若N的位数为奇数，那么先将其分离成left、mid、right三个部分，其中mid为正中间那一位数。接下里需要对left和right的大小关系以及mid的值进行讨论：

2-1）若right小于等于反转后的left，那么说明比N的下一个回文数就应该是

[left][mid][reverse(left)]

这种形式，这里的reverse表示对left进行翻转。因此在这种情况下，ab...z的起始值就是left，M的起始值就是mid

2-2）若right大于反转后的left，那么说明下一个回文数是

[left][mid + 1][reverse(left)]

此时需要注意，若mid恰好为9，那么mid + 1就产生了进位，因此此时的回文数就变成了

[left + 1][0][reverse(left + 1)]

于是在这种情况下，若mid不等于9，那么ab...z的起始值为left，M的起始值为mid + 1；若mid等于9，那么ab...z的起始值为left + 1，M的起始值为0

确定了ab...z和M的起始值之后，就可以开始枚举了。首先对于L，若L是偶数，那么先将其加上1，因为我们现在考察的是长度为L的数。同时，这也决定了这里ab...z枚举的上界就是100...00，其中有L / 2 - 1个0。M的枚举上界则显然是9。每枚举完一个ab...z之后都应当从0开始再枚举M。

若当前长度L找不到答案，那么就将L加上2，然后重复上述步骤即可。

对于素数的判断，只需要考察当前枚举的数X是不是2到sqrt(X)中某个数的倍数即可。注意到这里答案保证在2\*10^9之内，我选择先使用筛法找出2到16384之间的素数将其储存起来，然后就只需要考察当前数X是不是这些素数的倍数了，这样可以节省一些判断素数的时间。

最后附上python代码：

```python
class Solution(object):
    def primePalindrome(self, N):
        """
        :type N: int
        :rtype: int
        """

        f = [None] * 16384
        x = 2
        while x < 16384:
            if f[x] is None:
                f[x] = True
                tmp = x + x
                while tmp < 16384:
                    f[tmp] = False
                    tmp += x
            if x == 2:
                x += 1
            else:
                x += 2
        
        prime_list = []
        for x in range(2, 16384):
            if f[x]:
                prime_list.append(x)
        
        while N <= 11:
            if self.check(N, prime_list):
                return N
            N += 1
        
        length = len(str(N))
        if length % 2 == 0:
            length += 1

        while True:
            if length == len(str(N)):
                mid = int(str(N)[length/2])
                start = int(str(N)[:length/2])
                reverse_start = int(str(N)[:length/2][::-1])
                end = int(str(N)[length/2 + 1:])
                if reverse_start >= end:
                    start_num = start
                elif reverse_start < end:
                    if mid == 9:
                        mid = 0
                        start_num = start + 1
                    else:
                        mid += 1
                        start_num = start
            else:
                start_num = int('1' + '0' * (length / 2 - 1))
                mid = 0

            for first_part in range(start_num, int('1' + '0' * (length / 2))):
                for mid_part in range(mid, 10):
                    now = str(first_part) + str(mid_part) + str(first_part)[::-1]
                    if self.check(int(now), prime_list):
                        return now
                mid = 0
            length += 2

    def check(self, now, prime_list):
        if now == 1:
            return False
    
        pos = 0
        while prime_list[pos] ** 2 <= now:
            if now % prime_list[pos] == 0:
                return False
            pos += 1
        
        return True
```
