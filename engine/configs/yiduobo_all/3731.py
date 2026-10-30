CONFIG = dict(
    num=3731, title='找出缺失的元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='集合判重 · while 逐个检测',
    tags=[],
    code='''
class Solution(object):
    def findMissingElements(self, nums):
        
        num_set = set(nums)
        mi = min(nums)
        ma = max(nums)
        x = mi + 1
        res = []
        while x < ma:
            if x not in num_set:
                res.append(x)
            x += 1
        
        return res
''',
    call='Solution().findMissingElements([7,3,9,4])',
    expect=[5, 6, 8],
    views=[
        dict(type='array', var='nums', label='nums', cell=84),
        dict(type='set', var='num_set', label='num_set', fmt=lambda x: str(x)),
        dict(type='array', var='res', label='res（缺失的整数）', cell=84, color=lambda S, i, v: 'green'),
        dict(type='text', fn=lambda S: (f"从 mi+1 = `{S['mi']+1}` 检测到 ma-1 = `{S['ma']-1}`，当前 x = ==`{S['x']}`==" if 'x' in S else ''), size=26),
    ],
    watch=['mi', 'ma', ('x', 'x', 'blue'), 'res'],
    captions={
        'num_set = set': '先把 `nums` 放进集合 `num_set`，判断某个数在不在只要 O(1)',
        'mi = min': '最小值 `mi = {mi}`',
        'ma = max': '最大值 `ma = {ma}`：这两个端点一定在 nums 里，不用检查',
        'x = mi + 1': '从 `mi + 1 = {x}` 开始往后检测',
        'res = []': '`res` 收集缺失的整数',
        'while x < ma': lambda S, B, r: (f'`x = {S.x} < ma = {S.ma}`，还没走到最大值，继续' if S.x < S.ma else f'`x = {S.x} == ma = {S.ma}`，检测完毕'),
        'if x not in': lambda S, B, r: (f'`{S.x}` 不在 num_set 里 → ==它是缺失的=='  if S.x not in S.num_set else f'`{S.x}` 在 num_set 里 → 没缺失，跳过'),
        'res.append': '把 `{x}` 加入 `res`：`{res}`',
        'x += 1': '`x` → {x}',
        'return res': '缺失的整数是 `{res}`',
    },
    cards=dict(
        one_liner='取出最小、最大值，中间每个数查一下在不在集合里',
        complexity='时间 `O(D)`，空间 `O(n)`',
        problem=['`nums` 由互不相同的整数组成，原本覆盖某个范围内的所有整数，现在缺了一些',
                 '范围的最小值和最大值仍在 `nums` 里；按升序返回缺失的整数，没缺就返回空列表',
                 '本视频：`[7,3,9,4]` → `[5,6,8]`'],
        quote='先取出nums中的最小值mi以及最大值ma，然后从mi + 1开始向后遍历，到ma - 1为止，检测目前遍历到的元素是否在nums中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`set(nums)` 让「在不在」变成 O(1)',
              '`x` 从 `mi + 1` 往后走，到 `ma - 1` 为止（`x < ma`）',
              '不在集合里的 `x` 追加进 `res`，因为 `x` 递增，结果自然有序'],
        summary=['时间 `O(D)`，空间 `O(n)`，`D = ma − mi`',
                 '易错：循环条件是 `x < ma`，端点本身不检查',
                 '原文 Python 2 写法，无需改动（只有 `set`/`min`/`max`）',
                 '对比灵神：灵神用一行列表推导式，这里用 `while` 手动自增'],
    ),
)
