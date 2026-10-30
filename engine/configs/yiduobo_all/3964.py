CONFIG = dict(
    num=3964, title='照亮道路的最少灯泡数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组 · 最左未照亮处右边装灯',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维', '难度分 1572'],
    code='''
class Solution(object):
    def minLights(self, lights):
        
        n = len(lights)
        f = [0] * (n + 1)
        for index, v in enumerate(lights):
            if v > 0:
                f[max(0, index - v)] += 1
                f[min(n - 1, index + v) + 1] -= 1

        res = 0
        now = 0
        for index in range(n):
            now += f[index]
            if now == 0:
                res += 1
                now += 1
                f[min(n - 1, index + 2) + 1] -= 1
        
        return res
''',
    call='Solution().minLights([0,0,0,0,0,1,0,0])',
    expect=3,
    views=[
        dict(type='array', var='lights', pointers={'index': 'blue'}, h=170, label='lights'),
        dict(type='array', var='f', pointers={'index': 'blue'}, h=170, label='f（差分数组）'),
        dict(type='text', fn=lambda S: (f"位置 `{S['index']}`：当前生效灯泡 `now` = =={S['now']}==，已额外安装 `res` = {S['res']}" if 'now' in S and 'res' in S else '')),
    ],
    watch=['index', ('v', 'v', 'cyan'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'f = [0]': '`f[index]`：在 `index` 处生效（+1）或失效（−1）的灯泡数',
        'if v > 0': lambda S, B, r: f'`lights[{S.index}] = {S.v}`：' + ('有灯泡' if S.v > 0 else '没灯泡，跳过'),
        'f[max(0, index - v)] += 1': '照明起点 `{max(0, index-v)}` 处生效 → `f[{max(0, index-v)}] = {f[max(0, index-v)]}`',
        'f[min(n - 1, index + v) + 1] -= 1': '终点是 `{min(n-1, index+v)}`，下一位 `{min(n-1, index+v)+1}` 起失效 → `f[{min(n-1, index+v)+1}] = {f[min(n-1, index+v)+1]}`',
        'now += f[index]': '位置 `{index}` 生效的灯泡数 `now = {now}`',
        'if now == 0': lambda S, B, r: f'`now = {S.now}`：' + ('==没有灯泡照到==这个位置，要额外装灯' if S.now == 0 else '有灯泡照到，无事发生'),
        'res += 1': '最左边的黑暗位置 `{index}`：装在 `{min(index+1,n-1)}`（`index+1`，到头则 `n-1`），左边无需求、右边能多照两格 → `res = {res}`',
        'now += 1': '新灯泡也照到当前位置：`now` 加 1 → {now}',
        'f[min(n - 1, index + 2) + 1] -= 1': '新灯泡照到 `{min(n-1,index+2)}`，下一位起失效 → `f[{min(n-1,index+2)+1}] = {f[min(n-1,index+2)+1]}`',
        'return res': '最少额外灯泡 `{res}` 个',
    },
    cards=dict(
        one_liner='最左边没被照到的位置 p，灯泡装在 p + 1 最划算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['长度 `n` 的路，`lights[index] = v > 0` 表示该处有灯，照亮 `[index−v, index+v]`',
                 '额外灯泡装在 `j`，照亮 `[j−1, j+1]`',
                 '求让每个位置都可见的最少额外灯数；本视频 `[0,0,0,0,0,1,0,0]` → `3`'],
        quote='对于最左侧没被找到的位置p，如果想要为其提供照明，只能在p - 1、p、p + 1三个位置中选择一个安装额外灯泡。为了使得额外安装的灯泡数量最少，在这里显然应该在p + 1安装额外灯泡',
        quote_src='—— yiduobo 题解原文',
        idea=['先不管额外灯泡：灯泡起点 `+1`、失效处 `−1`，扫一遍用 `now` 记录生效数',
              '`now == 0` 就是最左的黑暗位置，在 `index + 1` 装灯：`res` 和 `now` 都加 1',
              '这个灯泡在 `index + 3` 失效，所以 `f[index + 3]` 减 1（有 `min` 保护）'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f` 长度 `n + 1`，失效下标用 `min(n − 1, 终点) + 1`',
                 '`now == 0` 时才装灯，装完 `now` 要加 1，否则会重复装',
                 '原文已是 Python 3 可运行的写法，未做改动',
                 '对比灵神：灵神把新灯泡的失效点写成 `min(i + 3, n)`，等价'],
    ),
)
