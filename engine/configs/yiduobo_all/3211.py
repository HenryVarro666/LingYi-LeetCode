CONFIG = dict(
    num=3211, title='生成不含相邻零的二进制字符串', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='动态规划 · 以 1 / 0 结尾分别存串',
    tags=['灵神核心路线', '灵神题单·位运算', '难度分 1353'],
    code='''
class Solution(object):
    def validStrings(self, n):

        f = ["1"]
        g = ["0"]

        for index in range(1, n):
            new_f = [s + "1" for s in f] + [s + "1" for s in g]
            new_g = [s + "0" for s in f]
            f, g = new_f, new_g
        
        return f + g
''',
    call='Solution().validStrings(5)',
    expect=['11111', '01111', '10111', '11011', '01011', '11101', '01101', '10101', '11110', '01110', '10110', '11010', '01010'],
    views=[
        dict(type='text', fn=lambda S: (f"现在 `f`、`g` 里的字符串长度都是 =={len(S['f'][0])}==" if 'f' in S else ''), size=28, h=60),
        dict(type='stack', var='f', label='f：以 1 结尾的有效串', h=200),
        dict(type='stack', var='g', label='g：以 0 结尾的有效串', h=170),
        dict(type='stack', var=lambda S: S.get('new_f'), label='new_f（长度 +1，以 1 结尾）', h=200),
        dict(type='stack', var=lambda S: S.get('new_g'), label='new_g（长度 +1，以 0 结尾）', h=170),
    ],
    watch=[('n', 'n', 'blue'), ('index', 'index', 'pink'), ('len(f)', 'len(f)', 'cyan'), ('len(g)', 'len(g)', 'orange')],
    skip=[],
    captions={
        'f = ["1"]': '长度为 1：以 `1` 结尾的只有 `"1"` → `f`',
        'g = ["0"]': '以 `0` 结尾的只有 `"0"` → `g`',
        'for index in range(1, n)': lambda S, B, ret: (f'要从长度 `{S.index}` 推到长度 `{S.index + 1}`' if 'index' in S and S.get('index') != B.get('index') or 'index' not in B
                                                        else '长度已经到 `n`，结束循环'),
        'new_f = ': '以 `1` 结尾：前面是 `f` 或 `g` 都行，各接一个 `"1"` → `{len(new_f)}` 个',
        'new_g = ': '以 `0` 结尾：前一个必须是 `1`，所以只能接在 `f` 后面 → `{len(new_g)}` 个（`g` 后面再接 0 就是 `00`）',
        'f, g = new_f, new_g': '滚动更新：只需要上一轮，现在长度是 `{index + 1}`',
        'return f + g': '最后把以 1 结尾和以 0 结尾的拼起来：共 `{len(ret)}` 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='按最后一位分两组：1 结尾随便接，0 结尾只能接在 1 后面',
        complexity='时间 `O(n·φ^n)`，空间 `O(φ^n)`（`φ ≈ 1.618`）',
        problem=['返回所有长为 `n` 的二进制字符串，要求不含相邻的 `0`（顺序任意）',
                 '示例：`n = 3` → `["010","011","101","110","111"]`',
                 '本视频：`n = 5`，一共 `13` 个'],
        quote='令f[i]和g[i]分别表示长度为i且最后一个字符分别为1和0时的所有合法字符串。……而对于g[i]，则只能在f[i - 1]的基础上填充一个0，因为g[i - 1]已经是以0结尾了。',
        quote_src='—— yiduobo 题解原文',
        idea=['计数题常见的 DP：`f[i]`、`g[i]` 记以 1、0 结尾的方案数；这题把“数量”换成“具体字符串”',
              '`f[i] = f[i-1] + "1"` 加上 `g[i-1] + "1"`；`g[i] = f[i-1] + "0"`',
              '每一轮只和上一轮有关，用滚动变量省掉 `i` 这一维'],
        summary=['时间 `O(n·φ^n)`：`φ^n` 个字符串，每个长 `n`；空间同阶',
                 '`g` 只能从 `f` 转移，否则会出现 `00`',
                 '初始是长度 1：`f = ["1"]`，`g = ["0"]`，循环从 1 到 `n-1`',
                 '对比灵神：灵神用位运算 `x & (x>>1)` 枚举取反数；yiduobo 用 DP 直接构造，不枚举非法串',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行'],
    ),
)
