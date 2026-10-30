CONFIG = dict(
    num=3961, title='设备评分的最大和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序取最小次小 + 最小值集中到一台',
    tags=['灵神题单', '难度分 1880'],
    code='''
class Solution:
    def maxRatings(self, units: list[list[int]]) -> int:
        if len(units[0]) == 1:
            # 每个设备都只有一个单元
            return sum(unit[0] for unit in units)

        ans = 0
        mn = mn2 = inf
        for unit in units:
            unit.sort()  # 线性做法见【Python3 手动计算最小次小】
            ans += unit[1]  # 先加上次小
            mn2 = min(mn2, unit[1])
            mn = min(mn, unit[0])

        # 把包含 mn2 的那个设备作为集中站，存放每个设备的最小值
        ans += mn - mn2  # 把 ans 中的 mn2 替换成 mn
        return ans
''',
    call='Solution().maxRatings([[5,3,8],[2,6,4],[7,9,1]])',
    expect=13,
    views=[
        dict(type='grid', var='units', h=330, cell=110,
             color=lambda S, i, j, v: (('pink' if j == 0 else 'green' if j == 1 else None)
                                       if 'unit' in S and S['unit'] is S['units'][i] and S['_line'] >= 11 else None)),
        dict(type='text', size=34, fn=lambda S: (f"最小值 `mn = {S['mn']}`，次小值中的最小 `mn2 = {S['mn2']}`" if 'mn2' in S and S['mn2'] != float('inf') else '')),
    ],
    watch=[('ans', 'ans', 'green'), ('mn', 'mn', 'pink'), ('mn2', 'mn2', 'cyan')],
    captions={
        'len(units[0]) == 1': '只有 1 个单元时，移走它设备就空了（评分 0），所以不动',
        'return sum': '每台设备评分就是唯一的单元：直接求和',
        'ans = 0': '`ans` 累加每台设备移走最小值后的评分（次小值）',
        'mn = mn2 = inf': '`mn` 记全局最小值，`mn2` 记所有次小值里的最小',
        'for unit in units': lambda S, B, r: ('所有设备都处理完了' if B.get('unit') == S.unit else f'处理下一台设备 `{S.unit}`'),
        'unit.sort()': '排序后 `{unit}`：第 0 个是最小（要被移走），第 1 个是次小（新评分）',
        'ans += unit[1]': '移走最小后评分变成次小 `{unit[1]}`，`ans` = {ans}',
        'mn2 = min': '次小值里的最小：`mn2 = {mn2}`——集中站候选',
        'mn = min': '全局最小 `mn = {mn}`——集中站收到的评分',
        'ans += mn - mn2': '集中站评分从次小 `{mn2}` 掉到 `{mn}`：`ans += {mn} − {mn2}` → =={ans}==',
        'return ans': '最大评分和为 `{ans}`',
    },
    cards=dict(
        one_liner='每台设备扔掉最小值，全扔给次小值最小的那台',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`units[i]` 是设备的单元容量，设备评分 = 单元最小值',
                 '每台设备最多当一次源：移走一个单元放进别的设备',
                 '示例：`[[5,3,8],[2,6,4],[7,9,1]]` → `13`'],
        quote='所以最优做法是把最小值都集中到同一个设备中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只有移走最小单元，设备评分才会变大：评分变成==次小值==',
              '移出的最小值若分散存放，会拉低多台设备；==集中到一台==只拉低一台',
              '集中站评分从次小掉到全局最小 `mn`，选次小最小（`mn2`）的设备掉得最少'],
        summary=['时间 `O(mn)`（排序写法为 `O(m n log n)`），空间 `O(1)`',
                 '先特判 `n = 1`：不能移动，否则设备变空评分为 0',
                 '`ans` 里先加的是每台次小值，最后把 `mn2` 换成 `mn`',
                 '题解另给了手动计算最小次小的线性写法，本视频用排序写法'],
    ),
)
