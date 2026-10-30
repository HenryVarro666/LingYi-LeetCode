---
title: "3348. 最小可整除数位乘积II"
aliases: ["yiduobo的每日leetcode 3348.最小可整除数位乘积II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "leetcode/bao-li", "题单/动态规划", "题单/贪心算法", "题单/动态规划/十-数位-DP", "题单/动态规划/专题-输出具体方案-打印方案", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26086771463"
zhihu_id: "26086771463"
zhihu_title: "yiduobo的每日leetcode 3348.最小可整除数位乘积II"
question_id: "3348"
question: "最小可整除数位乘积 II"
problem_url: "https://leetcode.cn/problems/smallest-divisible-digit-product-ii/"
difficulty: "Hard"
rating: 3101
created: "2025-02-24T22:35:15+08:00"
updated: "2025-02-24T22:35:15+08:00"
upvotes: 0
comments: 0
---

# 3348. 最小可整除数位乘积II

> **[yiduobo的每日leetcode 3348.最小可整除数位乘积II](https://zhuanlan.zhihu.com/p/26086771463) · 知乎 · 2025-02-24 · 赞同 0**
> 力扣：[3348. 最小可整除数位乘积 II](https://leetcode.cn/problems/smallest-divisible-digit-product-ii/) · Hard · 灵茶山艾府：[两种方法：从左到右暴搜/从右到左枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3348.最小可整除数位乘积II

[3348. 最小可整除数位乘积 II - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-divisible-digit-product-ii/)

题目给出一个字符串num，表示一个正整数，同时给出一个整数t。若一个整数中没有任何数位为0，那么就称这个整数为无零数字。对于给出的num，要求找出大于等于num的最小无零整数，且各数位之积能被t整除。若不存在这样的正数，则返回-1。

首先可以明确的是，由于答案整数中的数位由1到9组成，那么其各数位之积必然可以写成(2^a) \* (3^b) \* (5^c) \* (7^d)，也就是说，t如果有2、3、5、7之外的质因子，那么必然找不到合法的答案整数。于是可以先对t将其中的2、3、5、7都分离出来，不妨记为cnt，若分离完之后t不等于1，说明还存在其他质因子，此时应该直接返回-1。

---

接下来对于分离出的这些质因子cnt，可以想办法先实现一个构造函数generate，其作用是对于数组cnt，各数位之积可以被(2^cnt[0]) \* (3^cnt[1]) \* (5^cnt[2]) \* (7^cnt[3])整除的最小整数是多少。

对于5和7的处理方法是比较简单的，因为这两个质因子无法再次进行组合，因此这个最小整数中一定需要有cnt[2]个5以及cnt[3]个7。方便起见，记five为cnt[2]个5拼接得到的字符串，seven为cnt[3]个7拼接得到的字符串。

对于2和3的处理，由于可以进行组合，因此需要根据具体情况进行分析。为了使得构造出来的整数最小，因此需要让这个整数的长度尽量多，也就是说应该尽量进行组合。可行的组合方式分别为

2 \* 2 \* 2 \= 8

2 \* 2 \= 4

3 \* 3 \= 9

2 \* 3 \= 6

直观上来看，应该尽量先构造9和8，这样一来既可以使得需要的数位组小，也可以使得剩下用不完的2和3构成的数最小。例如两个2和两个3，可以两个2构成4，两个3构成9，得到49，或者构成两组2\*3 \= 6，得到66，此时构成49显然是更优的。一个比较简单的理解是构成的9和8越多，剩下的数就越小，把这些小的数放在高位上得到的最终结果必然最小。

根据上面的结论，接下来就可以对2的数量cnt[0]和3的数量cnt[1]分情况讨论。方便起见，可以先记eight为(cnt[0] // 3)个8拼接得到的字符串，nine为(cnt[1] // 2)个9拼接得到的字符串。

1、若cnt[0]是3的倍数，cnt[1]是2的倍数：

此时没有额外的2和3，只需将5、7、8、9拼接起来就行了，得到的结果就是

mi \= five + seven + eight + nine

2、若cnt[0]是3的倍数，cnt[1]模2余1：

此时有一个落单的3，应该将其拼在字符串的最前面，得到的结果就是

mi \= '3' + five + seven + eight + nine

3、若cnt[0]模3余1，cnt[1]是2的倍数：

此时有一个落单的2，应该将其拼在字符串的最前面，得到的结果就是

mi \= '2' + five + seven + eight + nine

4、若cnt[0]模3余1，cnt[1]模2余1：

此时有一个落单的2和一个落单的3，应该组合成一个6。需要注意这里的6应该放在5的后面，得到的结果就是

mi \= five + '6' + seven + eight + nine

5、若cnt[0]模3余2，cnt[1]是2的倍数：

此时有两个落单的2，应该组合成一个4然后将其拼在字符串的最前面，得到的结果就是

mi \= '4' + five + seven + eight + nine

6、若cnt[0]模3余2，cnt[1]模2余1：

此时有两个落单的2，一个落单的3。根据上面的结果，应该尽量先组合出大的数字，因此在这里应该组合成一个6，剩下另一个落单的2。将2拼在字符串的最前面，然后将6放在5的后面，得到的结果就是

mi \= '2' + five + '6' + seven + eight + nine

---

到了这里，就得到了构造函数generate。可以先对于t分解得到的cnt计算出对应的mi，这个是构造整数的下限。若mi的长度一开始就大于num的长度，那么mi就是大于num且满足条件的最小整数，此时直接返回mi即可。

若不满足，那么可以先构造一个较优解res，具体的构造方法为在mi的左侧补充若干的1，直到res的长度大于num的长度为止。

当然，目前的res不一定最优，因为除此之外，还有一种可能是通过修改num中的某些数位就可以使得num中数位之积可以被t整除。接下来考虑应该如何修改。

---

为了使得最终答案最小，因此修改的位置应该尽量靠后，尽量保持num的高位不变。于是在这里就应该从num的最后一个数位开始，从后往前尝试修改。不过在这里有一个特例，就是num的数位中不允许存在0，因此对于这种情况，应该从num中最左侧0的为师开始，从后往前尝试修改。

在这里就可以先从头开始对num进行一趟遍历，一边使用前缀中数位的质因子修正cnt数组，一边检测是否存在值为0的数位，若存在，则退出循环并从当前数位开始进行修改。这里说的修正cnt数组指的是在保持num高位不变的前提下，这些数位中的质因子可以抵消掉cnt中的某些需求。

不妨设从第start位开始向前修正，若此时尝试修改的是第p位之后的数位：

由于最开始的遍历使用num[p]修正了cnt，因此在这里需要先将num[p]对cnt之前做的修正去除掉，也就是将num[p]中的质因子还给cnt。

接下来应该从num[p] + 1开始到9进行遍历，找出修改后的数值v。

如果将num[p]修改位v，那么就应该先使用v再次修正cnt，接下来的问题就是能否在从p + 1位开始的这个后缀中构造出一个最小的整数，使得这个整数的各数位之积可以适配当前的cnt。可以发现，上面的构造函数generate在这里又可以发挥作用了。

对于当前的cnt，调用generate得到需要构造的最小整数mi，若mi的长度足够短可以填充到后缀中，即mi的长度小于等于len(num) - p - 1，那么将其填充到后缀中，此时就得到最终答案了。需要注意的是此时的mi可能长度不足len(num) - p - 1，可以在mi的左侧填充一些1。

若mi的长度太长而无法填充，则说明这种修改的方案不行，此时应该先将v中的质因子还给cnt，然后继续尝试下一个v。若num[p] + 1到9的所有的修改都行不通，那么p就需要向前移动，尝试修改第p - 1位之后的数位，直到找到答案或者p等于-1为止。

若一直找不到修改的方案，那么最终答案就是上面找到的较优解res。

最后附上python代码：

```python
class Solution(object):
    def smallestNumber(self, num, t):
        """
        :type num: str
        :type t: int
        :rtype: str
        """

        def update(v, cnt, delta):
            if v == 0:
                return v
            for index, x in enumerate([2, 3, 5, 7]):
                while v % x == 0:
                    cnt[index] += delta
                    v //= x
            return v

        cnt = [0] * 4
        t = update(t, cnt, 1)
        if t > 1:
            return "-1"

        def generate():
            if max(cnt) <= 0:
                return ''
            tmp = [max(0, x) for x in cnt]
            nine = ['9'] * (tmp[1] // 2)
            eight = ['8'] * (tmp[0] // 3)
            seven = ['7'] * tmp[3]
            five = ['5'] * tmp[2]

            mi = []

            if tmp[0] % 3 == 0:
                if tmp[1] % 2 == 0:
                    mi = five + seven + eight + nine
                else:
                    mi = ['3'] + five + seven + eight + nine
            elif tmp[0] % 3 == 1:
                if tmp[1] % 2 == 0:
                    mi = ['2'] + five + seven + eight + nine
                else:
                    mi = five + ['6'] + seven + eight + nine
            elif tmp[0] % 3 == 2:
                if tmp[1] % 2 == 0:
                    mi = ['4'] + five + seven + eight + nine
                else:
                    mi = ['2'] + five + ['6'] + seven + eight + nine
            
            return ''.join(mi)

        mi = generate()
        if len(mi) > len(num):
            return mi

        res = '1' * (len(num) - len(mi) + 1) + mi

        start = None
        for p, c in enumerate(num):
            if c == '0':
                start = p
                break
            update(int(c), cnt, -1)

        if start is None:
            if max(cnt) <= 0:
                return num
            start = len(num) - 1

        for p in range(start, -1, -1):
            update(int(num[p]), cnt, 1)

            for v in range(int(num[p]) + 1, 10):
                update(v, cnt, -1)
                
                mi = generate()
                if len(mi) <= len(num) - p - 1:
                    return num[:p] + str(v) + '1' * (len(num) - p - 1 - len(mi)) + mi
                
                update(v, cnt, 1)
        
        return res
```
