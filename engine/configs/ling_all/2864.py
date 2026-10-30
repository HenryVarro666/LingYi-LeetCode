CONFIG = dict(
    num=2864, title='最大二进制奇数', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='贪心构造',
    tags=[],
    code='''
class Solution:
    def maximumOddBinaryNumber(self, s: str) -> str:
        cnt1 = s.count('1')
        return '1' * (cnt1 - 1) + '0' * (len(s) - cnt1) + '1'
''',
    call="Solution().maximumOddBinaryNumber('0101101')",
    expect='1110001',
    views=[
        dict(type='text', fn=lambda S: ('数出 `1` 的个数：==%d== 个，`0` 有 ==%d== 个' % (S['cnt1'], len(S['s']) - S['cnt1'])) if 'cnt1' in S else '先数一数有几个 `1`', size=28),
        dict(type='string', var='s', label='s（绿 = 1，其余 = 0）', cell=84,
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='text', fn=lambda S: ('结果 = `%s` + `%s` + `1`' % ('1' * (S['cnt1'] - 1), '0' * (len(S['s']) - S['cnt1']))) if 'cnt1' in S else '', size=28),
    ],
    watch=[('cnt1', 'cnt1', 'green'), ('len(s)', 'len(s)')],
    captions={
        'cnt1 = s.count': '`s` 里一共有 =={cnt1}== 个 `1`，其余 `{len(s) - cnt1}` 个是 `0`',
        'return': '奇数末位必须是 `1` → 留 1 个放最后；其余 `{cnt1 - 1}` 个 `1` 全放最高位，中间补 `{len(s) - cnt1}` 个 `0` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='末尾放一个 1，其余的 1 全堆在开头',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给二进制串 `s`（至少有一个 `1`），重新排列各位', '求能得到的==最大的奇数==，可以有前导零',
                 '示例：`"0101"` → `"1001"`'],
        quote='由于奇数的二进制末尾一定是 1，我们可以把一个 1 放在末尾，其余的 1 全部放在开头，这样构造出的奇数尽量大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数 ⇔ 二进制末位是 `1`，先预留一个 `1`', '二进制越靠左权重越大 → 剩下的 `1` 都挤到最高位', '中间补 `0`，末位补那个 `1`'],
        before=[dict(heading='先看一个小例子', lines=['`s = "0101101"`：共 7 位，4 个 `1`、3 个 `0`', '末位固定放 `1`，还剩 3 个 `1`', '`111` ＋ `000` ＋ `1` → `1110001`'])],
        after=[dict(heading='为什么这样最大', lines=['末位被迫是 `1`，其余位置里 `1` 越靠左越大', '把 `1` 往左挪一位，数值至少翻倍', '所以答案唯一：先全部 1，再全部 0，再一个 1'])],
        summary=['时间 `O(n)`（`count` 一遍），空间 `O(1)`，返回值不计入',
                 '易错：留给末位的 `1` 要从 `cnt1` 里减掉，写成 `cnt1 - 1`',
                 '0 的个数是 `len(s) - cnt1`，题目保证 `cnt1 ≥ 1`'],
    ),
)
