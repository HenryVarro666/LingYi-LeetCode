REQ = ["java", "nodejs", "reactjs", "aws"]
PEOPLE = [["java"], ["nodejs", "reactjs"], ["reactjs", "aws"], ["java", "nodejs"]]


def _fgrid(S):
    f = S.get('f')
    if f is None:
        return [[]]
    return [list(f[0:8]), list(f[8:16])]


def _color(S, r, c, v):
    j, msk = S.get('j'), S.get('msk')
    k = r * 8 + c
    line = S.get('_line', 0)
    if j is None or msk is None or line < 14:
        return None
    if k == j:
        return 'yellow'
    if k == (j | msk):
        return 'green'
    return None


def _bits(x, w=4):
    return format(x, f'0{w}b')


def _info(S):
    j, msk, i = S.get('j'), S.get('msk'), S.get('i')
    if 'mask' not in S:
        return '技能 `java=0, nodejs=1, reactjs=2, aws=3` → 每个人压成二进制数'
    ms = '  '.join(f'人{k}=={_bits(m)}==' for k, m in enumerate(S['mask']))
    if j is None or msk is None or S.get('_line', 0) < 14:
        return ms
    return f'`{_bits(j)}` | 人{i}`{_bits(msk)}` = `{_bits(j | msk)}`'


def _cap_if(S, B, ret):
    j, msk, i = S.j, S.msk, S.i
    t = j | msk
    if S.f[j] + 1 < S.f[t]:
        return f'`f[{j}] + 1 = {S.f[j] + 1}` < `f[{t}] = {S.f[t]}`：加上人{i}，用更少的人凑出 `{_bits(t)}` → 更新'
    return f'`f[{j}] + 1 = {S.f[j] + 1}` 不比 `f[{t}] = {S.f[t]}` 小：加人{i}不划算，跳过'


CONFIG = dict(
    num=1125, title='最小的必要团队', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状压 DP（集合版 0-1 背包 · 刷表法）',
    tags=['灵神题单', '动态规划', '难度分 2251'],
    code='''
class Solution:
    def smallestSufficientTeam(self, req_skills: List[str], people: List[List[str]]) -> List[int]:
        sid = {s: i for i, s in enumerate(req_skills)}  # 字符串映射到下标
        n = len(people)
        mask = [0] * n
        for i, skills in enumerate(people):
            for s in skills:  # 把 skills 压缩成一个二进制数 mask[i]
                mask[i] |= 1 << sid[s]

        u = 1 << len(req_skills)
        ids = [0] * u  # ids[j] 表示 f[j] 对应的 people 下标集合
        f = [inf] * u  # f[j] 表示并集为 j 至少要选的 people 个数
        f[0] = 0
        for j in range(u - 1):  # f[u-1] 无需计算
            if f[j] == inf: continue  # 无法更新其它状态，直接跳过
            for i, msk in enumerate(mask):
                if f[j] + 1 < f[j | msk]:
                    f[j | msk] = f[j] + 1  # 刷表：用 f[j] 去更新其它状态
                    ids[j | msk] = ids[j] | (1 << i)

        res = ids[-1]
        return [i for i in range(n) if (res >> i) & 1]  # 所有在 res 中的下标
''',
    call=f'Solution().smallestSufficientTeam({REQ!r}, {PEOPLE!r})',
    expect=[2, 3],
    skip=['for s in skills', 'for j in range', 'for i, msk in enumerate', 'f[0] = 0', 'sid = {', 'n = len(people)', 'u = 1 <<', 'ids = [0]', 'for i, skills', 'ids[j | msk] = '],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='table', var=_fgrid, label='f[j]：凑出技能集合 j 至少要几个人（黄 = 当前 j，绿 = 被更新的 j|mask）', h=250, cell=100,
             rows=['j=0..7', 'j=8..15'], cols=[str(k) for k in range(8)], color=_color),
        dict(type='array', var='mask', label='mask[i]：第 i 个人的技能集合', h=150, cell=90, pointers={'i': 'blue'}),
        dict(type='array', var='ids', label='ids[j]：人员集合（位掩码）', h=170, cell=50,
             pointers={'j': 'yellow'}),
    ],
    watch=[('j', 'j', 'yellow'), ('i', 'i', 'blue'), ('msk', 'msk', 'cyan'), ('j | msk', 'j | msk', 'green')],
    max_steps=44,
    captions={
        'sid = ': '技能名映射到下标：`{sid}`',
        'mask[i] |= ': '人{i}掌握 `{s}`，把第 `{sid[s]}` 位置 1 → `mask[{i}] = {mask[i]}`',
        'f = [inf]': '`f[j]`：凑出技能集合 `j` 最少要几个人，先全设成无穷',
        'ids = [0]': '`ids[j]`：记录 `f[j]` 对应的具体人员集合（也是二进制数）',
        'if f[j] == inf': lambda S, B, r: (f'`f[{S.j}] = inf`：集合 {S.j} 凑不出来，不能用它去更新别人 → 跳过' if S.f[S.j] == inf
                                           else f'`f[{S.j}] = {S.f[S.j]}`：集合 {S.j} 已经能凑出，用它去更新别的状态（刷表）'),
        'if f[j] + 1 < f[j | msk]': _cap_if,
        'f[j | msk] = f[j] + 1': '`f[{j|msk}] = {f[j|msk]}`：`{j}` 加人{i}得到 `{j|msk}`；同时 `ids[{j|msk}]` = `ids[{j}] | (1<<{i})` = `{ids[j]|(1<<i):b}`',
        'res = ids[-1]': '全集 `{u-1}` 对应的人员集合 `ids[-1] = {ids[-1]:b}`（二进制）',
        'return [i for i': '取出二进制中为 1 的位：团队 = =={ret}==',
    },
    cards=dict(
        one_liner='把人看作物品、技能集合看作背包，状压后刷表求最小个数',
        complexity='时间 `O(T + n·2^m)`，空间 `O(S + n + 2^m)`',
        problem=['有 `req_skills` 个必需技能，每个备选人员掌握若干技能',
                 '选出==人数最少==的团队，使每项技能至少有一人掌握，返回人员编号',
                 '示例：4 项技能、4 个人 → 选 `[2, 3]`（人2 管 reactjs、aws，人3 管 java、nodejs）'],
        quote='把 people[i] 看成物品（集合），reqSkills 看成背包容量（目标集合），本题就是一个集合版本的 ==0-1 背包问题==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['集合用二进制表示：`1 << x` 是 `{x}`，`A | B` 是并集',
              '刷表法：从小到大遍历 `j`，用 `f[j]` 去更新 `f[j | msk]`',
              '`f[j]` 还是初始值就说明凑不出，直接跳过；另开 `ids` 记录具体方案'],
        summary=['时间 `O(T + n·2^m)`，空间 `O(S + n + 2^m)`',
                 '灵神先写记忆化搜索，再 1:1 翻译成递推，再空间优化，最后用刷表法跳过无效状态',
                 '用 `ids` 单独存人员集合，避免反复调用 `bit_count`',
                 '易错：`range(u - 1)` 不含全集；`f[j] == inf` 必须跳过，否则 `inf + 1` 会污染状态'],
    ),
)
