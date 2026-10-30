CONFIG = dict(
    num=2231, title='按奇偶性交换后的最大数字', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='奇偶分组排序 + 回填原位置',
    tags=[],
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
        dict(type='text', fn=lambda S: f"还剩 `num = {S['num']}`" if 'num' in S else '', h=60),
        dict(type='array', var=lambda S: S['digits'][0], label='digits[0]（偶数）', h=170) if False else dict(type='text', fn=lambda S: f"偶数 `digits[0] = {S['digits'][0]}`，位置 `pos[0] = {S['pos'][0]}`" if 'digits' in S else '', h=60),
        dict(type='text', fn=lambda S: f"奇数 `digits[1] = {S['digits'][1]}`，位置 `pos[1] = {S['pos'][1]}`" if 'digits' in S else '', h=60),
        dict(type='array', var='res', h=240, label='res（低位在左，下标 = 位权）',
             color=lambda S, i, v: 'green' if S.get('_line') and v != 0 else None) if False else dict(type='array', var=lambda S: S.get('res', []), h=240, label='res（下标 0 = 个位）'),
    ],
    watch=['l', ('now', 'now', 'blue'), ('digits', 'digits', 'green'), ('pos', 'pos', 'purple')],
    captions={
        'now = num % 10': '取最低位 `now = {now}`，它是{"奇" if now % 2 else "偶"}数',
        'num //= 10': '去掉最低位，`num` → {num}',
        'digits[now % 2].append': '`{now}` 放进{"奇" if now % 2 else "偶"}数组 → `{digits[now % 2]}`',
        'pos[now % 2].append': '同时记下它的位置 `{l}`（0 = 个位）→ `{pos[now % 2]}`',
        'digits[0].sort': '偶数从小到大排好：`{digits[0]}`',
        'digits[1].sort': '奇数从小到大排好：`{digits[1]}`',
        'res = [0] * l': '准备 `{l}` 位的结果，下标 0 是个位',
        'res[pos[0][index]]': '位置越靠后越是高位，且数组升序 → ==最大的偶数落在最高的偶数位==：`res[{pos[0][index]}] = {digits[0][index]}`',
        'res[pos[1][index]]': '同理奇数：`res[{pos[1][index]}] = {digits[1][index]}`',
        'res.reverse': '翻转成高位在前：`{res}`',
        'return int': '拼成数字 =={ret}==',
    },
    cards=dict(
        one_liner='同奇偶的位置随便换，大数放高位',
        complexity='时间 `O(n log n)`，空间 `O(n)`（n 为位数）',
        problem=['正整数 `num`，可以任意次交换奇偶性相同的两位数字',
                 '返回能得到的最大值',
                 '示例：`1234` → `3412`；`65875` → `87655`'],
        quote='为了使得结果最大，那么就应该让较大的数字放在高位上，于是可以先将每一位数字按奇偶性分到两个数组中，同时使用两个数组分别记录下奇数数字和偶数数字的原始位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇偶互不能换：奇数占的位置和偶数占的位置是固定的',
              '位置记录从个位开始，下标越大位权越高',
              '两组各自升序排序，按位置从低到高回填，大数自然落在高位'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：位置从个位数起算，回填后要 `reverse` 再拼接',
                 '原文为 Python 2 写法，整数除法 `num /= 10` 已改为 `num //= 10`'],
    ),
)
