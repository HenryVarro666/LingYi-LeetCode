CONFIG = dict(
    num=2231, title='按奇偶性交换后的最大数字', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='按奇偶分组 + 记位置排序', tags=[],
    code='''
class Solution(object):
    def largestInteger(self, num):

        digits = [[], []]
        pos = [[], []]

        l = 0
        while num:
            now = num % 10
            num //= 10
            digits[now % 2].append(now)
            pos[now % 2].append(l)
            l += 1
        
        digits[0].sort()
        digits[1].sort()

        res = [0] * l
        for index in range(len(digits[0])):
            res[pos[0][index]] = digits[0][index]
        for index in range(len(digits[1])):
            res[pos[1][index]] = digits[1][index]

        res.reverse()

        return int(''.join([str(x) for x in res]))
''',
    call='Solution().largestInteger(65875)',
    expect=87655,
    views=[
        dict(type='array', var=lambda S: S['digits'][0], label='digits[0]：偶数', h=110),
        dict(type='array', var=lambda S: S['pos'][0], label='pos[0]：偶数的位置（从个位数起）', h=110),
        dict(type='array', var=lambda S: S['digits'][1], label='digits[1]：奇数', h=110),
        dict(type='array', var=lambda S: S['pos'][1], label='pos[1]：奇数的位置（从个位数起）', h=110),
        dict(type='array', var='res', label='res（低位在前）', h=120),
    ],
    watch=['num', 'now', 'l', 'index'],
    captions={
        'digits = [[], []]': '`digits[0]` 存偶数，`digits[1]` 存奇数',
        'pos = [[], []]': '`pos` 对应记下每个数原来的位置',
        'l = 0': '`l` 是当前位下标，从个位开始',
        'while num': lambda S, B, r: f'`num = {S.num}`，还有数字没拆' if S.num else '`num` 变成 0，数字拆完了',
        'now = num % 10': '取最低位：`now = {now}`',
        'num //= 10': '去掉最低位，`num` = {num}',
        'digits[now % 2].append': '`{now}` 是{"奇" if now % 2 else "偶"}数 → 放进 `digits[{now % 2}]`',
        'pos[now % 2].append': '同时记下它在位置 `{l}`',
        'l += 1': '共拆出 `{l}` 位',
        'digits[0].sort': '偶数从小到大排好，等会儿填的时候大的要放高位',
        'digits[1].sort': '奇数从小到大排好',
        'res = [0] * l': '准备结果数组，长度 `{l}`',
        'for index in range(len(digits[0]))': '开始把偶数按顺序填回：`index = {index}`',
        'res[pos[0][index]]': '偶数 `{digits[0][index]}` 填到位置 `{pos[0][index]}`',
        'for index in range(len(digits[1]))': '再把奇数填回：`index = {index}`',
        'res[pos[1][index]]': '奇数 `{digits[1][index]}` 填到位置 `{pos[1][index]}`',
        'res.reverse': '位置是从个位数起的，反转后高位在前：`{res}`',
        'return int': '拼成整数 `{ret}`',
    },
    cards=dict(
        one_liner='位置不变、数字重排：同奇偶里，大的放高位',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['奇偶性相同的两位数字可任意交换，求最大值',
                 '本视频：`65875` → `87655`'],
        quote='为了使得结果最大，那么就应该让较大的数字放在高位上，于是可以先将每一位数字按奇偶性分到两个数组中，同时使用两个数组分别记录下奇数数字和偶数数字的原始位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`% 10` 从低位拆数，同时记下每个数的位置 `pos`',
              '两组数字各自升序；位置也是从个位数起升序，所以最大的数会配到最高位',
              '按位置填回，反转后就是答案'],
        summary=['原文为 Python 2 写法，整数除法 `num /= 10` 已改为 `num //= 10`',
                 '时间 `O(n log n)`，空间 `O(n)`',
                 '易错：位置是从个位数起记的，最后必须 `reverse`',
                 '位置升序 + 数字升序 = 最大的数落在最高位'],
    ),
)
