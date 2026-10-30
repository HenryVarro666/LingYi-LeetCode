def _cur(S):
    ins = S.get('_inner', {})
    return ins.get('ast')


CONFIG = dict(
    num=2126, title='摧毁小行星', difficulty='Medium', category='位运算',
    author='yiduobo', technique='排序 + 一趟贪心',
    tags=['灵神题单', '位运算', '难度分 1335'],
    code='''
class Solution(object):
    def asteroidsDestroyed(self, mass, asteroids):

        for ast in sorted(asteroids):
            if mass >= ast:
                mass += ast
            else:
                return False

        return True
''',
    call='Solution().asteroidsDestroyed(10, [3, 9, 19, 5, 21])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"行星质量 `mass` = =={S['mass']}==" + (f"，正在撞质量 `{S['ast']}` 的小行星" if 'ast' in S else ''), size=28),
        dict(type='array', var=lambda S: sorted(S['asteroids']), label='sorted(asteroids)：从小到大逐个撞（绿 = 已摧毁，蓝 = 当前）',
             cell=100, h=300, pointers={'sorted(asteroids).index(ast)': 'blue'}, pointer_labels={'sorted(asteroids).index(ast)': 'ast'},
             color=lambda S, i, v: ('green' if 'ast' in S and v < S['ast'] else 'blue' if 'ast' in S and v == S['ast'] else None)),
    ],
    watch=[('mass', 'mass', 'green'), ('ast', 'ast', 'blue')],
    captions={
        'for ast in sorted': lambda S, B, r: (f'先排序，再取下一颗：`ast = {S.ast}`' if 'ast' in S and S.get('ast') != B.get('ast') or 'ast' not in B
                                              else '小行星都撞完了'),
        'if mass >= ast': lambda S, B, r: (f'`mass = {S.mass} ≥ ast = {S.ast}` → ==能摧毁==' if S.mass >= S.ast
                                           else f'`mass = {S.mass} < ast = {S.ast}` → ==撞不碎，行星被摧毁=='),
        'mass += ast': '摧毁后吸收质量：`mass` += {ast} → =={mass}==，下一颗更容易撞',
        'return False': '当前最小的剩余小行星都撞不碎，后面更大的更不行 → `False`',
        'return True': '遍历完，没有撞不碎的 → `True`',
    },
    cards=dict(
        one_liner='排好序，一趟遍历：能摧毁就累加，不能就失败',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['行星 `mass` 可按任意顺序与小行星碰撞，`mass ≥ 小行星` 才能摧毁并增重',
                 '问能否全部摧毁',
                 '本视频：`mass = 10, [3,9,19,5,21]` → `true`'],
        quote='比较简单的贪心题，将小行星从小到大进行排序，然后一趟遍历尝试逐个摧毁。',
        quote_src='—— yiduobo 题解原文',
        idea=['质量越小越容易摧毁，先摧毁它们可以让行星越来越大',
              '对当前小行星：能摧毁就 `mass += ast`，不能就直接返回 `False`',
              '遍历完都没失败，返回 `True`'],
        result='依次吃下 3, 5, 9, 19, 21，质量一路增长 → True ✓',
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 产生新列表）',
                 '比较条件是 `mass >= ast`，==相等也能摧毁==',
                 '对比灵神：他用二进制长度分组免去排序，达到 `O(n)`'],
    ),
)
