L1 = ['Shogun', 'Tea', 'Burger', 'KFC', 'Piatti']
L2 = ['Piatti', 'KFC', 'Burger', 'Shogun']


def _ptr2(S):
    return S['index'] if S['_line'] >= 11 and 'index' in S else None


def _txt(S):
    if S['_line'] >= 12 and 's' in S and 'index' in S and S['s'] in S['s_dict']:
        a, b = S['s_dict'][S['s']], S['index']
        return f"`{S['s']}`：list1 下标 {a} + list2 下标 {b} = =={a + b}==；当前最小和 = {S['index_sum']}"
    if S['_line'] >= 12 and 's' in S:
        return f"`{S['s']}` 不在 list1 中，不参与"
    return ''


CONFIG = dict(
    num=599, title='两个列表的最小索引和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表存下标 · 扫另一个列表',
    tags=[],
    code='''
class Solution(object):
    def findRestaurant(self, list1, list2):

        s_dict = {}
        for index, s in enumerate(list1):
            s_dict[s] = index
        
        res = []
        index_sum = None
        
        for index, s in enumerate(list2):
            if s in s_dict:
                if index_sum is None or index_sum > s_dict[s] + index:
                    index_sum = s_dict[s] + index
                    res = [s]
                elif index_sum == s_dict[s] + index:
                    res.append(s)
        
        return res
''',
    call=f'Solution().findRestaurant({L1!r}, {L2!r})',
    expect=['Shogun'],
    views=[
        dict(type='array', var='list1', label='list1', cell=120, h=140, index=True),
        dict(type='array', var='list2', label='list2（扫描它）', cell=120, h=230, pointers={'index': 'blue'}),
        dict(type='map', var='s_dict', label='s_dict（餐厅 → 在 list1 的下标）', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'cyan'), ('index_sum', 'index_sum', 'orange'), ('res', 'res', 'green')],
    captions={
        's_dict = {}': '`s_dict` 用来记住 list1 里每家餐厅的下标',
        'for index, s in enumerate(list1)': lambda S, B, r: ('list1 存完了' if S.index == B.get('index') and S.s == B.get('s') and len(S.s_dict) == len(S.list1)
                                                              else f'读 list1 的第 `{S.index}` 项 `{S.s!r}`'),
        's_dict[s] = index': '记下：`s_dict[{s!r}] = {index}`',
        'res = []': '`res` 存答案：当前所有最小索引和的餐厅',
        'index_sum = None': '`index_sum` 是目前最小的索引和，`None` 表示还没遇到公共餐厅',
        'for index, s in enumerate(list2)': lambda S, B, r: ('list2 扫完了' if B.get('index') == S.index and B.get('s') == S.s
                                                              else f'读 list2 的第 `{S.index}` 项 `{S.s!r}`'),
        'if s in s_dict': lambda S, B, r: (f'`{S.s!r}` 在 s_dict 里：两个列表都有 → 算索引和' if S.s in S.s_dict
                                           else f'`{S.s!r}` 不在 s_dict：只有 list2 有，跳过'),
        'if index_sum is None or': lambda S, B, r: (f'还没有最小值，先记下' if B.index_sum is None
                                                    else (f'`{B.index_sum} > {S.s_dict[S.s]} + {S.index}`：和更小 → ==换掉==旧答案' if B.index_sum > S.s_dict[S.s] + S.index
                                                          else f'`{B.index_sum} > {S.s_dict[S.s] + S.index}` 不成立：不是更小')),
        'index_sum = s_dict[s] + index': '最小索引和更新为 `{s_dict[s]} + {index} = {index_sum}`',
        'res = [s]': '旧答案作废，重新开始：`res = {res}`',
        'elif index_sum ==': lambda S, B, r: (f'`{S.index_sum} == {S.s_dict[S.s] + S.index}`：和相同 → 并列最小，也要加入' if S.index_sum == S.s_dict[S.s] + S.index
                                              else f'`{S.index_sum} ≠ {S.s_dict[S.s] + S.index}`：更大，不要'),
        'res.append(s)': '并列：`res` 追加 `{s!r}` → `{res}`',
        'return res': '索引和最小为 `{index_sum}`，返回 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='list1 的下标存进字典，扫 list2 时边查边比较',
        complexity='时间 `O(m+n)`，空间 `O(m)`',
        problem=['两个餐厅名列表，找==同时出现==在两个列表里、==下标和最小==的餐厅',
                 '下标和相同的都要返回，答案顺序不限',
                 '本视频：`list1 = [Shogun, Tea, Burger, KFC, Piatti]`，`list2 = [Piatti, KFC, Burger, Shogun]` → `[Shogun]`'],
        quote='使用哈希表储存其中一个索引中餐厅的位置，然后遍历另一个索引，求每个餐厅在两个索引中的和',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 list1 做成 `餐厅 → 下标` 的字典，查找是 `O(1)`',
              '扫描 list2：在字典里的就是公共餐厅，索引和 = 字典下标 + 当前下标',
              '`index_sum` 保存当前最小和：更小就==清空重来==，相等就==追加=='],
        summary=['时间 `O(m+n)`，空间 `O(m)`',
                 '易错：更小时要 `res = [s]` 重置，而不是 append',
                 '`index_sum` 初值用 `None`，所以第一个公共餐厅一定会被收下',
                 '原文说“找出最大的”应为笔误，代码求的是索引和==最小==',
                 '原文为 Python 2 风格，本题代码在 Python 3 下可直接运行，未改动'],
    ),
)
