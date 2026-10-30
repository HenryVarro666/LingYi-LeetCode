TESTS = [[1, 2, 1], [1, 3, 2, 1]]


def _k(S):
    """刚追加的 res 元素来自 nums 的哪个下标"""
    if 'res' not in S or 'nums' not in S:
        return None
    k = len(S['res']) - len(S['nums']) - 1
    return k if k >= 0 else None


CONFIG = dict(
    num=1929, title='数组串联', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='先拷贝一份，再逐个 append',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def getConcatenation(self, nums):

        res = nums[:]
        for num in nums:
            res.append(num)
        
        return res
''',
    call='[' + ', '.join(f'Solution().getConcatenation({t})' for t in TESTS) + ']',
    expect=[t * 2 for t in TESTS],
    views=[
        dict(type='text', fn=lambda S: (f"`res` 长度 `{len(S['res'])}` / 目标 `{2 * len(S['nums'])}`" if 'res' in S else
                                        '`res = nums[:]` 先得到第一份，再把 nums 逐个接到末尾'), h=60),
        dict(type='array', var='nums', label='nums（蓝 = 刚接到 res 末尾的那个数）', h=200,
             color=lambda S, i, v: 'blue' if i == _k(S) and S.get('_line') == 6 else None),
        dict(type='array', var='res', label='res（前 n 格 = 拷贝的第一份，绿 = 刚 append 的）', h=240,
             color=lambda S, j, v: ('green' if S.get('_line') == 6 and j == len(S['res']) - 1 else
                                    'purple' if j < len(S['nums']) else None)),
    ],
    watch=['num', ('len(res)', 'len(res)', 'green')],
    captions={
        'res = nums[:]': '`nums[:]` 拷贝出第一份：`res = {res}`；==必须拷贝==，不然 res 和 nums 是同一个列表',
        'for num in nums': lambda S, B, r: (f'依次取出 `num = {S.num}`' if S.get('num') is not None and (S.get('num') != B.get('num') or 'num' not in B or S['_line'] != B.get('_line'))
                                            else 'nums 遍历完：第二份也接好了'),
        'res.append(num)': '把 `{num}` 接到 res 末尾：`res = {res}`',
        'return res': lambda S, B, r: f'返回 =={r}==',
    },
    cards=dict(
        one_liner='直接把原数组原样复制两份放进答案',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['给长为 `n` 的数组 `nums`，返回长为 `2n` 的数组 `ans`',
                 '要求 `ans[i] == nums[i]` 且 `ans[i + n] == nums[i]`，即两个 nums ==串联==',
                 '示例：`[1,2,1]` → `[1,2,1,1,2,1]`；`[1,3,2,1]` → `[1,3,2,1,1,3,2,1]`'],
        quote='比较基础的题目，==直接把原数组原样复制两份放进答案里面即可==。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一份：`res = nums[:]` 切片拷贝，一步到位',
              '第二份：遍历 nums，逐个 `append` 到 res 末尾',
              '为什么要拷贝？若 `res = nums`，边遍历边 append 同一个列表会==永远停不下来=='],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '`nums[:]` 是浅拷贝；`res = nums` 只是起别名',
                 '易错：别在遍历列表时往==同一个列表==里 append',
                 '更短的写法：`return nums + nums` 或 `nums * 2`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
