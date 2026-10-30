CONFIG = dict(
    num=1773, title='统计匹配检索规则的物品数量', difficulty='Easy', category='模拟',
    author='yiduobo', technique='确定列下标后一趟扫描',
    tags=[],
    code='''
class Solution(object):
    def countMatches(self, items, ruleKey, ruleValue):

        cnt = 0
        if ruleKey == 'type':
            check_index = 0
        elif ruleKey == 'color':
            check_index = 1
        else:
            check_index = 2

        res = 0
        for item in items:
            if item[check_index] == ruleValue:
                res += 1

        return res
''',
    call='Solution().countMatches([["tv","red","a1"],["pc","tan","b2"],["tv","sky","c3"]], "type", "tv")',
    expect=2,
    views=[
        dict(type='table', var='items', label='items（列：type / color / name）', h=300,
             cols=['type', 'color', 'name'],
             color=lambda S, i, j, v: ('green' if S.get('item') is not None and S['items'][i] is S['item']
                                       and 'check_index' in S and j == S['check_index']
                                       and v == S['ruleValue'] else
                                       ('yellow' if S.get('item') is not None and S['items'][i] is S['item']
                                        and 'check_index' in S and j == S['check_index'] else None))),
        dict(type='text', fn=lambda S: '检索：`ruleKey = %s`，`ruleValue = %s`' % (S['ruleKey'], S['ruleValue']), size=28, h=70),
    ],
    watch=['ruleKey', 'ruleValue', 'check_index', ('item', 'item'), ('res', 'res', 'green')],
    captions={
        "ruleKey == 'type'": '`ruleKey` 决定看每件物品的哪一列：type 是第 0 列',
        "ruleKey == 'color'": '不是 type，再看是不是 color（第 1 列）',
        'check_index = 0': '要查 type → 下标 `check_index = 0`',
        'check_index = 1': '要查 color → 下标 `check_index = 1`',
        'check_index = 2': '剩下只可能是 name → 下标 `check_index = 2`',
        'item[check_index] == ruleValue': '`{item}[{check_index}] = {item[check_index]!r}`，和 `{ruleValue!r}` 比较 → ==' '{"相等" if item[check_index] == ruleValue else "不相等"}==',
        'res += 1': '匹配成功，`res` 加一 → {res}',
        'return res': '扫完全部物品，共 `{res}` 件匹配',
    },
    cards=dict(
        one_liner='先把检索类型换成列下标，再一趟扫描计数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每件物品是 `[type, color, name]`，再给检索规则 `ruleKey` 和 `ruleValue`',
                 '统计第 `ruleKey` 个属性等于 `ruleValue` 的物品数',
                 '示例：规则 `type = tv` → 匹配 `2` 件'],
        quote='首先根据要检索的种类确定在数组中寻找的下标，然后一趟扫描枚举就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`type`、`color`、`name` 分别对应下标 0、1、2',
              '先算出 `check_index`，之后每件物品只需比较一个位置',
              '相等就计数加一，扫描结束即答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`check_index` 只算一次，不要在循环里重复判断类型',
                 '`cnt = 0` 在原文中是多余的变量，没有被使用',
                 '原文为 Python 2 写法，Python 3 下可直接运行，代码未改'],
    ),
)
