CONFIG = dict(
    num=2113, title='查询删除和添加元素后的数组', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='找规律 · 对 2n 取模',
    code='''
class Solution(object):
    def elementInNums(self, nums, queries):

        n = len(nums)
        res = []
        for t, index in queries:
            t %= (n + n)
            if t < n:
                if index < n - t:
                    res.append(nums[index + t])
                else:
                    res.append(-1)
            else:
                if index < t - n:
                    res.append(nums[index])
                else:
                    res.append(-1)
        
        return res
''',
    call='Solution().elementInNums([0,1,2], [[0,2],[2,0],[3,2],[5,0]])',
    expect=[2, 2, -1, 0],
    views=[
        dict(type='array', var='nums', label='nums（原数组）', cell=84, h=150,
             color=lambda S, i, v: 'pink' if 'index' in S and 't' in S and 'res' in S and i == (S['index'] + S['t'] if S['t'] < S['n'] else S['index']) and S['_line'] >= 9 else None),
        dict(type='text', h=90, size=28,
             fn=lambda S: ('第 `%d` 分钟：%s' % (S['t'], ('数组 = nums[%d:]，长度 %d' % (S['t'], S['n'] - S['t']))
                                          if S['t'] < S['n'] else ('数组 = nums[:%d]，长度 %d' % (S['t'] - S['n'], S['t'] - S['n']))))
             if 't' in S and 'index' in S and 'res' in S and S['_line'] >= 9 else '前 n 分钟逐个删掉开头，后 n 分钟逐个补回'),
        dict(type='array', var='res', label='res（每个询问的答案）', cell=84, h=150, color=lambda S, i, v: 'green'),
    ],
    watch=[('n', 'n'), ('t', 't', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '一轮变化共 `2n` 分钟：先删 n 步，再补 n 步。`n = {n}`',
        'res = []': '`res` 按顺序保存每个询问的答案',
        'for t, index in queries': '询问：第 `{t}` 分钟，下标 `{index}`',
        't %= (n + n)': '数组每 `2n = {n + n}` 分钟循环一次 → 只看 `t = {t}`',
        'if t < n': lambda S, B, r: (f'`t = {S.t} < n = {S.n}`：前 n 步，数组是 ==后缀== `nums[{S.t}:]`，长度 `{S.n - S.t}`'
                                     if S.t < S.n else f'`t = {S.t} ≥ n = {S.n}`：后 n 步，数组是 ==前缀== `nums[:{S.t - S.n}]`，长度 `{S.t - S.n}`'),
        'if index < n - t': lambda S, B, r: (f'`index = {S.index} < 长度 {S.n - S.t}` → 下标在范围内'
                                             if S.index < S.n - S.t else f'`index = {S.index} ≥ 长度 {S.n - S.t}` → 下标越界'),
        'res.append(nums[index + t])': '后缀从 `nums[t]` 开始，答案 `nums[{index}+{t}] = {res[-1]}`',
        'if index < t - n': lambda S, B, r: (f'`index = {S.index} < 长度 {S.t - S.n}` → 下标在范围内'
                                             if S.index < S.t - S.n else f'`index = {S.index} ≥ 长度 {S.t - S.n}` → 下标越界'),
        'res.append(nums[index])': '前缀从 `nums[0]` 开始，答案 `nums[{index}] = {res[-1]}`',
        'res.append(-1)': '数组长度不够 → 答案 `-1`',
        'return res': '全部询问的答案：`{res}`',
    },
    cards=dict(
        one_liner='数组按 2n 分钟循环，前半是后缀，后半是前缀',
        complexity='时间 `O(q)`，空间 `O(1)`（不计答案），q 为询问数',
        problem=['`nums` 每分钟删掉最左元素直到为空，再每分钟从左到右补回一个',
                 '每个询问 `[time, index]`：第 `time` 分钟 `nums[index]` 是多少，越界为 `-1`',
                 '示例：`nums = [0,1,2]`，`[2,0]` → `2`，`[3,2]` → `-1`'],
        quote='找规律的题目，首先数组是按照2n次每轮的长度进行变换，那么对于某个询问[time, index]，可以先将time对2n取模。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `t %= 2n`，只看一轮内的第 `t` 分钟',
              '`t < n`：数组是后缀，长度 `n - t`，答案是 `nums[index + t]`',
              '`t ≥ n`：数组是前缀，长度 `t - n`，答案是 `nums[index]`；下标 ≥ 长度则 `-1`'],
        summary=['时间 `O(q)`，空间 `O(1)`（不计答案）',
                 '易错：`t = n` 时数组为空，要归入后半段（长度 0）',
                 '先判 `index` 是否越界，再取值',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
