def _top(S):
    if 'res' not in S:
        return '精力：初始必须 > 所有 energy 之和；经验：边打边补'
    return f"精力一次补齐后 `res = {S['res']}`" + (f"；经验当前 `now = {S['now']}`" if 'now' in S else '')


CONFIG = dict(
    num=2383, title='赢得比赛需要的最少训练时长', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='精力求和 + 经验一趟补',
    tags=[],
    code='''
class Solution(object):
    def minNumberOfHours(self, initialEnergy, initialExperience, energy, experience):

        res = sum(energy) + 1 - initialEnergy
        if res < 0:
            res = 0

        now = initialExperience
        for exp in experience:
            if now <= exp:
                res += exp + 1 - now
                now = exp + 1
            
            now += exp
        
        return res
''',
    call='Solution().minNumberOfHours(5, 3, [1, 4, 3, 2], [2, 6, 3, 1])',
    expect=8,
    views=[
        dict(type='text', fn=_top, size=28, h=70),
        dict(type='array', var='energy', label='energy：只减不增，总和 + 1 就是初始精力下限', cell=96, h=190),
        dict(type='array', var='experience', label='experience：边打边涨，缺了就补（蓝 = 当前对手）', cell=96, h=190,
             color=lambda S, i, v: 'blue' if 'exp' in S and 'now' in S and v == S['exp'] and
             all(S['experience'][j] != v for j in range(i)) else None),
        dict(type='text', size=26, h=80,
             fn=lambda S: (f"经验 `now = {S['now']}`，对手经验 `{S['exp']}`" if 'now' in S and 'exp' in S else '')),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'pink'), 'exp'],
    captions={
        'res = sum(energy)': '精力只减不增：初始至少要 `sum(energy) + 1 = {sum(energy) + 1}`，还差 `{sum(energy) + 1} - {initialEnergy}` = =={res}==',
        'if res < 0': lambda S, B, ret: (f'`res = {S.res} < 0`：初始精力已经富余，不用补' if S.res < 0
                                         else f'`res = {S.res} >= 0`：精力要补这么多'),
        'res = 0': '富余就不用补，`res` 归零',
        'now = initialExperience': '经验从 `{now}` 开始，一趟遍历',
        'for exp in experience': lambda S, B, ret: ('所有对手遍历完了' if 'exp' in B and S.exp == B.exp and S.now == B.now
                                                    else f'下一个对手经验 `{S.exp}`，当前经验 `now = {S.now}`'),
        'if now <= exp': lambda S, B, ret: (f'`now = {S.now} <= {S.exp}`：经验不严格超过 → ==不够，要补=='
                                            if S.now <= S.exp else f'`now = {S.now} > {S.exp}`：经验够了'),
        'res += exp + 1 - now': '要补 `{exp} + 1 - {B.now}` = {exp + 1 - B.now} 小时 → `res = {res}`',
        'now = exp + 1': '经验补到 `{exp} + 1 = {now}`，刚好超过',
        'now += exp': '打赢后获得经验 `{exp}` → `now = {now}`',
        'return res': '精力和经验的补充量加起来：==`{res}`== 小时',
    },
    cards=dict(
        one_liner='精力和经验分开算：精力看总和，经验一趟补',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['精力、经验都要==严格超过==对手才能赢；赢后精力减、经验加',
                 '开赛前每训练 1 小时，精力或经验 +1，求最少小时数',
                 '示例：`5, 3, [1,4,3,2], [2,6,3,1]` → `8`'],
        quote='对于精力值而言，由于精力值只会不断减少，因此必须保证初始的精力值足够大。为了使得最终有精力剩余，因此初始精力至少要是energy之和加1。',
        quote_src='—— yiduobo 题解',
        idea=['精力只减不增：初始精力 `> sum(energy)`，缺的就是 `sum(energy) + 1 - 初始`',
              '经验会在途中增加，顺序固定，所以==一趟遍历==，不足时补到刚好超过',
              '两种数值互不影响，分开考虑再相加'],
        result='精力补 6、经验补 2，共 8 小时 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：精力缺口为负要归零（`if res < 0`）',
                 '经验补完要先 `now = exp + 1` 再 `now += exp`',
                 '原文变量名 `exp` 是对手经验，不要和初始经验混淆'],
    ),
)
