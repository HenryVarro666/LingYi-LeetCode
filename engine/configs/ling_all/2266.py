_F, _G = [1, 1, 2, 4], [1, 1, 2, 4]
for _ in range(5):
    _F.append(_F[-1] + _F[-2] + _F[-3])
    _G.append(_G[-1] + _G[-2] + _G[-3] + _G[-4])

CONFIG = dict(
    num=2266, title='统计打字方案数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='分组 + 爬楼梯 + 乘法原理',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1857'],
    setup='from itertools import groupby',
    code='''
MOD = 1_000_000_007
f = [1, 1, 2, 4]
g = [1, 1, 2, 4]
for _ in range(10 ** 5 - 3):  # 预处理所有长度的结果
    f.append((f[-1] + f[-2] + f[-3]) % MOD)
    g.append((g[-1] + g[-2] + g[-3] + g[-4]) % MOD)

class Solution:
    def countTexts(self, pressedKeys: str) -> int:
        ans = 1
        for ch, s in groupby(pressedKeys):
            m = len(list(s))
            ans = ans * (g[m] if ch in "79" else f[m]) % MOD
        return ans
''',
    call='Solution().countTexts("2227777")',
    expect=32,
    views=[
        dict(type='string', var='pressedKeys', h=190, label='pressedKeys',
             color=lambda S, i, v: ('blue' if S.get('ch') == v else None)),
        dict(type='array', var=_F, label='f：长为 i 的 2/3/4/5/6/8 键方案数（i = 下标）', h=190,
             color=lambda S, i, v: 'green' if S.get('m') == i and S.get('ch') not in (None, '7', '9') else None),
        dict(type='array', var=_G, label='g：长为 i 的 7/9 键方案数（i = 下标）', h=190,
             color=lambda S, i, v: 'green' if S.get('m') == i and S.get('ch') in ('7', '9') else None),
        dict(type='text', size=30, fn=lambda S: (f"当前组：字符 `{S['ch']}` 连续 `{S['m']}` 次" if 'm' in S else '')),
    ],
    watch=['ch', 'm', ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '各组互相独立，按==乘法原理==把各组方案数相乘，先令 `ans = 1`',
        'for ch, s in groupby': '`groupby` 把连续相同的按键分成一组：这一组是 `{ch}`',
        'm = len': '这一组连续按了 `{m}` 次 `{ch}`',
        'ans = ans *': lambda S, B, r: (f"`{S.ch}` 是 7/9 键，末尾可拆 1~4 个字符 → 查 `g[{S.m}] = {_G[S.m]}`" if S.ch in '79' else f"`{S.ch}` 只有 3 个字母，末尾拆 1~3 个字符 → 查 `f[{S.m}] = {_F[S.m]}`") + f"；`ans = {B.ans} × {_G[S.m] if S.ch in '79' else _F[S.m]} = {S.ans}`",
        'return ans': '所有组相乘完毕，答案 `{ans}`',
    },
    cards=dict(
        one_liner='连续相同按键拆成 1~3（或 4）段：就是爬楼梯',
        complexity='时间 `O(n)`，空间 `O(1)`（忽略预处理）',
        problem=['按键串 `pressedKeys` 是 Alice 每个字母按若干次得到的，问她可能发出多少种文字',
                 '按 `i` 次某键得到该键第 `i` 个字母；`7`、`9` 键有 4 个字母',
                 '本视频：`"2227777"` → `32`；答案对 `10^9+7` 取余'],
        quote='把这 $10$ 个字符拆分成若干段，每段的长度可以是 $1,2,3$ ……这本质上是 ==70. 爬楼梯==，每次可以跳 $1,2,3$ 个台阶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['连续 `m` 个相同数字，拆成若干段，每段对应一个字母',
              '`f[i] = f[i-1]+f[i-2]+f[i-3]`；7、9 键再加 `f[i-4]`，记作 `g`',
              '不同组互不影响 → ==乘法原理== 把各组结果相乘'],
        after=[dict(heading='预处理的 f 和 g', lines=['`f = [1, 1, 2, 4, 7, 13, ...]`：每次跳 1/2/3 个台阶', '`g = [1, 1, 2, 4, 8, 15, ...]`：每次跳 1/2/3/4 个台阶', '先把所有长度的结果算好，每组直接查表'])],
        summary=['时间 `O(n)`；预处理 `f, g` 只做一次',
                 '易错点：==7 和 9 要用 g==，其余用 f；每次乘法后都要取模',
                 '预处理只做一次，演示里不逐步追踪，只展示表的前几项',
                 '`groupby` 来自 `itertools`，演示里在 setup 中导入',
                 '同类题：70. 爬楼梯、91. 解码方法'],
    ),
)
