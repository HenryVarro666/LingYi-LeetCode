CONFIG = dict(
    num=481, title='神奇字符串', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='自生成构造 + 双指针',
    code='''
class Solution:
    def magicalString(self, n: int) -> int:
        s = [1, 2, 2]
        i = 2
        while len(s) < n:
            s += [s[-1] ^ 3] * s[i]  # 1^3=2, 2^3=1，这样就能在 1 和 2 之间转换
            i += 1
        return s[:n].count(1)
''',
    call='Solution().magicalString(10)',
    expect=5,
    views=[
        dict(type='array', var='s', pointers={'i': 'blue'}, label='s（i 指向的数 = 下一组要写几个）', h=260,
             color=lambda S, k, v: 'green' if k == len(S['s']) - 1 and S.get('_line') == 7 else None),
        dict(type='text', fn=lambda S: (f"下一组写 `{S['s'][S['i']]}` 个 `{S['s'][-1] ^ 3}`" if 'i' in S and S['i'] < len(S['s']) else ''), size=34, h=80),
        dict(type='text', fn=lambda S: f"当前长度 `len(s) = {len(S['s'])}`，目标 `n = {S['n']}`" if 's' in S else '', size=30, h=70),
    ],
    watch=[('n', 'n', 'orange'), ('i', 'i', 'blue'), ('len(s)', 'len(s)', 'cyan')],
    captions={
        's = [1, 2, 2]': '神奇字符串从 `122` 开始：它自己说“第 1 组 1 个、第 2 组 2 个”',
        'i = 2': '`i = 2`：`s[0]`、`s[1]` 已经用完，现在轮到 `s[2]`',
        'while len(s) < n': lambda S, B, r: (f'`len(s) = {len(S.s)} < n = {S.n}` → 还不够长，继续构造' if len(S.s) < S.n else f'`len(s) = {len(S.s)} >= n = {S.n}` → 构造完成'),
        's += [': '末尾 `{B.s[-1]}` ^ 3 = =={s[-1]}==；`s[i] = {s[i]}` → 追加 `{len(s) - len(B.s)}` 个 `{s[-1]}`，`s` 长到 {len(s)}',
        'i += 1': '这一组写好了，`i` 指向下一个“组长度” → `i = {i}`',
        'return s[:n].count(1)': '最后一轮可能多填一个，所以只数前 `n` 个：`s[:{n}]` 里有 `{ret}` 个 1',
    },
    cards=dict(
        one_liner='s 自己描述自己：用已有的数当后面每组的长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['神奇字符串只含 `1`、`2`，把连续相同字符的组长度连起来，恰好还是 `s`',
                 '`s = 1 22 11 2 1 22 ...`，各组长度 `1 2 2 1 1 2 ...` 就是 `s`',
                 '返回前 `n` 个字符中 `1` 的个数；本视频 `n = 10` → `5`'],
        quote='把 s 看成是由「1 组」和「2 组」交替组成的，重点在于每组内的数字是一个还是两个，这可以从 s 自身上知道。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i` 指向“当前组长度”，`s[-1] ^ 3` 把 1 变 2、2 变 1 得到下一组的数字',
              '`s += [x] * s[i]`：写 `s[i]` 个 x，然后 `i += 1`，直到长度 ≥ n',
              '构造出的 `s` 本身又是后面组长度的来源，一边读一边写'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`^ 3` 在 1 与 2 之间切换：`1^3=2`，`2^3=1`',
                 '最后一次可能填入两个数使 `len(s) = n+1`，所以要数 `s[:n]` 而不是整个 `s`',
                 '另一种写法：先构造长度 ≥ 1e5 的 `s` 并做前缀和 `acc`，每次查询 `O(1)`'],
    ),
)
