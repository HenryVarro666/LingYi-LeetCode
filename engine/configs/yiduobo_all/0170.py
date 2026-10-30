CONFIG = dict(
    num=170, title='两数之和 III - 数据结构设计', difficulty='Easy', category='设计',
    author='yiduobo', technique='哈希表计数 + find 时遍历', tags=[],
    code='''
class TwoSum(object):

    def __init__(self):
        self.cnt_dict = {}

    def add(self, number):
        self.cnt_dict[number] = self.cnt_dict.get(number, 0) + 1

    def find(self, value):
        for number in self.cnt_dict:
            target = value - number
            if number == target:
                if self.cnt_dict[number] >= 2:
                    return True
                else:
                    continue
            elif target in self.cnt_dict:
                return True
        
        return False
''',
    call='''ts = TwoSum()
out = []
ts.add(1)
ts.add(3)
ts.add(4)
out.append(ts.find(4))
out.append(ts.find(6))
ts.add(3)
out.append(ts.find(6))
out''',
    expect=[True, False, True],
    views=[
        dict(type='map', var='self.cnt_dict', label='cnt_dict（数 → 出现次数）', fmt=lambda k, v: f'{k} → {v} 次', h=200, font=34),
        dict(type='text', size=30, h=100, fn=lambda S: f"find({S['value']})：当前数 `{S['number']}`，需要配 `{S['value']} − {S['number']}` = =={S['target']}==" if 'target' in S and 'value' in S else (f"find({S['value']})" if 'value' in S else '')),
        dict(type='text', size=30, h=90, fn=lambda S: '各次 find 的结果 `out` = ' + str(S['out']) if 'out' in S else ''),
    ],
    watch=[('number', 'number', 'blue'), ('value', 'value', 'orange'), ('target', 'target', 'pink'), ('out', 'out', 'green')],
    captions={
        'self.cnt_dict = {}': '空哈希表：记录每个数出现的次数',
        'self.cnt_dict[number] =': '`add({number})`：次数加一 → `{self.cnt_dict[number]}` 次',
        'for number in self.cnt_dict': '遍历哈希表里的每个数：当前 `number = {number}`',
        'target = value - number': '`find({value})` 需要另一个数 `target = {value} − {number} = {target}`',
        'if number == target': '`number == target`？`{number} == {target}` → {"相等，要看次数" if number == target else "不等"}',
        'if self.cnt_dict[number] >= 2': '同一个数要用两次：`{number}` 出现 `{self.cnt_dict[number]}` 次 → {"够两次" if self.cnt_dict[number] >= 2 else "不够，不能自己配自己"}',
        'return True': '找到一对和为 `{value}` 的数，返回 `True`',
        'continue': '次数不够，换下一个数',
        'elif target in self.cnt_dict': '`{target}` 在表里吗？→ {"在，两数之和成立" if target in self.cnt_dict else "不在，换下一个"}',
        'return False': '所有数都试过，没有一对和为 `{value}` → `False`',
    },
    cards=dict(
        one_liner='add 只记次数，find 时遍历：差值在不在表里',
        complexity='`add` 为 `O(1)`，`find` 为 `O(n)`，空间 `O(n)`',
        problem=['设计 `TwoSum`：`add(number)` 加入一个数，`find(value)` 判断是否存在两数之和等于 `value`',
                 '同一个数可以用两次，前提是它加入过两次',
                 '本视频：`add 1,3,4`；`find(4)`；`find(6)`；`add 3`；`find(6)`'],
        quote='对于查询操作，则需要遍历哈希表中的所有数number，判断value - number是否也存在于哈希表中。需要特别注意的是，当number = value - number时，需要判断number出现的次数是否大于等于两次。',
        quote_src='—— yiduobo 题解原文',
        idea=['在线操作，不预处理所有两数之和：`add` 次数多时那样太慢',
              '用哈希表而不是有序数组 + 双指针：==维护有序更麻烦==',
              '`find`：枚举 `number`，查 `value - number`；相等时看次数 `≥ 2`'],
        summary=['`add` `O(1)`，`find` `O(n)`，空间 `O(n)`',
                 '易错：`number == target` 时必须出现至少两次，如只加过一个 3，`find(6)` 为 `False`',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
