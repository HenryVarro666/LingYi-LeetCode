CONFIG = dict(
    num=2248, title='多个数组求交集', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='转集合 · 枚举 1 到 1000', tags=[],
    code='''
class Solution(object):
    def intersection(self, nums):

        num_set_list = []
        for num_list in nums:
            num_set_list.append(set(num_list))
        
        res = []
        for num in range(1, 1001):
            flag = True
            for num_set in num_set_list:
                if num not in num_set:
                    flag = False
                    break
            
            if flag:
                res.append(num)
        
        return res
''',
    call='Solution().intersection([[3,1,2],[2,3,1,4],[3,2,5]])',
    expect=[2, 3],
    trace_limit=80, max_steps=70,
    views=[
        dict(type='text', fn=lambda S: ('枚举的数 `num` = ==' + str(S['num']) + '==' if 'num' in S and not isinstance(S['num'], list) else ''), h=80),
        dict(type='set', var='num_set', h=200, label='当前检查的集合 num_set'),
        dict(type='array', var='res', h=170, label='res（升序枚举，天然有序）'),
    ],
    watch=['num', ('flag', 'flag', 'green')],
    captions={
        'num_set_list.append': '数组转成集合，==查某个数在不在里面==变成 O(1)',
        'for num in range(1, 1001)': '值域只有 1 到 1000，从小到大枚举，答案自然升序：试 `{num}`',
        'flag = True': '先假设 `{num}` 在所有数组中都出现',
        'for num_set in num_set_list': '依次检查每个数组的集合：`{num_set}`',
        'if num not in num_set': lambda S, B, r: (f'`{S.num}` 不在 `{S.num_set}` 里 → 有数组缺它' if S.num not in S.num_set else f'`{S.num}` 在 `{S.num_set}` 里 → 继续查下一个'),
        'flag = False': '这个数不是公共元素：`flag = False`',
        'break': '已经不满足，不用再查后面的集合',
        'if flag': lambda S, B, r: (f'`flag` 为真：`{S.num}` 在每个数组里都有 → 加入答案' if S.flag else f'`flag` 为假：`{S.num}` 不是交集元素，试下一个数'),
        'res.append': '`{num}` 加入答案 → `{res}`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='值域只有 1000：从小到大逐个数问，每个数组里有没有',
        complexity='时间 `O(1000 × m + L)`，空间 `O(L)`',
        problem=['二维数组 `nums`，子数组内元素互不相同',
                 '返回在所有数组里都出现的数，升序',
                 '示例：`[[3,1,2],[2,3,1,4],[3,2,5]]` → `[2, 3]`'],
        quote='由于所有数的范围到在1到1000之内，同时最终答案要求从小到大进行排序，因此可以从小到大枚举1到1000内的所有数',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个数组转成集合，判断「某个数在不在」只要 O(1)',
              '值域小：直接从 1 枚举到 1000，免去最后的排序',
              '用 `flag` 记录是否每个集合都有它，缺一个就 `break`'],
        summary=['时间 `O(1000 × m + L)`，m 为数组个数，空间 `O(L)`',
                 '易错点：必须先转集合，否则每次查找都是线性的',
                 '枚举值域省去排序，但值域大时这个办法就不适用了',
                 '视频只追踪前面一部分步骤，后面的数同理，快进到结束'],
    ),
)
