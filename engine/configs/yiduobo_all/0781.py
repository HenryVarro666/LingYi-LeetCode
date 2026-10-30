ANS = [2, 2, 2, 1, 1, 2, 0]


def _txt(S):
    if 'cnt' in S and 'num' in S:
        n, c = S['num'], S['cnt']
        return f"回答 `{n}` 的有 `{c}` 只，每 `{n + 1}` 只一组：`{c} // {n + 1}` 组整，" + (
            f"余 `{c % (n + 1)}` 只还要再开一组" if c % (n + 1) else '正好分完')
    if 'count_dict' in S and 'res' not in S:
        return '先统计每个回答出现了几次'
    return ''


CONFIG = dict(
    num=781, title='森林中的兔子', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='计数 · 每 k+1 只分一组向上取整',
    tags=['灵神题单', '贪心与思维', '难度分 1453'],
    code='''
class Solution(object):
    def numRabbits(self, answers):

        count_dict = {}
        for num in answers:
            count_dict[num] = count_dict.get(num, 0) + 1
        
        res = 0
        for num, cnt in count_dict.items():
            res += cnt // (num + 1) * (num + 1)
            if cnt % (num + 1) != 0:
                res += num + 1
        return res
''',
    call=f'Solution().numRabbits({ANS})',
    expect=9,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='answers', color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None, h=200),
        dict(type='map', var='count_dict', fmt=lambda k, v: f'回答 {k}：{v} 只', h=300),
    ],
    watch=['num', 'cnt', ('res', 'res', 'green')],
    captions={
        'count_dict = {}': '`count_dict`：回答 `k` 的兔子有几只',
        'for num in answers': lambda S, B, r: ('全部回答统计完毕' if sum(S.count_dict.values()) == len(S.answers) and 'cnt' not in S
                                                else f'下一只兔子回答 `{S.answers[sum(S.count_dict.values())]}`'),
        'count_dict[num] =': '回答 `{num}` 的兔子又多一只：`count_dict[{num}] = {count_dict[num]}`',
        'res = 0': '`res` 累计兔子总数，从 0 开始',
        'for num, cnt in': lambda S, B, r: ('每种回答都处理完了，退出循环' if 'cnt' in B and B.num == S.num and S.num == list(S.count_dict)[-1]
                                             else f'处理回答 `{S.num}` 的 `{S.cnt}` 只兔子，每 `{S.num + 1}` 只同色为一组'),
        'res += cnt': '整组的部分：`{cnt} // {num + 1} = {cnt // (num + 1)}` 组，每组 `{num + 1}` 只 → `res` = {res}',
        'if cnt %': lambda S, B, r: (
            f'`{S.cnt} % {S.num + 1} = {S.cnt % (S.num + 1)}` ≠ 0：还剩几只凑不满 → ==再开一组=='
            if S.cnt % (S.num + 1) != 0 else f'`{S.cnt} % {S.num + 1} = 0`：正好分完，不用再加'),
        'res += num + 1': '多开的一组也有 `{num} + 1 = {num + 1}` 只（含没被问到的）→ `res` = {res}',
        'return res': '森林里最少 `{res}` 只兔子',
    },
    cards=dict(
        one_liner='回答 k 的兔子每 k+1 只一组，组数向上取整',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每只被问到的兔子说出「还有几只和我同色」',
                 '给出所有回答 `answers`，求森林中兔子最少有多少只',
                 '示例：`[1,1,2]` → `5`；本视频用 `[2,2,2,1,1,2,0]` → `9`'],
        quote='我们必须尽可能让每只兔子描述的都是出现在answer中的兔子，因此我们可以按每k + 1只兔子进行分组，组内的兔子颜色一致。',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计：回答 `k` 的兔子有 `p` 只',
              '每 `k+1` 只一组，至少需要 `t = ceil(p / (k+1))` 组',
              '每组 `k+1` 只，答案累加 `t * (k+1)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '向上取整被拆成「整除 + 有余数再加一组」两步',
                 '对比灵神：灵神一行公式 `(c+x)//(x+1)*(x+1)`，yiduobo 显式判断余数'],
    ),
)
