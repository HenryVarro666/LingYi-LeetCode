CONFIG = dict(
    num=2248, title='多个数组求交集', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='转集合 + 枚举 1 到 1000',
    tags=[],
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
    call='Solution().intersection([[2, 3, 1], [1, 2, 4], [2, 1, 5]])',
    expect=[1, 2],
    views=[
        dict(type='set', var='num_set_list[0]', label='第 1 个数组的集合', h=95, fmt=lambda x: str(x)),
        dict(type='set', var='num_set_list[1]', label='第 2 个数组的集合', h=95, fmt=lambda x: str(x)),
        dict(type='set', var='num_set_list[2]', label='第 3 个数组的集合', h=95, fmt=lambda x: str(x)),
        dict(type='text', fn=lambda S: (f"正在检查数 `{S['num']}`：" + ('==每个集合都有 → 进答案==' if S.get('flag') and S.get('_line') else '有集合缺它 → 淘汰') if 'num' in S else ''), size=28),
        dict(type='array', var='res', label='答案 res（从小到大自然有序）', h=130, cell=70),
    ],
    watch=['num', 'flag', ('res', 'res', 'green')],
    skip=['num_set_list = []', 'for num_list in nums', 'for num in range', 'for num_set in num_set_list', 'flag = True'],
    max_steps=50, max_events=60000,
    captions={
        'num_set_list.append': '数组转成集合：`{num_set_list[-1]}`，以后查某数在不在是 `O(1)`',
        'if num not in num_set': lambda S, B, r: (f'`{S.num}` 不在集合 `{S.num_set}` 里 → 不是公共元素' if S.num not in S.num_set
                                                  else f'`{S.num}` 在集合 `{S.num_set}` 里，继续查下一个集合'),
        'flag = False': '`flag = False`：有集合没有它',
        'break': '已经淘汰，不用再查剩下的集合 → `break`',
        'if flag': lambda S, B, r: (f'`{S.num}` 在每个集合都出现过 → ==公共元素==' if S.flag else f'`{S.num}` 被淘汰，换下一个数'),
        'res.append(num)': '`res` 加入 `{num}`：枚举顺序从小到大，答案天然升序 → {res}',
        'return res': '1 到 1000 都枚举完，返回 `{res}`',
    },
    cards=dict(
        one_liner='值域只有 1 到 1000，从小到大枚举，每个数查是否都在',
        complexity='时间 `O(1000 × n)`，空间 `O(总元素数)`',
        problem=['`nums` 是若干个不重复的正整数数组',
                 '按升序返回在==所有数组==里都出现过的数',
                 '示例：`[[3,1,2,4,5],[1,2,3,4],[3,4,5,6]]` → `[3,4]`；本视频用更小的 `[[2,3,1],[1,2,4],[2,1,5]]` → `[1,2]`'],
        quote='由于所有数的范围到在1到1000之内，同时最终答案要求从小到大进行排序，因此可以从小到大枚举1到1000内的所有数，判断这个数是否在每个数组中都出现过。',
        quote_src='—— yiduobo 题解原文',
        idea=['值域小 + 要升序 → 直接枚举 `1..1000`，不用再排序',
              '先把每个数组转成集合，判断「在不在」变成 `O(1)`',
              '一个集合没有它就 `break`；全都有才加入 `res`'],
        summary=['时间 `O(1000 × n)`，`n` 为数组个数',
                 '易错点：不转集合直接 `in` 列表会慢很多',
                 '`range(1, 1001)` 右端点要写 1001',
                 '视频中间枚举 12 到 997 的重复步骤被快进，逻辑与前面淘汰的数一样',
                 '原文本身是 Python 3 可运行写法，未改动代码'],
    ),
)
