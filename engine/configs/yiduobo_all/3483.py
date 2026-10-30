CONFIG = dict(
    num=3483, title='不同三位偶数的数目', difficulty='Easy', category='链表、二叉树与回溯',
    author='yiduobo', technique='枚举 100~998 的偶数 + Counter 比较',
    tags=['灵神核心路线', '灵神题单·数学算法', '难度分 2094'],
    code='''
class Solution(object):
    def totalNumbers(self, digits):
        
        cnt = Counter(digits)
        res = 0
        for target in range(100, 1000, 2):
            first = target // 100
            second = target // 10 % 10
            third = target % 10
            need = Counter([first, second, third])
            flag = True
            for v in need:
                if need[v] > cnt[v]:
                    flag = False
                    break
            
            if flag:
                res += 1

        return res
''',
    call='Solution().totalNumbers([1, 0, 2])',
    expect=3,
    views=[
        dict(type='map', var='cnt', label='cnt：digits 里每个数字的个数', h=140, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='need', label='need：当前 target 需要的数字个数', h=140, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=lambda S: (f"正在检查 `{S['target']}`：" + ('==够用==' if S.get('flag') else '==不够==') if 'need' in S and S['_line'] >= 15 else (f"正在检查 `{S['target']}`" if 'target' in S else '')), size=32),
    ],
    watch=[('target', 'target', 'blue'), ('v', 'v', 'pink'), ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    skip=['cnt = Counter', 'res = 0'],
    max_steps=66,
    captions={
        'for target in range': '枚举三位偶数：`target = {target}`',
        'first = target': '分离百位：`{target} // 100 = {first}`',
        'second = target': '分离十位：`{target} // 10 % 10 = {second}`',
        'third = target': '分离个位：`{target} % 10 = {third}`',
        'need = Counter': '`target` 需要的数字：`need` = {need}',
        'flag = True': '先假设能凑出：`flag = True`',
        'for v in need': '检查需要的每种数字 `v = {v}`',
        'if need[v] > cnt[v]': lambda S, B, ret: (
            f'数字 `{S.v}` 需要 `{S.need[S.v]}` 个，库存只有 `{S.cnt[S.v]}` 个 → ==不够==' if S.need[S.v] > S.cnt[S.v]
            else f'数字 `{S.v}` 需要 `{S.need[S.v]}` 个，库存 `{S.cnt[S.v]}` 个 → 够'),
        'flag = False': '有一种数字不够 → `flag = False`',
        'break': '已经凑不出了，不用再看别的数字',
        'if flag': lambda S, B, ret: (f'`flag` 为真 → `{S.target}` 能凑出，计数' if S.flag else f'`flag` 为假 → `{S.target}` 凑不出'),
        'res += 1': '`res` → {res}',
        'return res': '检查完所有三位偶数，能凑出 `{res}` 个',
    },
    cards=dict(
        one_liner='三位偶数就 450 个，逐个拆出数位，和库存比一比',
        complexity='时间 `O(n + 450)`，空间 `O(1)`',
        problem=['`digits` 里选三个数字，每个只能用一次',
                 '组成不含前导零的==三位偶数==，求能组成多少个不同的数',
                 '本视频：`[1,0,2]` → `3`（102、120、210）'],
        quote='可以从100开始到998，以步长为2进行一趟遍历，检测所有的三位偶数能否被构造出来。对于当前遍历到的target，将target中的三个数位都分离出来，然后对比digits中对应的数位是否足够。',
        quote_src='—— yiduobo 题解原文',
        idea=['`range(100, 1000, 2)`：从 100 开始、只取偶数，就不会有前导零',
              '把 `target` 的三位放进 `need`，和库存 `cnt` 逐种比较',
              '不同的 `target` 本来就互不相同，所以直接计数，==不用去重=='],
        result='能凑出 3 个：102、120、210 ✓',
        summary=['时间 `O(n + 450)`，空间 `O(1)`',
                 '`Counter` 取不存在的键返回 0，所以 `cnt[v]` 不会报错',
                 '库存比较是「个数」而不是「有没有」：222 需要 3 个 2',
                 '步数很多，视频中间一段会快进',
                 '对比灵神：灵神是枚举个位再用乘法原理，`O(n)`；这里是暴力枚举'],
    ),
)
