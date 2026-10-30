def _txt(S):
    if 'cnt' not in S:
        return '右移 `a` 位 = 左移 `n − a` 位：全部换成左移再累加'
    if 'd' in S and S['_line'] in (8, 9, 10, 11):
        return f"当前操作 `[{S['d']}, {S['a']}]`，累计左移 `cnt` = =={S['cnt']}=="
    return f"累计左移 `cnt` = =={S['cnt']}=="


CONFIG = dict(
    num=1427, title='字符串的左右移', difficulty='Easy', category='字符串',
    author='yiduobo', technique='方向统一 · 累加后取模',
    tags=[],
    code='''
class Solution(object):
    def stringShift(self, s, shift):

        n = len(s)
        cnt = 0
        for d, a in shift:
            if d == 0:
                cnt += a
            else:
                cnt += n - a
        
        cnt %= n
        return s[cnt:] + s[:cnt]
''',
    call='Solution().stringShift("abcdefg", [[1, 1], [1, 1], [0, 2], [1, 3]])',
    expect='efgabcd',
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 左移 cnt 位后的新开头）', cell=100, h=190,
             pointers={'cnt % n': 'blue'}),
        dict(type='text', h=100, size=30, fn=_txt),
        dict(type='array', var='shift', label='shift：[方向, 位数]（0 = 左移，1 = 右移）', cell=130, h=140,
             fmt=lambda v: str(v)),
    ],
    watch=['n', 'd', 'a', ('cnt', 'cnt', 'blue')],
    captions={
        'n = len(s)': '`n = {n}`：左移 `n` 位等于没动，所以最后对 `n` 取模',
        'cnt = 0': '`cnt` 累计「向左移动的总位数」',
        'for d, a in shift': '取一次操作：方向 `d = {d}`，位数 `a = {a}`',
        'if d == 0': lambda S, B, r: ('`d == 0`：本来就是左移 → 成立' if S.d == 0 else '`d == 1`：是右移 → 不成立'),
        'cnt += a': '左移 `{a}` 位：`cnt` → =={cnt}==',
        'cnt += n - a': '右移 `{a}` 位 = 左移 `n − a = {n - a}` 位：`cnt` → =={cnt}==',
        'cnt %= n': '左移 `n` 位回到原样：`cnt` 对 `{n}` 取模 → =={cnt}==',
        'return s[cnt:]': '`s[{cnt}:] + s[:{cnt}]`：前 `{cnt}` 个字符挪到末尾 → `{ret}`',
    },
    cards=dict(
        one_liner='右移 i 位就是左移 n − i 位，全部换成左移再累加取模',
        complexity='时间 `O(n + m)`，空间 `O(n)`（m 为操作数）',
        problem=['字符串 `s` 和操作 `shift[i] = [direction, amount]`',
                 '`direction = 0` 左移，`1` 右移，每次移动 `amount` 位（循环移位）',
                 '示例：`"abc", [[0,1],[1,2]]` → `"cab"`',
                 '本视频：`"abcdefg"` 四次操作 → `"efgabcd"`'],
        quote='题目中向右移动i位实际上可以认为是向左移动了n - i位，因此可以将所有的移动操作都视为向左移动，然后将移动的位数累加起来，这个累加和对n取模就得到了最终向左移动的位数。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用真的一步步移动字符串，只关心总位移',
              '右移 `a` 位 ≡ 左移 `n − a` 位，把方向统一',
              '累加后取模，最后只切一次：`s[cnt:] + s[:cnt]`'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '`cnt %= n` 一定要做，否则切片位置可能超过长度',
                 '左右抵消会自然体现在累加和里，不用逐个模拟',
                 '题面为根据文章和 LeetCode 原题补写（本库未收录题面）',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
