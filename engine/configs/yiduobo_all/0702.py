CONFIG = dict(
    num=702, title='搜索长度未知的有序数组', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='固定上界 9999 的二分',
    tags=['灵神题单·二分算法'],
    setup='''
class ArrayReader(object):
    def __init__(self, a):
        self.a = a
    def get(self, i):
        return self.a[i] if 0 <= i < len(self.a) else 2147483647
reader = ArrayReader([-1, 0, 3, 5, 9, 12])
arr = reader.a
''',
    code='''
#class ArrayReader(object):

class Solution(object):
    def search(self, reader, target):

        left = 0
        right = 9999
        while left <= right:
            mid = (left + right) >> 1
            v = reader.get(mid)
            if v == 2147483647 or v > target:
                right = mid - 1
            elif v < target:
                left = mid + 1
            else:
                return mid
        
        return -1
''',
    call='Solution().search(reader, 9)',
    expect=4,
    views=[
        dict(type='array', var='reader.a', label='reader 背后的数组（只能用 reader.get(i) 访问）', h=210,
             color=lambda S, i, v: 'yellow' if 'mid' in S and S['mid'] == i else None),
        dict(type='text', h=120, fn=lambda S: (f"候选区间 `[{S['left']}, {S['right']}]`，`mid = {S['mid']}`" + (f"，`reader.get({S['mid']}) = ==越界 2^31-1==`" if 'v' in S and S['v'] == 2147483647 else (f"，`reader.get({S['mid']}) = ==={S['v']}==`" if 'v' in S else '')) if 'mid' in S else (f"候选区间 `[{S['left']}, {S['right']}]`" if 'right' in S else ''))),
    ],
    watch=['left', 'right', 'mid', 'v', ('target', 'target', 'green')],
    captions={
        'left = 0': '下标从 `0` 开始',
        'right = 9999': '题目保证长度不超过 10000，所以上界直接取 ==`9999`==',
        'while left <= right': lambda S, B, r: f'`left = {S.left} <= right = {S.right}`，继续二分' if S.left <= S.right else f'`left = {S.left} > right = {S.right}`：区间空了，没找到',
        'mid = (left': '`mid = ({left} + {right}) >> 1 = {mid}`',
        'v = reader.get': lambda S, B, r: f'`reader.get({S.mid})` = ' + ('==2147483647==，说明 `mid` 已经超出数组末尾' if S.v == 2147483647 else f'=={S.v}=='),
        'if v == 2147483647': lambda S, B, r: (f'`v = 2^31-1`：越界 → ==成立==，答案只可能在左边' if S.v == 2147483647 else (f'`v = {S.v} > target = {S.target}` → ==成立==，答案在 `mid` 左边' if S.v > S.target else f'`v = {S.v}` 在界内且 `<= target = {S.target}`，不成立')),
        'right = mid - 1': '去左半边：`right = {right}`',
        'elif v < target': lambda S, B, r: f'`v = {S.v} < target = {S.target}` → ==成立==，答案在右边' if S.v < S.target else f'`v = {S.v}` 不小于 `target`',
        'left = mid + 1': '去右半边：`left = {left}`',
        'return mid': '`v == target`，找到了，下标 ==`{ret}`==',
        'return -1': '二分结束仍没找到，`target` 不在数组里 → `-1`',
    },
    cards=dict(
        one_liner='不知道长度，就把越界值当成无穷大，在 0~9999 上二分',
        complexity='时间 `O(log 10000)`，空间 `O(1)`',
        problem=['有序数组长度未知，只能通过 `reader.get(i)` 访问；越界时返回 `2^31-1`',
                 '找 `target` 的下标，不存在返回 `-1`',
                 '示例：`[-1,0,3,5,9,12]`，`target = 9` → `4`'],
        quote='由于题目保证了数组长度不超过10000，因此二分的初始边界可以设定为left = 0，right = 9999，接下来开始进行二分。',
        quote_src='—— yiduobo 题解原文',
        idea=['越界返回 `2^31-1`，比任何合法值都大 → 和 `v > target` 一样处理',
              '`v > target` 或越界：去左边；`v < target`：去右边',
              '等于就直接返回下标'],
        summary=['时间 `O(log C)`，`C = 10000`；空间 `O(1)`',
                 '越界值要并进 `v > target` 分支，否则会往右越走越远',
                 '`(left + right) >> 1` 等价于整除 2',
                 '视频里补了 `ArrayReader`（原文只留了注释），方便演示'],
    ),
    max_steps=100,
)
