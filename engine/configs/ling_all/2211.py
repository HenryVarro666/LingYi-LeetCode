CONFIG = dict(
    num=2211, title='统计道路上的碰撞次数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='去掉首尾 · 数移动的车',
    tags=['灵神题单', '难度分 1581'],
    code='''
class Solution:
    def countCollisions(self, s: str) -> int:
        s = s.lstrip('L')  # 前缀向左的车不会发生碰撞
        s = s.rstrip('R')  # 后缀向右的车不会发生碰撞
        return len(s) - s.count('S')  # 剩下非静止的车计入碰撞次数
''',
    call='Solution().countCollisions("LLRSRLRR")',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（黄 = 静止的车）', cell=84,
             color=lambda S, i, v: 'yellow' if v == 'S' else ('blue' if v == 'R' else 'pink')),
        dict(type='text', size=28, fn=lambda S: (f"剩余车辆 `{len(S['s'])}` 辆，其中静止 `{S['s'].count('S')}` 辆，移动 `{len(S['s']) - S['s'].count('S')}` 辆"
                                                  if 's' in S else '')),
    ],
    watch=[('len(s)', 'len(s)', 'blue'), ('s.count("S")', "s.count('S')", 'yellow')],
    captions={
        'lstrip': '开头向左的车，左边没有车挡路 → 去掉，剩 `{s}`',
        'rstrip': '结尾向右的车，右边没有车挡路 → 去掉，剩 `{s}`',
        'return': '剩下的车都会碰撞；一次碰撞只算在==移动的车==上 → `{len(s)} - {s.count("S")}` = =={ret}==',
    },
    cards=dict(
        one_liner='首尾向外开的车不会撞，剩下每辆移动的车贡献一次碰撞',
        complexity='时间 `O(n)`，空间 `O(n)` 或 `O(1)`',
        problem=['公路上有 `n` 辆车，方向为 `L` 向左、`R` 向右、`S` 静止',
                 '相向相撞 +2，移动车撞静止车 +1，撞后停下；求碰撞总次数',
                 '本视频：`"LLRSRLRR"` → `3`'],
        quote='所以碰撞次数等于移动的车辆数，即剩余车辆数减去静止的车辆数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['去掉前缀的 `L` 和后缀的 `R` 后，剩下的车必然会碰撞',
              '约定：碰撞次数==算在移动的车上==，相向相撞的两辆各算 1，共 2，静止的被撞不算',
              '所以答案 = 剩余车辆数 − 静止车辆数'],
        after=[dict(heading='逐个看本例的碰撞', lines=['`"LLRSRLRR"`：开头两个 `L` 向左开走，结尾两个 `R` 向右开走', '剩下 `RSRL`：第 1 辆 R 撞静止的 S → 1', 'S 被撞后仍静止；末尾 R 与 L 相向相撞 → 2，共 `1 + 2 = 3`'])],
        summary=['时间 `O(n)`，空间 `O(n)`（切片会新建字符串）',
                 '先去前缀 `L`，再去后缀 `R`；两者互不影响',
                 '易错：`lstrip` 去的是==所有==连续的 `L`，不是只去一个'],
    ),
)
