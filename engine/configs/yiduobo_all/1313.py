CONFIG = dict(
    num=1313, title='解压缩编码列表', difficulty='Easy', category='模拟',
    author='yiduobo', technique='两两扫描展开',
    tags=[],
    code='''
class Solution(object):
    def decompressRLElist(self, nums):

        n = len(nums)
        res = []
        for index in range(0, n, 2):
            res.extend([nums[index + 1]] * nums[index])
        
        return res
''',
    call='Solution().decompressRLElist([1,2,3,4,2,5])',
    expect=[2, 4, 4, 4, 5, 5],
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（每两个数：次数 freq，值 val）', h=160),
        dict(type='array', var='res', label='res（展开结果）', h=160),
        dict(type='text', fn=lambda S: (f"`{S['nums'][S['index']]}` 个 `{S['nums'][S['index'] + 1]}` → 追加 =={[S['nums'][S['index'] + 1]] * S['nums'][S['index']]}==") if 'index' in S else '', h=90),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '一共 `{n}` 个数，每两个一组',
        'res = []': '`res` 存解压后的列表',
        'for index in range': '这一组从 `index = {index}` 开始：`nums[{index}]` 是次数，`nums[{index}+1]` 是值',
        'res.extend': '重复 `{nums[index+1]}` 共 `{nums[index]}` 次接到 `res` 后面 → `{res}`',
        'return res': '所有组处理完：`{ret}`',
    },
    cards=dict(
        one_liner='两个数一组：前面是次数，后面是值',
        complexity='时间 `O(解压后长度)`，空间 `O(1)`（不计结果）',
        problem=['`nums` 里每对 `[freq, val]` 表示 `freq` 个 `val`',
                 '把所有对依次展开拼接成一个列表',
                 '示例：`[1,2,3,4]` → `[2,4,4,4]`；本视频：`[1,2,3,4,2,5]`'],
        quote='比较基础的题目，从头开始向后两两扫描，按题目给出的方式解码后输出即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`range(0, n, 2)` 每次跳两格，正好取到每组的次数',
              '`[val] * freq` 一次生成重复的片段',
              '用 `extend` 接到结果后面，保持顺序'],
        summary=['时间 `O(S)`，`S` 是解压后的长度',
                 '易错：下标步长是 2，值在 `index+1`，次数在 `index`',
                 '`extend` 是拼接元素，`append` 会多套一层列表',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
