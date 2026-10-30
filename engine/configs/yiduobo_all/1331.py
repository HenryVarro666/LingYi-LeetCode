CONFIG = dict(
    num=1331, title='数组序号转换', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序后依次编号 · 映射',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def arrayRankTransform(self, arr):

        pos_dict = {}
        now = None
        cnt = 0
        for num in sorted(arr):
            if num != now:
                cnt += 1
                pos_dict[num] = cnt
                now = num
        
        return [pos_dict[num] for num in arr]
''',
    call='Solution().arrayRankTransform([37,12,28,9,100,56,80,5,12])',
    expect=[5, 3, 4, 2, 8, 6, 7, 1, 3],
    views=[
        dict(type='array', var='arr', label='arr（原数组）', h=150, color=lambda S, i, v: 'yellow' if v == S.get('num') else None),
        dict(type='array', var=lambda S: sorted(S['arr']), label='sorted(arr)（当前数字高亮，新数字才编号）', h=170,
             color=lambda S, i, v: 'yellow' if v == S.get('num') else None),
        dict(type='map', var='pos_dict', label='pos_dict（数字 → 序号）', fmt=lambda k, v: f'{k}: {v}', h=230, font=28),
    ],
    watch=['num', 'now', ('cnt', 'cnt', 'green')],
    captions={
        'pos_dict = {}': '`pos_dict` 记录「数字 → 序号」',
        'now = None': '`now` 记录上一个编号的数字，用来判断是不是新数字',
        'cnt = 0': '`cnt` 是当前已发出的最大序号',
        'for num in sorted': '从小到大取下一个数 `num = {num}`',
        'if num != now': lambda S, B, r: (f'`{S.num} != {S.now}`：==第一次出现==的数字，要发新序号' if S.num != S.now
                                           else f'`{S.num} == {S.now}`：和上一个相同，重复数字不再编号'),
        'cnt += 1': '序号加一：`cnt` → =={cnt}==',
        'pos_dict[num] = cnt': '`pos_dict[{num}] = {cnt}`',
        'now = num': '记下 `now = {now}`，下一个相同的数就会被跳过',
        'return [': '再按原数组顺序查表，得到 `{ret}`',
    },
    cards=dict(
        one_liner='先排序，遇到新数字才发新序号，再映射回去',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把数组每个元素换成排序后的序号，序号从 1 开始',
                 '==相等的元素序号相同==，序号尽可能小',
                 '示例：`[37,12,28,9,100,56,80,5,12]` → `[5,3,4,2,8,6,7,1,3]`'],
        quote='将原数组从小到大进行排序，然后依次对第一次出现的数字进行编号，并建立数字到编号的映射，然后通过映射将原数组转化为序号数组返回即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后相同的数字挨在一起，用 `now` 记住上一个数字',
              '`num != now` 说明碰到新数字，`cnt += 1` 发新序号',
              '最后按原数组顺序查 `pos_dict`，不用二分'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`now` 初值为 `None`，保证第一个数字一定被编号',
                 '只有新数字才让 `cnt` 加一，所以序号连续且最小',
                 '和灵神的区别：灵神用 `set` 先去重再编号，yiduobo 在排序后的数组上边扫边去重'],
    ),
)
