CONFIG = dict(
    num=2303, title='计算应缴税款总额', difficulty='Easy', category='模拟',
    author='yiduobo', technique='last 记录上一档上限，一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def calculateTax(self, brackets, income):

        last = 0
        res = 0
        for upper, percent in brackets:
            if income > upper:
                res += (upper - last) * percent / 100.0
            else:
                res += (income - last) * percent / 100.0
                break
        
            last = upper

        return res
''',
    call='Solution().calculateTax([[3,50],[7,10],[12,25]], 10)',
    expect=2.65,
    views=[
        dict(type='grid', var='brackets', cols=['上限', '税率%'], h=230,
             color=lambda S, i, j, v: 'blue' if 'upper' in S and S['brackets'][i][0] == S['upper'] else None),
        dict(type='text', fn=lambda S: (f"上一档上限 `last = {S['last']}`，已缴税 `res = {S['res']:.2f}`" if 'last' in S else ''), h=70),
    ],
    watch=['income', 'last', 'upper', 'percent', ('res', 'res', 'green')],
    captions={
        'last = 0': '`last` 记录上一个税级的上限，起点是 0',
        'res = 0': '`res` 累计税款',
        'for upper, percent': '看这一档：上限 `{upper}`，税率 `{percent}%`',
        'if income > upper': '`income = {income}` {">" if income > upper else "≤"} `upper = {upper}`：{"收入超过本档上限，整档都要交税" if income > upper else "收入在本档内结束"}',
        'res += (upper - last)': '整档税：`({upper} − {last}) × {percent}%` → `res = {res:.2f}`',
        'res += (income - last)': '最后一段：`({income} − {last}) × {percent}%` → `res = {res:.2f}`',
        'break': '收入算完了，直接结束遍历',
        'last = upper': '本档上限成为下一档起点：`last = {last}`',
        'return res': '应缴税款总额 =={res}==',
    },
    cards=dict(
        one_liner='用 last 记上一档上限，超过就整档收，否则收到 income 为止',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`brackets` 是各档的 `[上限, 税率%]`，每档只对本档范围内的收入收税',
                 '给定总收入 `income`，求总税款',
                 '示例：`[[3,50],[7,10],[12,25]]`，`income = 10` → `2.65`'],
        quote='使用一个变量last记录上一个税级上限，然后一趟遍历。若总收入大于当前遍历到的税级上限，那么就根据当前税级上限与last之差来计算税额并累加至答案',
        quote_src='—— yiduobo 题解原文',
        idea=['`income > upper`：这一档被收满，段长 `upper - last`',
              '否则只收到 `income`，段长 `income - last`，然后 `break`',
              '每档处理完把 `last` 更新为本档上限'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '每档直接用 `/ 100.0` 做浮点累加，对本题精度足够',
                 '原文本身可直接在 Python 3 运行，未做修改',
                 '易错：`last = upper` 只在整档收满时更新；走到 `break` 就不需要了'],
    ),
)
