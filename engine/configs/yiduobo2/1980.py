NUMS = ["000", "010", "001"]


def _ncolor(S, i, v):
    ln = S.get('_line')
    num = S['_inner'].get('num')
    if ln is not None and ln <= 9 and num == v:
        return 'yellow'
    if 'num_set' in S and int(v, 2) in S['num_set'] and (ln > 9 or num != v):
        return 'cyan'
    return None


def _info(S):
    ln = S.get('_line')
    if ln is not None and ln <= 9 and 'num' in S['_inner']:
        return f"把二进制串 `\"{S['num']}\"` 转成整数：`now = now × 2 + 当前位` → `now = {S['now']}`"
    if ln in (11, 12, 13):
        return f"从 0 往上枚举：`now = {S['now']}` " + ('==在==集合里，继续 +1' if S['now'] in S['num_set'] else '==不在==集合里 → 就是答案')
    if ln in (15, 17, 18):
        return f"把答案转回 `{len(S['nums'])}` 位二进制：每次取 `now % 2` 得到最低位，再 `now //= 2`"
    if ln in (20, 21):
        return f"低位先进 `res` → 翻转后就是高位在前：`\"{''.join(S['res'])}\"`"
    return 'n 很小：把串转成数放进集合，再从 0 开始找第一个没出现的数'


CONFIG = dict(
    num=1980, title='找出不同的二进制字符串', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='集合 + 从 0 向上暴力枚举',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def findDifferentBinaryString(self, nums):
        num_set = set()
        for num in nums:
            now = 0
            for char in num:
                now = now * 2 + int(char)

            num_set.add(now)

        now = 0
        while now in num_set:
            now += 1

        res = []
        for _ in range(len(nums)):
            res.append(str(now % 2))
            now //= 2

        res.reverse()
        return ''.join(res)
''',
    call=f'Solution().findDifferentBinaryString({NUMS!r})',
    expect='011',
    skip=['for num in nums:', 'for char in num:', 'for _ in range(len(nums))'],
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='nums', label='nums（黄 = 正在转换，青 = 已进集合）', cell=120, h=150, color=_ncolor),
        dict(type='set', var='num_set', label='num_set（出现过的整数）', fmt=lambda x: f'{x} = {x:03b}', h=120),
        dict(type='array', var='list(range(8))', label='候选答案 0 … 2^n−1（灰 = 在集合里，绿 = 找到的答案）', cell=78, h=175,
             pointers={'now if 11 <= _line <= 13 else None': 'yellow'},
             pointer_labels={'now if 11 <= _line <= 13 else None': 'now'},
             color=lambda S, i, v: ('green' if S.get('_line', 0) >= 11 and 'num_set' in S and i not in S['num_set']
                                    and i == min(x for x in range(8) if x not in S['num_set']) else None),
             dim=lambda S, i, v: 'num_set' in S and i in S['num_set']),
        dict(type='array', var='res', label='res（逐位取出的二进制位）', cell=78, h=140),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'yellow'), ('char', lambda S: S['_inner'].get('char') if S['_line'] <= 9 else None, 'cyan')],
    captions={
        'num_set = set()': '`n = {len(nums)}` 很小 → 直接==暴力==：先把每个串变成整数放进集合',
        5: '开始转换 `"{num}"`：`now` 从 0 起步，从高位往低位读',
        'now = now * 2 + int(char)': '读到 `{char}`：`now = {B.now} × 2 + {char}` = =={now}==',
        'num_set.add(now)': '`"{num}"` = `{now}`，加入集合 → `{sorted(num_set)}`',
        11: '再从 `now = 0` 开始向上枚举',
        'while now in num_set': lambda S, B, r: (f'`{S.now}` 出现过 → 不能用，继续' if S.now in S.num_set
                                                 else f'`{S.now}` ==没有出现==在集合里 → 找到了！'),
        'now += 1': '换下一个：`now = {now}`',
        'res = []': '把 `{now}` 转回长度为 `{len(nums)}` 的二进制串（必须补前导 0）',
        'res.append(str(now % 2))': '最低位 `{B.now} % 2 = {res[-1]}` → `res = {res}`',
        'now //= 2': '`now = {B.now} // 2 = {now}`，去掉最低位（原文 `/=`，已改为 `//=`）',
        'res.reverse()': '`res` 里是从低位到高位 → 翻转：`{res}`',
        "return ''.join(res)": '返回 =={ret}==：它不在 `nums` 里',
    },
    cards=dict(
        one_liner='n 很小：串转整数放进集合，从 0 向上找第一个没出现的数',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`nums` 有 `n` 个==互不相同==的二进制串，每个长度都是 `n`',
                 '返回一个长度为 `n` 且==没有出现==在 `nums` 中的二进制串（任意一个即可）',
                 '示例：`nums = ["00","01"]` → `"11"`（`"10"` 也对）',
                 '本视频：`nums = ["000","010","001"]`'],
        quote='注意到题目中n的规模很小，因此我在这里直接使用的暴力算法。==将nums中的每个数加入到集合中，然后从0开始向上枚举，找出一个没有出现在集合中的数==，再将其转化成二进制串返回即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐位 `now = now × 2 + 当前位`，把每个串变成整数放进 `num_set`',
              '`n` 个数最多挡住 `0..n-1` → 最多枚举 `n + 1` 次就能找到',
              '再用 `% 2`、`// 2` 逐位取出，补够 `n` 位后翻转'],
        result='`0、1、2` 都出现过，`3` 没有 → `3` 补成 3 位 = `"011"`',
        summary=['时间 `O(n^2)`（转换 `n` 个长为 `n` 的串），空间 `O(n)`',
                 '易错：答案要补前导 0；这里固定循环 `len(nums)` 次取位，自然补齐',
                 '对比灵神的康托对角线：`ans[i] = nums[i][i]` 取反，`O(n)` 且不用集合',
                 '原文为 Python 2 写法：`now /= 2` 已改为 `now //= 2`，并删去了文档字符串'],
    ),
)
