def _bits(S):
    x = S.get('x')
    return bin(x)[2:][::-1] if x else '0'


def _ans_text(S):
    a = S.get('ans')
    if not a:
        return ''
    done = [v for v in a if v is not None]
    return '已得答案：' + ' , '.join(f'`{v}`' for v in done) if done else ''


def _s_text(S):
    s = S.get('s')
    if s is None:
        return ''
    cur = ''.join(s)
    return f'当前拼出的字符串 s = ==`{cur}`== （从左到右就是字典序最大的串）'


CONFIG = dict(
    num=4036, title='字符对转换后字典序最大的字符串', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='二进制拆分 · 像 2048 合成',
    tags=[],
    code='''
class Solution:
    def largestString(self, nums: list[int]) -> list[str]:
        ans = [None] * len(nums)
        for idx, x in enumerate(nums):
            # 单独处理 'z'
            s = ['z' * (x >> 25)]
            # 然后从 'y' 到 'a'
            for i in range(min(24, x.bit_length() - 1), -1, -1):
                if x >> i & 1:  # x 的 i 位是 1，所以有字母 i
                    s.append(ascii_lowercase[i])
            ans[idx] = ''.join(s)
        return ans
''',
    call='Solution().largestString([5, 6, 9])',
    expect=['ca', 'cb', 'da'],
    skip=['ans = [None]'],
    views=[
        dict(type='array', var='nums', pointers={'idx': 'blue'}, label='nums', h=170, cell=90,
             color=lambda S, k, v: 'blue' if k == S.get('idx') else None,
             dim=lambda S, k, v: S.get('idx') is not None and k < S['idx']),
        dict(type='string', var=_bits, label='x 二进制（低位在左，第 i 位 = 字母 i）', pointers={'i': 'pink'}, h=210, cell=80,
             color=lambda S, k, v: ('green' if v == '1' else None) if S.get('i') is not None else None),
        dict(type='text', fn=_s_text, size=26, h=60),
        dict(type='text', fn=_ans_text, size=26, h=60),
    ],
    watch=[('idx', 'idx', 'blue'), 'x', ('i', 'i', 'pink'), ('s', lambda S: ''.join(S['s']) if 's' in S else '', 'green')],
    captions={
        'for idx, x in enumerate': lambda S, B, r: ('nums 都处理完了，退出循环' if S.ans[S.idx] is not None else f'处理 `nums[{S.idx}] = {S.x}`：它是 {S.x} 个 `a`，二进制是 `{bin(S.x)[2:]}`'),
        "s = ['z'": '`x >> 25 = {x >> 25}`：每 `2^25` 个 a 合成一个 z，所以前面有 =={x >> 25}== 个 z（这里 x 太小，没有）',
        'for i in range(min': lambda S, B, r: (f'从最高位 `{S.i}` 倒着往 0 看：字母越大越要放前面' if 'i' not in B or B.get('x') != S.x or B.get('i') is None else (f'下一位：`i = {S.i}`' if S.i < B['i'] else '所有位都看完了，拼好这个 x 的答案')),
        'if x >> i & 1': lambda S, B, r: (f'`x` 的第 `{S.i}` 位 = `{S.x >> S.i & 1}`：'
                                            + (f'是 1 → 有 `2^{S.i}` 个 a 合成的字母 ==`{ascii_lowercase[S.i]}`==' if S.x >> S.i & 1 else '是 0 → 没有这个字母，跳过')),
        'ascii_lowercase[i]': '把字母 `{ascii_lowercase[i]}` 接在后面：`s` = `{"".join(s)}`',
        'ans[idx]': '`nums[{idx}]` 的答案 ==`{ans[idx]}`==',
        'return ans': '全部处理完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='把 x 个 a 当成 2048：二进制里的 1 就是答案里的字母',
        complexity='时间 `O(n·(U/2^26 + min(26, log U)))`，空间 `O(1)`',
        problem=['`x` 个 `a`，每次把相邻相同的两个字母合成下一个字母（`aa→b`，`zz` 不能合）',
                 '对每个 `x` 求能得到的字典序最大的字符串',
                 '示例：`[2,5,7]` → `["b","ca","cba"]`；本视频：`[5,6,9]` → `["ca","cb","da"]`'],
        quote='类似《2048》那种游戏，用两个 a 可以合成 b，用两个 b 可以合成 c，依此类推，用 2^k 个 a 可以合成小写字母 \'a\' + k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字典序最大：先让第一个字母尽量大 → 有 `2^25` 个 a 就先合出 z',
              '前面有 `floor(x / 2^25)` 个 `z`，剩下的从 `y` 到 `a` 倒着看',
              '此时每种字母至多一个：==`x` 二进制第 `k` 位是 1，就有第 `k` 个字母=='],
        summary=['时间 `O(n·(U/2^26 + min(26, log U)))`，空间 `O(1)`（返回值不计入）',
                 '`z` 要单独处理：`x >> 25` 可以大于 1，其余字母至多一个',
                 '枚举范围是 `min(24, x.bit_length() - 1)`：既不超过 `y`，也不越过最高位',
                 '倒着枚举（高位到低位），字母才是从大到小排列'],
    ),
)
