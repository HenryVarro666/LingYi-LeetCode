D = ["acd", "bed", "accd"]

CONFIG = dict(
    num='LCP 66', title='最小展台数量', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表记每种展台单天最大需求',
    code='''
class Solution(object):
    def minNumBooths(self, demand):

        max_cnt = {}
        for d in demand:
            char_cnt = {}
            for char in d:
                char_cnt[char] = char_cnt.get(char, 0) + 1
            
            for char in char_cnt:
                if char_cnt[char] > max_cnt.get(char, 0):
                    max_cnt[char] = char_cnt[char]
        
        return sum(max_cnt.values())
''',
    call=f'Solution().minNumBooths({D!r})',
    expect=6,
    views=[
        dict(type='array', var='demand', label='demand（每天的需求，蓝 = 当前这天）', cell=100, h=190,
             color=lambda S, i, v: 'blue' if S.get('d') == v else None),
        dict(type='map', var='char_cnt', label='char_cnt（当天各展台数量）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=30),
        dict(type='map', var='max_cnt', label='max_cnt（各展台历史单天最大数量）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=30),
    ],
    watch=[('d', 'd', 'blue'), ('char', 'char', 'pink'), ('总数', 'sum(max_cnt.values())', 'green')],
    captions={
        'max_cnt = {}': '`max_cnt`：每种展台==单天最多==需要几个',
        'for d in demand': lambda S, B, r: ('每一天都看完了' if 'd' in B and B.d == S.d else f'看一天的需求 `{S.d!r}`'),
        'for char in d': lambda S, B, r: ('这一天的字符数完了' if sum(S.char_cnt.values()) == len(S.d) else f'取当天的下一个展台 `{S.char!r}`'),
        'char_cnt = {}': '这一天单独统计，`char_cnt` 清空',
        'char_cnt[char] =': '`{char!r}` 在当天出现 → `char_cnt[{char!r}] = {char_cnt[char]}`',
        'for char in char_cnt': lambda S, B, r: ('当天用到的展台都比较完了' if B.char == S.char and len(S.char_cnt) > 1 else f'检查当天用到的展台 `{S.char!r}`'),
        'if char_cnt[char] >': lambda S, B, r: (f'当天需要 `{S.char_cnt[S.char]}` 个，历史最大 `{S.max_cnt.get(S.char, 0)}` → ' + ('更多，要更新' if S.char_cnt[S.char] > S.max_cnt.get(S.char, 0) else '不比历史多，不用管')),
        'max_cnt[char] =': '`{char!r}` 的最大需求更新为 `{max_cnt[char]}`',
        'return sum': '每种展台单天最大需求加起来：`{max_cnt}` → =={ret}==',
    },
    cards=dict(
        one_liner='每种展台取单天最大需求，累加就是答案',
        complexity='时间 `O(L)`，空间 `O(|Σ|)`',
        problem=['`demand[i]` 是第 i 天要用的展台类型',
                 '同一展台不同天可以复用，求最少准备数量',
                 '示例：`["acd","bed","accd"]` → `6`'],
        quote='由于不同天之间，展台可以重复利用，那么只需一趟遍历，找出每种展台在同一天中最多需要几个，然后将每种展台单天最多需要的数量累加起来即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一天内展台不能共用，天与天之间可以',
              '所以每种展台要备的数量 = ==它在某一天的最大需求==',
              '一趟遍历：当天先数一遍，再去更新全局最大'],
        summary=['时间 `O(L)`，空间 `O(|Σ|)`',
                 '`char_cnt` 每天重新建，不能跨天累计',
                 '用 `max_cnt.get(char, 0)` 处理第一次出现的展台',
                 '原文为 Python 2 风格，无需改动即可运行'],
    ),
)
