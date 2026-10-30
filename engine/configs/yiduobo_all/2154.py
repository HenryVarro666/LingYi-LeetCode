CONFIG = dict(
    num=2154, title='将找到的值乘以 2', difficulty='Easy', category='位运算',
    author='yiduobo', technique='集合记录 · 迭代翻倍',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def findFinalValue(self, nums, original):

        num_set = set(nums)
        while original in num_set:
            original += original
        
        return original
''',
    call='Solution().findFinalValue([5,3,6,1,12], 3)',
    expect=24,
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 当前 original）', h=190,
             color=lambda S, i, v: 'green' if 'original' in S and v == S['original'] else None),
        dict(type='set', var='num_set', label='num_set', h=230, fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: (f"original = ==`{S['original']}`=={'，在集合中' if S['original'] in S.get('num_set', ()) else '，不在集合中'}"
                                        if 'num_set' in S else ''), size=34, h=100),
    ],
    watch=[('original', 'original', 'blue')],
    captions={
        'num_set = set': '用集合 `num_set` 记录出现过的数字，查找 `O(1)`',
        'while original in num_set': lambda S, B, r: (f'`original = {S.original}` 在集合里 → 继续迭代' if S.original in S.num_set
                                                      else f'`original = {S.original}` 不在集合里 → 结束循环'),
        'original += original': '`original + original` 就是乘 2：`original` = =={original}==',
        'return original': '当前 `original` 已不在集合中，返回 =={ret}==',
    },
    cards=dict(
        one_liner='用集合记数字，从 original 开始一路翻倍到找不到为止',
        complexity='时间 `O(n + log(U/original))`，空间 `O(n)`',
        problem=['在 `nums` 中找 `original`，找到就翻倍继续，找不到就返回当前值', '示例：`nums=[5,3,6,1,12]`，`original=3` → `24`',
                 '示例：`nums=[2,7,9]`，`original=4` → `4`'],
        quote='使用集合记录出现过的数字，然后从original开始迭代。若当前的original出现在集合中，那么就将original更新为original * 2，然后重复此过程直到当前original不在集合中为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `nums` 转成集合，一次转换后每次查找 `O(1)`', '在集合里就 `original += original`（翻倍），继续查',
              '不在集合里就停，当前值即答案'],
        summary=['时间 `O(n + log(U/original))`，空间 `O(n)`',
                 '易错：必须用集合而不是列表查找，否则每轮 `O(n)`',
                 '原文已是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神把它归结为“找最小的不在 nums 里的 original·2^k”，还给出位运算优化'],
    ),
)
