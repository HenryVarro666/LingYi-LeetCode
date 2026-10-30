CONFIG = dict(
    num=339, title='嵌套列表权重和', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='递归 · 深度加权',
    setup='''
class NestedInteger:
    def __init__(self, v=None):
        self.v = v if v is not None else []
    def isInteger(self):
        return isinstance(self.v, int)
    def getInteger(self):
        return self.v
    def getList(self):
        return self.v
    def __repr__(self):
        return str(self.v) if isinstance(self.v, int) else '[' + ','.join(map(repr, self.v)) + ']'
def _mk(x):
    return NestedInteger(x) if isinstance(x, int) else NestedInteger([_mk(y) for y in x])
nl = [_mk(y) for y in [[1, 1], 2, [1, [3]]]]
''',
    code='''
class Solution(object):
    def depthSum(self, nestedList):

        global res
        res = 0

        def calc(now, depth):
            global res
            for part in now:
                if part.isInteger():
                    res += part.getInteger() * depth
                else:
                    calc(part.getList(), depth + 1)
        
        calc(nestedList, 1)
        return res
''',
    call='Solution().depthSum(nl)',
    expect=17,
    views=[
        dict(type='text', fn=lambda S: (f"当前深度 `depth = {S['depth']}`，正在看 `{S['part']!r}`" if 'part' in S and 'depth' in S else '准备从深度 1 开始递归'), h=60),
        dict(type='array', var='now', label='now（当前这一层的元素）', pointers={'k': 'blue'} if False else {}, h=150),
        dict(type='calls', h=300),
    ],
    watch=['depth'],
    captions={
        'res = 0': '全局答案 `res` 清零，累加所有“数字 × 深度”',
        'calc(nestedList, 1)': '从最外层开始，深度 `1`',
        'for part in now': '取这一层的下一个元素 `part = {part!r}`',
        'if part.isInteger()': lambda S, B, r: (f'`{S.part!r}` 是整数 → 直接乘当前深度' if S.part.isInteger() else f'`{S.part!r}` 是列表 → 要往里一层'),
        'res += part': lambda S, B, r: f'`res += {S.part.getInteger()} × {S.depth}` = ==+{S.part.getInteger() * S.depth}==，累加进 `res`',
        'calc(part.getList()': '是列表：深度 +1 递归：`calc(.., {B.depth} + 1)` 进入第 {B.depth + 1} 层',
        'return res': '全部算完：`2+2+2+2+9`，答案 ==`{ret}`==',
    },
    cards=dict(
        one_liner='遇到列表就递归，每深一层权重加 1',
        complexity='时间 `O(n)`（每个元素一次），空间 `O(d)`（d 为最大深度）',
        problem=['嵌套列表里每个整数的权重 = 它所在的==深度==（最外层为 1）',
                 '返回所有整数 × 深度 之和',
                 '示例：`[[1,1],2,[1,[3]]]` → `1×2+1×2+2×1+1×2+3×3 = 17`'],
        quote='若part是一个整数，那么就将其与当前深度相乘，然后将乘积累加到最终答案中。若part是一个list，那么就在深度加1的前提下递归求解part。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举当前列表的每个元素 `part`',
              '整数：加 `值 × depth`；列表：`calc(part.getList(), depth + 1)`',
              '用全局变量 `res` 累加，递归不用返回值'],
        summary=['时间 `O(n)`，空间 `O(d)`',
                 '易错：进入子列表要 ==depth + 1==，而不是 res 加 1',
                 '内层函数里改全局 `res` 要再写一次 `global res`',
                 '题目的 NestedInteger 接口（isInteger/getInteger/getList）在 setup 里补了一个等价实现'],
    ),
)
