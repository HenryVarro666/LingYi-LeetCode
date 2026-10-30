_cnt = {}


def _once(key):
    _cnt[key] = _cnt.get(key, 0) + 1
    return _cnt[key] == 1


def _arr(S):
    return S['prices'] if 'prices' in S else S.get('nums')


def _color(S, i, v):
    if 'prices' in S:
        if 'p' in S and v == S['p']:
            return 'pink'                                   # 今天（卖出日）
        if 'min_price' in S and v == S['min_price']:
            return 'green'                                  # 之前的最低价（买入日）
        return None
    if 'cur_end' in S:
        if i <= S['cur_end']:
            return 'cyan'                                   # 已造的桥能覆盖的位置
        if i <= S.get('next_end', -1):
            return 'yellow'                                 # 再造一座桥能到的位置
    return None


def _formula(S):
    if 'prices' in S and 'p' in S:
        return (f"今天卖 `p = {S['p']}`，买在之前最低价 `{S['min_price']}`"
                f" → 利润 `{S['p'] - S['min_price']}`，最好 `ans = {S['ans']}`")
    if 'prices' in S:
        return '模板①：==枚举卖出日==，买入日一定选之前的最低价'
    if 'cur_end' in S and 'next_end' in S:
        return (f"青色 = 已造桥能到 `[0, {S['cur_end']}]`，黄色 = 再造一座桥最远到 `{S['next_end']}`，"
                f"`ans = {S['ans']}`")
    return '模板②「造桥」：无路可走时，回头选能跳得最远的点建桥'


CONFIG = dict(
    num=None, title='贪心算法 · 通用思想与模板', author='概念讲解', category='贪心算法',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def max_profit(prices):              # 121. 枚举卖出日
    ans, min_price = 0, prices[0]
    for p in prices:
        ans = max(ans, p - min_price)  # 今天卖，买在之前最低点
        min_price = min(min_price, p)
    return ans

def jump(nums):                      # 45. 跳跃游戏 II（造桥）
    ans = 0
    cur_end = 0                      # 已建造的桥的右端点
    next_end = 0                     # 下一座桥的右端点的最大值
    for i in range(len(nums) - 1):
        next_end = max(next_end, i + nums[i])  # 默默收集信息
        if i == cur_end:             # 无路可走，必须建桥
            cur_end = next_end       # 选最远的点建桥
            ans += 1
    return ans
''',
    call='''
a = max_profit([7, 1, 5, 3, 6, 4])
b = jump([2, 3, 1, 1, 4])
(a, b)
''',
    expect=(5, 2),
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='bars', var=_arr, label='prices / nums', pointers={'i': 'pink'}, color=_color, h=330),
        dict(type='text', fn=lambda S: ('粉 = 今天（卖出日），绿 = 之前的最低价（买入日）' if 'prices' in S else
                                        ('柱高 = `nums[i]` = 从 i 最多能跳几格' if 'nums' in S else '')),
             size=26, h=60),
    ],
    watch=[('p', 'p', 'pink'), ('min_price', 'min_price', 'green'), ('ans', 'ans', 'yellow'), ('i', 'i', 'pink'),
           ('cur_end', 'cur_end', 'cyan'), ('next_end', 'next_end')],
    captions={
        'ans, min_price = 0': '模板①：`min_price` 记录 ==卖出日之前的最低价==，`ans` 是最大利润',
        'for p in prices': lambda S, B, ret: (f'假设今天以 `{S.p}` 卖出' if B.get('p') != S.p else '每一天都试过了'),
        'ans = max(ans, p - min_price)': lambda S, B, ret: (
            (f'今天卖赚 `{S.p} - {S.min_price} = {S.p - S.min_price}`：换成别的买入日 ==不会赚得更多==，`ans = {S.ans}`'
             if _once('profit') else f'今天卖赚 `{S.p} - {S.min_price} = {S.p - S.min_price}`，`ans = {S.ans}`')
            if S.p - S.min_price > 0 else f'今天卖赚 `{S.p - S.min_price}`，不如不卖，`ans = {S.ans}`'),
        'min_price = min': lambda S, B, ret: (f'今天的价格 `{S.p}` 更低 → 更新最低价 `min_price = {S.min_price}`'
                                              if S.min_price != B.min_price else f'最低价仍是 `{S.min_price}`'),
        'ans = 0': '模板②「造桥」：`ans` 是造了几座桥（跳了几次）',
        'cur_end = 0': '`cur_end`：已建造的桥最远能到哪；一开始站在 0',
        'next_end = 0': '`next_end`：在当前桥上走的时候，记下 ==再造一座桥最远能到哪==',
        'for i in range': lambda S, B, ret: (f'走到位置 `i = {S.i}`' if B.get('i') != S.i else '走到了终点前一格，结束'),
        'next_end = max': '默默收集信息：从 `{i}` 最远能跳到 `{i + nums[i]}`，`next_end = {next_end}`',
        'if i == cur_end': lambda S, B, ret: (f'`i = {S.i}` 到达桥的尽头 → ==无路可走，必须建桥=='
                                              if S.i == S.cur_end else f'`i = {S.i}` 还在桥上，继续走'),
        'cur_end = next_end': lambda S, B, ret: (
            f'在能跳最远的位置 `{max(range(S.i + 1), key=lambda j: j + S.nums[j])}` 起跳建桥：右端点 → `{S.cur_end}`'),
        'ans += 1': '桥的数量 `ans = {ans}`',
        'return ans': lambda S, B, ret: (f'最少跳 `{ret}` 次' if 'nums' in S else f'最大利润 `{ret}`'),
    },
    cards=dict(
        one_liner='每一步做当下最好的选择，并能证明这样做不会让答案变差',
        complexity='通常一次遍历：时间 `O(n)`，空间 `O(1)`',
        problem_heading='什么时候用？',
        problem=['每一步都有一个「显然最好」的选择，选了不会后悔',
                 '能用 ==交换论证==：最优解里的选择换成贪心选择，不变差',
                 '跳跃、区间覆盖、划分 → 维护「最远能到哪」',
                 '买卖一次股票 → 枚举卖出日，维护之前的最低价'],
        before=[dict(heading='核心概念：交换论证', lines=[
            '任取一个最优解，把它的某个选择换成贪心选择，答案 ==不会变差==',
            '能跳到 `i < j` 且 `i + nums[i] ≥ j + nums[j]` → 跳 `i` 不亏',
            '固定卖出日，买在之前最低价——换成其他买入日利润不会更高',
            '想不出证明时先写暴力 / DP：贪心常常是对它们的优化']),
        ],
        idea_heading='两位作者怎么说',
        quote='不妨设这次起跳可以跳到位置 i 与位置 j，其中 i < j，且 i + nums[i] ≥ j + nums[j]，那么这一步应该跳到 i，因为==从 j 起跳能到的位置从 i 起跳都能到==，反之则不一定。',
        quote_src='—— yiduobo · 45. 跳跃游戏 II',
        idea=['灵神 45「造桥」：==在无路可走之前，我们只是在默默地收集信息==',
              '灵神还说 45 的贪心本质是对暴力（BFS 按步数分层）的优化，是个递推',
              '121 两人一致：枚举卖出日，==先用 p - min 更新答案，再更新 min=='],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`121` 买卖股票的最佳时机：枚举卖出日，维护最低买入价',
                 '`55` 跳跃游戏：维护最右可达位置 `mx`，`i > mx` 就到不了',
                 '`45` 跳跃游戏 II：造桥，无路可走时选最远的点',
                 '`763` 划分字母区间：每个字母的最后位置 → 合并区间',
                 '易错：121 先算利润再更新最低价；45 只遍历到 `n-2`'],
    ),
)
