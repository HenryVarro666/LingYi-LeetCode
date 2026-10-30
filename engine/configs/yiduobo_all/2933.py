CONFIG = dict(
    num=2933, title='高访问员工', difficulty='Medium', category='字符串',
    author='yiduobo', technique='哈希表收集 + 排序比较上上个时间点', tags=[],
    code='''
class Solution(object):
    def findHighAccessEmployees(self, access_times):

        times_dict = {}
        for name, t in access_times:
            if name not in times_dict:
                times_dict[name] = []
            times_dict[name].append(int(t[:2]) * 60 + int(t[2:]))
        
        res = []
        for name in times_dict:
            times_list = sorted(times_dict[name])
            for i in range(2, len(times_list)):
                if times_list[i] - times_list[i - 2] < 60:
                    res.append(name)
                    break
        
        return res
''',
    call='Solution().findHighAccessEmployees([["d","0002"],["c","0808"],["c","0829"],["e","0215"],["d","1508"],["d","1444"],["d","1410"],["c","0809"]])',
    expect=['d', 'c'],
    views=[
        dict(type='map', var='times_dict', fmt=lambda k, v: f'{v}', label='times_dict：姓名 → 访问时间（分钟）', h=260),
        dict(type='array', var='times_list', pointers={'i': 'blue'}, label='times_list（当前员工，已排序）', h=170),
        dict(type='array', var='res', label='res（高访问员工）', h=130),
    ],
    watch=['name', 'i', ('res', 'res', 'green')],
    captions={
        'times_dict = {}': '哈希表：员工 → 他所有访问时间',
        'if name not in times_dict': lambda S, B, r: ('第一次见 `%s`，新建列表' % S.name) if S.name not in S.times_dict else '`%s` 已经有列表了' % S.name,
        'append(int(t[:2])': '`{t}` 转分钟：`{t[:2]}×60 + {t[2:]}`，放入 `{name}` 的列表',
        'times_list = sorted': '`{name}` 的访问时间从小到大排序：`{times_list}`',
        'for i in range(2': lambda S, B, r: (f'从第 3 个时间点开始看：只有 `{len(S.times_list)}` 次访问，不足 3 次' if len(S.times_list) < 3 else f'从第 3 个时间点开始，对比它与上上个时间点（`i = {S.i}`）' if 'i' in S else '下一位员工'),
        'if times_list[i] - times_list[i - 2] < 60': lambda S, B, r: (
            f'`{S.times_list[S.i]} − {S.times_list[S.i-2]} = {S.times_list[S.i]-S.times_list[S.i-2]}`'
            + (' `< 60`：这三次访问在一小时内' if S.times_list[S.i]-S.times_list[S.i-2] < 60 else ' `>= 60`：跨度超过一小时，继续')),
        'res.append(name)': '`{name}` 是高访问员工，加入 `res`',
        'break': '已确认，不用再看该员工的其他时间',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='排序后只看「上上个」时间点，差不到一小时就算高访问',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`access_times[i] = [姓名, 时间]`，同一天内的 4 位时间',
                 '同一小时内访问 ≥ 3 次是高访问员工，差恰好 60 分钟不算',
                 '本视频：8 条记录 → `["d","c"]`'],
        quote='对于当前遍历到的时间点，若其上上个时间点与当前时间点的时间差在一小时以内，那么说明当前时间点、上一个时间点以及上上个时间点这三次访问出现在一小时内。',
        quote_src='—— yiduobo 题解原文',
        idea=['用哈希表把每个员工的访问时间收集成 list，转成分钟后排序',
              '从第 3 个时间点开始，和上上个时间点比较',
              '差 `< 60` 即三次在一小时内，记录并 `break`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：必须严格 `< 60`',
                 '原文无需修改，Python 3 直接可运行',
                 '对比灵神：灵神用 defaultdict + any()，这里是显式 if/break'],
    ),
)
