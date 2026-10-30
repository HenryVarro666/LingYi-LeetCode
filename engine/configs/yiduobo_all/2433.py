CONFIG = dict(
    num=2433, title='找出前缀异或的原始数组', difficulty='Medium', category='位运算',
    author='yiduobo', technique='异或推导 · 一趟遍历',
    tags=['异或的性质', '难度分 1367'],
    code='''
class Solution(object):
    def findArray(self, pref):

        res = [pref[0]]
        for index in range(1, len(pref)):
            res.append(pref[index] ^ pref[index - 1])
        
        return res
''',
    call='Solution().findArray([5,2,0,3,1])',
    expect=[5, 7, 2, 3, 2],
    views=[
        dict(type='array', var='pref', label='pref（蓝箭头 = 当前 index）', cell=90, pointers={'index': 'blue'}, h=230),
        dict(type='array', var='res', label='res（还原出的 arr，绿 = 新加入）', cell=90, h=170,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='text', fn=lambda S: (f"`res[{S['index']}] = pref[{S['index']}] ^ pref[{S['index']-1}] = {S['pref'][S['index']]} ^ {S['pref'][S['index']-1]} = {S['pref'][S['index']] ^ S['pref'][S['index']-1]}`") if 'index' in S and S['index'] >= 1 else '', size=26, h=90),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = [pref[0]]': '`arr[0] = pref[0] = {pref[0]}`：只有一项时前缀异或就是它自己',
        'for index': lambda S, B, r: (f'`index = {S.index}`，还原 `arr[{S.index}]`' if len(S.res) < len(S.pref) else '`index` 已走完，循环结束'),
        'res.append': '`pref[{index}] ^ pref[{index-1}` = `{pref[index]} ^ {pref[index-1]}` = =={res[-1]}==，把 `arr[{index}]` 放进 res',
        'return res': '一趟遍历结束，返回 `{res}`',
    },
    cards=dict(
        one_liner='相邻两项前缀异或再异或一次，多出来的就是 arr[index]',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['`pref[i]` 是 `arr[0] ^ ... ^ arr[i]`，由 `pref` 还原 `arr`',
                 '示例：`[5,2,0,3,1]` → `[5,7,2,3,2]`'],
        quote='pref[index] = pref[index - 1] ^ arr[index]，于是就有 arr[index] = pref[index] ^ pref[index - 1]。',
        quote_src='—— yiduobo 题解原文',
        idea=['先写出 `pref[index]` 和 `pref[index-1]` 两个式子',
              '它们只差最后一项 `arr[index]`',
              '两边同时异或 `pref[index-1]`，前面各项两两抵消'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计答案）',
                 '`arr[0] = pref[0]` 要单独处理，循环从 1 开始',
                 '易错：`x ^ x = 0` 让前缀项相互抵消，这是推导的关键',
                 '原文为 Python 2 风格，代码无需改动（已是 Python 3 可运行）'],
    ),
)
