_N = 3


def _bits(S):
    i = S.get('i')
    return None if not isinstance(i, int) else [i >> t & 1 for t in range(_N)]


def _gcolor(S, r, c, v):
    i, j, k = S.get('i'), S.get('j'), S.get('k')
    if not isinstance(i, int):
        return None
    if r == j and c == k and v < 2:
        return 'red' if v != (i >> c & 1) else 'green'
    if i >> r & 1 and v < 2:
        return 'yellow'
    return None


def _any(S, B, ret):
    i, j, row = S['i'], S['j'], S['row']
    for k, st in enumerate(row):
        if st < 2 and st != i >> k & 1:
            return (f'好人 `{j}` 说玩家 `{k}` 是{"好人" if st else "坏人"}，但 `i` 里玩家 `{k}` 是{"好人" if i >> k & 1 else "坏人"}'
                    f' → ==矛盾==')
    return f'好人 `{j}` 的陈述 `{row}`（2 = 没说）逐条核对，全部和 `i` 相符 → 无矛盾'


CONFIG = dict(
    num=2151, title='基于陈述统计最多好人数', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='二进制枚举好人集合',
    tags=['灵神题单', '链表树与回溯', '难度分 1980'],
    code='''
class Solution:
    def maximumGood(self, statements: List[List[int]]) -> int:
        def check(i: int) -> int:
            cnt = 0  # i 中好人个数
            for j, row in enumerate(statements):  # 枚举 i 中的好人 j
                if i >> j & 1:
                    if any(st < 2 and st != i >> k & 1 for k, st in enumerate(row)):
                        return 0  # 好人 j 的某个陈述 st 与实际情况矛盾
                    cnt += 1
            return cnt

        return max(check(i) for i in range(1, 1 << len(statements)))
''',
    call='Solution().maximumGood([[2, 1, 2], [1, 2, 2], [2, 0, 2]])',
    expect=2,
    views=[
        dict(type='grid', var='statements', label='statements[j][k]（黄行 = 好人 j 的陈述；绿 = 与实际相符，红 = 矛盾）', h=200, cell=80, color=_gcolor,
             cursors=[('j', 'k', 'blue', '')]),
        dict(type='array', var=_bits, label='i 的二进制，下标 = 玩家（1 = 好人，0 = 坏人）', cell=80, h=130,
             pointers={'j': 'pink'}),
        dict(type='text', h=50, fn=lambda S: f"当前 `i` = =={S.get('i')}==，已数到好人 `cnt` = =={S.get('cnt', 0)}==" if isinstance(S.get('i'), int) else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cnt', 'cnt', 'green')],
    skip=['def check', 'for j, row in enumerate'],
    max_steps=90,
    captions={
        'cnt = 0': '枚举到 `i = {i}`（二进制 `{bin(i)[2:].zfill(3)[::-1]}` 从玩家 0 起）：好人集合，先让 `cnt = 0`',
        'if i >> j & 1': '玩家 `{j}` 在 `i` 中是 =={"好人" if i >> j & 1 else "坏人"}==' + '{"：要检查他的陈述" if i >> j & 1 else "：坏人想说啥都行，不用管"}',
        'if any(': _any,
        'return 0': '好人说了假话，这个 `i` ==不合法== → 返回 0',
        'cnt += 1': '好人 `{j}` 的陈述全部相符 → `cnt` = =={cnt}==',
        'return cnt': '这个 `i` 合法，好人共 =={ret}== 个',
        'return max(': lambda S, B, ret: ('所有 `i` 都检查完，合法情况里好人最多 =={}== 个'.format(ret) if ret is not None
                                          else '`i` 从 1 枚举到 `2^n - 1`，每个 `i` 都调一次 `check`，取最大值'),
    },
    cards=dict(
        one_liner='n ≤ 15，枚举谁是好人，只核对好人的陈述',
        complexity='时间 `O(n^2 · 2^n)`，空间 `O(1)`',
        problem=['好人只说真话，坏人可真可假；`statements[i][j]` = 0 认为坏人、1 认为好人、2 没说',
                 '求可能的好人最大数目',
                 '本视频：`[[2,1,2],[1,2,2],[2,0,2]]` → 2'],
        quote='用二进制数表示这 n 个人中谁好谁坏，其中 1 表示好人，0 表示坏人。这样就可以枚举 i∈[0,2^n-1] 中的所有数字，然后判断 i 中好人的陈述是否与实际情况矛盾',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i` 的第 j 位 = 1 表示玩家 j 是好人',
              '只看好人：他对 k 的陈述 `st` 若是 0/1，必须等于 `i` 的第 k 位',
              '有矛盾就这个 `i` 不合法；否则好人数 = `i` 的位 1 个数，取最大'],
        result='所有合法情况中，好人最多 2 个',
        summary=['时间 `O(n^2 · 2^n)`，空间 `O(1)`',
                 '坏人的话不用验证（可真可假），所以只检查好人',
                 '`st < 2` 才是有效陈述，2 表示没说',
                 '从 `i = 1` 开始枚举，全是坏人的情况好人数为 0，不影响答案',
                 '思考题：如果坏人一定说假话，就是 CF1594D'],
    ),
)
