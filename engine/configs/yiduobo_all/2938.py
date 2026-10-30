def _col(S, i, v):
    return 'purple' if v == '1' else None


CONFIG = dict(
    num=2938, title='区分黑球与白球', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='白球依次换到目标位 t',
    code='''
class Solution(object):
    def minimumSteps(self, s):

        res = 0
        t = 0
        for index in range(len(s)):
            if s[index] == '0':
                res += index - t
                t += 1
        
        return res
''',
    call='Solution().minimumSteps("1011001")',
    expect=7,
    views=[
        dict(type='string', var='s', label='s（紫 = 黑球 1，白 = 白球 0；蓝箭头 = index，黄 = 目标位 t）', pointers={'index': 'blue', 't': 'yellow'}, color=_col, h=300),
        dict(type='text', fn=lambda S: f"下一个白球的目标位置 `t` = =={S['t']}==；累计代价 `res` = =={S['res']}==" if 't' in S else '', h=80),
    ],
    watch=[('index', 'index', 'blue'), ('t', 't', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计所有白球移动的代价',
        't = 0': '`t` 记录==下一个白球应该去的位置==，第一个白球要去下标 0',
        'for index in range': '遍历到下标 `{index}` 的球：`{s[index]}`',
        "if s[index] == '0'": lambda S, B, r: (f"下标 `{S.index}` 是白球 → 要移到下标 `{S.t}`" if S.s[S.index] == '0' else f"下标 `{S.index}` 是黑球，先跳过，留在右边"),
        'res += index - t': '白球从 `{index}` 移到 `{t}`，代价 `{index} − {t}` = {index - t}：`res` = =={res}==',
        't += 1': '这个位置占好了，下一个白球去 `t` = =={t}==',
        'return': '全部白球就位，总代价 ==`{ret}`==',
    },
    cards=dict(
        one_liner='白球按先后顺序依次换到最左边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`1` 是黑球、`0` 是白球，每次交换相邻两球，求把白球全部换到左边的最少步数',
                 '示例：`"101"` → `1`', '本视频：`"1011001"` → `7`'],
        quote='可以简单认为如果打破了这个顺序，那么必然会出现两个白球进行交换的情况，这种情况在最优解中明显是不会产生的。',
        quote_src='—— yiduobo 题解原文',
        idea=['最左的白球换到答案最左，第二个白球换到第二位……白球之间不交换',
              '变量 `t` 记下一个白球的目标位置', '白球在 `index`，代价就是 `index − t`，然后 `t += 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`', '白球相对顺序不变，才不会多花步数',
                 '对比灵神：灵神数每个 0 左边的 1，yiduobo 算每个 0 到目标位的距离，结果相同',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
