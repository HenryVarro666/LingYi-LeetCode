CONFIG = dict(
    num=1338, title='数组大小减半', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='字典计数 · 次数降序累加',
    tags=['灵神题单', '难度分 1303'],
    code='''
class Solution(object):
    def minSetSize(self, arr):

        cnt_dict = {}
        for num in arr:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        now = 0
        for index, cnt in enumerate(sorted(cnt_dict.values(), reverse=True)):
            now += cnt
            if now + now >= len(arr):
                return index + 1
''',
    call='Solution().minSetSize([3,3,3,3,5,5,5,2,2,7])',
    expect=2,
    views=[
        dict(type='array', var='arr', label='arr', cell=70, h=150),
        dict(type='map', var='cnt_dict', label='cnt_dict（数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
        dict(type='array', var=lambda S: sorted(S['cnt_dict'].values(), reverse=True), label='次数从大到小（绿 = 已选）', cell=100, h=250,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if 'index' in S and 'now' in S and i <= S['index'] else None),
             dim=lambda S, i, v: 'index' not in S or i > S['index']),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"已删 `now = {S['now']}`，总数 `len(arr) = {len(S['arr'])}`；`2 × now = {2 * S['now']}`" if 'now' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'yellow'), ('now', 'now', 'green')],
    captions={
        'cnt_dict = {}': '用字典统计每个数出现几次',
        'for num in arr': lambda S, B, r: ('每个数都统计完了：`cnt_dict` 里是各数的出现次数' if sum(S.cnt_dict.values()) == len(S.arr) else f'看到 `{S.num}`'),
        'cnt_dict[num] =': '`cnt_dict[{num}]` = `{cnt_dict[num]}`',
        'now = 0': '`now` 记已经删掉的元素个数',
        'for index, cnt in enumerate': '次数从大到小取：第 `{index + 1}` 大的次数是 `{cnt}`，选这个数',
        'now += cnt': '删掉这个数的全部 `{cnt}` 个 → `now = {now}`',
        'if now + now >= len(arr)': lambda S, B, r: (f'`{S.now} + {S.now} = {2 * S.now}` ≥ `{len(S.arr)}`：删去的数已超过一半' if S.now + S.now >= len(S.arr)
                                                    else f'`{S.now} + {S.now} = {2 * S.now}` < `{len(S.arr)}`：还不到一半，继续选'),
        'return index + 1': '选了 `index + 1` = =={ret}== 个数',
    },
    cards=dict(
        one_liner='只要求超过一半，所以先删出现次数最多的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选一些数，把它们在数组里==全部出现==都删掉',
                 '至少删掉数组的一半，求最少选几个数',
                 '本视频：`[3,3,3,3,5,5,5,2,2,7]` → `2`'],
        quote='题目只需要删除超过一半的数，并没有要求恰好删去一半的数，因此我们应该先从出现次数较多的数开始进行删去。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用字典数出每个数的出现次数',
              '次数从大到小排序，一趟扫描累加',
              '`now + now >= len(arr)` 就是“前缀和 ≥ 总数一半”，用加法避免除法'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '用 `now + now >= len(arr)` 比较，不涉及除法',
                 '易错：返回 `index + 1`，因为下标从 0 开始',
                 '原文已是可直接运行的写法，无需改动'],
    ),
)
