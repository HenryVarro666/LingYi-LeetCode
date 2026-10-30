CONFIG = dict(
    num=1996, title='游戏中弱角色的数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序后一遍扫描',
    code='''
class Solution(object):
    def numberOfWeakCharacters(self, properties):

        sorted_properties = sorted(properties, key=lambda d:(-d[0], d[1]))

        max_def = sorted_properties[0][1]
        res = 0
        for index in range(1, len(sorted_properties)):
            if sorted_properties[index][1] < max_def:
                res += 1
            else:
                max_def = sorted_properties[index][1]
            
        return res
''',
    call='Solution().numberOfWeakCharacters([[1,5],[10,4],[4,3],[4,6],[4,2],[7,7]])',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"当前防御 `{S['sorted_properties'][S['index']][1]}`，之前最大防御 `max_def = {S['max_def']}`" if 'index' in S and 'max_def' in S else ''), h=60),
        dict(type='array', var='sorted_properties', label='sorted_properties（攻击, 防御）', fmt=lambda v: f'{v[0]},{v[1]}', cell=140,
             pointers={'index': 'blue'}, h=260),
    ],
    watch=[('index', 'index', 'blue'), ('max_def', 'max_def', 'cyan'), ('res', 'res', 'green')],
    captions={
        'sorted_properties = sorted': '先排序：攻击从大到小，攻击相同防御小的在前：`{sorted_properties}`',
        'max_def = sorted_properties[0]': '第一个角色攻击最大，先把它的防御当作 `max_def = {max_def}`',
        'res = 0': '`res` 统计弱角色数量',
        'for index in range': '从第 2 个角色开始；`index = {index}`，严格强于它的角色只可能在前面',
        'if sorted_properties[index][1] < max_def': '防御 `{sorted_properties[index][1]}` 与 `max_def = {max_def}`：{"前面有防御更高的人 → 它是弱角色" if sorted_properties[index][1] < max_def else "没人防御更高 → 不是弱角色"}',
        'res += 1': '弱角色 +1：`res` → {res}',
        'max_def = sorted_properties[index]': '`max_def` 更新为 `{max_def}`；攻击相同时小防御排前面，所以同攻击的不会互相误判',
        'return res': '弱角色一共 `{res}` 个',
    },
    cards=dict(
        one_liner='先让一个指标有序，再枚举另一个指标',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个角色有攻击和防御；另一角色两项都严格更高，则该角色是弱角色',
                 '求弱角色数量',
                 '本视频用 6 个角色 `[[1,5],[10,4],[4,3],[4,6],[4,2],[7,7]]` → `4`'],
        quote='对于这类多指标严格大于的问题，常见的做法是通过某种手段保证其中的一些指标有序，然后枚举另一些指标进行判断。',
        quote_src='—— yiduobo 题解原文',
        idea=['攻击从大到小排序：严格更强的人只会出现在前面',
              '记录前面出现过的最大防御，大于当前防御就是弱角色',
              '攻击相同时防御小的排前面，避免同攻击被误判'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 生成新数组）',
                 '易错点：==攻击相同要按防御升序==',
                 '原文还提到：三指标常用第一维排序 + 第二维归并，四指标再配数据结构',
                 '原文为 Python 2 风格，本题无需改动即可运行'],
    ),
)
