def _fcol(S, i, v):
    if 'need' in S:
        return 'green' if i == S['need'] and S['need'] <= S['ma'] else None
    if 'num' in S and 'res' not in S and S['_line'] in (12, 13):
        if i == S['num'] and S['_line'] == 13:
            return 'yellow'
        if i > S['num']:
            return 'cyan'
    return None


def _top(S):
    if 'need' in S:
        s, need = S['s'], S['need']
        return f"咒语 `s = {s}`：最弱可用药水 `need = {need}`" + (f"，答案 `f[{need}]`" if need <= S['ma'] else '，超过最大药水')
    if 'num' in S:
        return f"`f[i]` = potions 中 ==≥ i== 的个数：`f[i] = f[i + 1] + cnt[i]`"
    return '先统计每种药水强度出现几次'


CONFIG = dict(
    num=2300, title='咒语和药水的成功对数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='计数 + 递推（后缀和）',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1477'],
    code='''
class Solution(object):
    def successfulPairs(self, spells, potions, success):

        ma = max(potions)
        f = [0] * (ma + 1)

        cnt_dict = {}
        for p in potions:
            cnt_dict[p] = cnt_dict.get(p, 0) + 1

        f[ma] = cnt_dict.get(ma, 0)
        for num in range(ma - 1, -1, -1):
            f[num] = f[num + 1] + cnt_dict.get(num, 0)

        res = []
        for s in spells:
            need = success // s
            if success % s != 0:
                need += 1

            if need > ma:
                res.append(0)
            else:
                res.append(f[need])

        return res
''',
    call='Solution().successfulPairs([5,1,3], [1,2,2,4,5], 7)',
    expect=[4, 0, 2],
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='array', var='potions', label='potions', cell=90, h=160,
             color=lambda S, i, v: 'yellow' if 'p' in S and 'num' not in S and S['_line'] in (8, 9) and v == S['p'] else None),
        dict(type='map', var='cnt_dict', label='cnt_dict：强度 → 出现次数', h=150),
        dict(type='array', var='f', label='f[i] = potions 中 ≥ i 的个数', color=_fcol,
             pointers={'num if _line in (12, 13) else None': 'cyan', 'need': 'green'},
             pointer_labels={'num if _line in (12, 13) else None': 'num'}, cell=90, h=230),
        dict(type='array', var='res', label='res', cell=90, h=150),
    ],
    watch=['ma', 'success', ('s', 's', 'yellow'), ('need', 'need', 'green')],
    captions={
        'ma = max': '`ma = max(potions) = {ma}`',
        'f = [0]': '`f` 开 `ma + 1 = {ma + 1}` 个位置',
        'cnt_dict = {}': '`cnt_dict` 统计每种强度的出现次数',
        'for p in potions': lambda S, B, r: ('统计完毕' if B.get('p') == S.p and sum(S.cnt_dict.values()) == len(S.potions)
                                             else f'药水 `p = {S.p}`'),
        'cnt_dict[p] =': '`cnt_dict[{p}]` → {cnt_dict[p]}',
        'f[ma] =': '边界：`f[{ma}] = cnt[{ma}] = {f[ma]}`，≥ 最大值的只有它自己',
        'for num in range': lambda S, B, r: (f'从大到小递推：`num = {S.num}`' if B.get('num') != S.num else '递推完毕'),
        'f[num] = f[num + 1]': '`f[{num}] = f[{num + 1}] + cnt[{num}]` = `{f[num + 1]} + {cnt_dict.get(num, 0)}` = =={f[num]}==',
        'res = []': '开始回答每个咒语',
        'for s in spells': lambda S, B, r: ('全部咒语处理完毕' if 'need' in B and len(S.res) == len(S.spells) else f'咒语 `s = {S.s}`'),
        'need = success // s': '`need = {success} // {s} = {need}`：先下取整',
        'if success % s': lambda S, B, r: (f'`{S.success} % {S.s} = {S.success % S.s} ≠ 0`：除不尽 → 下取整的 need 不够，要 +1'
                                           if S.success % S.s else f'`{S.success} % {S.s} = 0`：正好整除，need 就够了'),
        'need += 1': '`need` → =={need}==：这就是 `ceil(success / s)`',
        'if need > ma': lambda S, B, r: (f'`need = {S.need} > ma = {S.ma}`：最强的药水也不够 → 不可能成功'
                                         if S.need > S.ma else f'`need = {S.need} ≤ ma = {S.ma}`：查 `f[{S.need}]`'),
        'res.append(0)': '答案 `0`',
        'res.append(f[need])': '`f[{need}]` = =={res[-1]}== 瓶药水强度 ≥ {need}',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='算出每个咒语需要的最弱药水 need，再用 f[need] 直接查个数',
        complexity='时间 `O(n + m + U)`，空间 `O(U)`，`U = max(potions)`',
        problem=['咒语强度 `spells[i]`，药水强度 `potions[j]`；相乘 `≥ success` 就是一对成功组合',
                 '返回每个咒语能和多少瓶药水成功组合',
                 '示例：`[5,1,3], [1,2,3,4,5], 7` → `[4,0,3]`',
                 '本视频：`[5,1,3], [1,2,2,4,5], 7` → `[4,0,2]`'],
        quote='令f[i]表示potions中大于等于i的数有多少个，那么对于f[i]就有==f[i] = f[i + 1] + cnt[i]==。这里的cnt[i]表示i在potions中出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['咒语 s 需要药水 `≥ need`，`need = success // s`，除不尽再 `+1`',
              '`f[i]` 从大到小递推：边界 `f[ma] = cnt[ma]`',
              '`need > ma` 答案为 0，否则答案就是 `f[need]`'],
        summary=['时间 `O(n + m + U)`，空间 `O(U)`',
                 '原文为 Python 2 写法，整数除法 `success / s` 已改为 `success // s`',
                 '`need` 可能远大于 `ma`，先判断再访问 `f[need]`',
                 '也可以把 potions 排序后对每个咒语二分，或用树状数组',
                 '对比灵神：思路相同；灵神用 `(success − 1) // x + 1` 一步上取整，并原地复用 cnt'],
    ),
)
