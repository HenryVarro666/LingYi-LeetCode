def _cur(S, i):
    return i == len(S['ans']) if 'ans' in S else False


CONFIG = dict(
    num=2640, title='一个数组所有前缀的分数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='一边遍历维护前缀最大值与前缀和', tags=[],
    code='''
class Solution:
    def findPrefixScore(self, nums: List[int]) -> List[int]:
        ans = []
        mx = s = 0
        for x in nums:
            mx = max(mx, x)  # 前缀最大值
            s += x + mx  # 累加前缀的得分
            ans.append(s)
        return ans
''',
    call='Solution().findPrefixScore([2,3,7,5,10])',
    expect=[4, 10, 24, 36, 56],
    views=[
        dict(type='text', fn=lambda S: f"当前前缀得分：`s` = 之前 + `x` + `mx` = =={S['s']}==" if 's' in S and 'x' in S else ''),
        dict(type='array', var='nums', label='nums（蓝 = 当前处理的数，灰 = 已处理）', h=165,
             color=lambda S, i, v: 'blue' if _cur(S, i) else None,
             dim=lambda S, i, v: 'ans' in S and i < len(S['ans'])),
        dict(type='array', var='ans', label='ans（每个前缀的分数）', h=165,
             color=lambda S, i, v: 'green' if i == len(S['ans']) - 1 else None),
    ],
    watch=[('x', 'x', 'blue'), ('mx', 'mx', 'orange'), ('s', 's', 'green')],
    captions={
        'mx = max': '前缀最大值：`max({B.mx}, {x})`，得 =={mx}==',
        's += x + mx': '累加得分：`s = {B.s} + {x} + {mx} = =={s}==`，这个前缀的转换数组和',
        'ans.append': '把当前前缀的分数 `{s}` 记入答案',
        'return ans': '每个前缀的分数都在 `ans` 里了：`{ans}`',
    },
    cards=dict(
        one_liner='边遍历边维护前缀最大值和前缀分数和',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['`conver[i] = arr[i] + max(arr[0..i])`，分数 = conver 的和',
                 '对每个前缀 `nums[0..i]` 求分数，返回数组',
                 '示例：`[2,3,7,5,10]` → `[4,10,24,36,56]`'],
        quote='一边遍历，一边计算前缀最大值 mx，以及前缀的得分之和 s。',
        quote_src='—— 灵茶山艾府题解',
        idea=['新来一个 `x`：先更新 `mx`，它的转换值就是 `x + mx`',
              '前缀分数是前一个前缀分数加上这一项，==不用重新求和=='],
        summary=['时间 `O(n)`，空间 `O(1)`，返回值不计入',
                 '==先更新 mx 再累加==：转换值用的是包含自己的前缀最大值',
                 '数值可达 1e9，Python 不会溢出；其他语言要用 64 位整数',
                 '同类：前缀最大值、前缀和一起维护'],
    ),
)
