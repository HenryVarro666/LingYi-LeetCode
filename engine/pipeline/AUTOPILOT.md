# AUTOPILOT：定时任务每次运行的操作手册

你是一个**无人值守**的定时运行（每小时触发一次）。目标：继续给 LC_Video 生成题解动画视频。不要用 AskUserQuestion，不要等用户回答；遇到无法继续的情况，写清原因后结束。

背景：用量按 5 小时窗口计，每个窗口大约够做 80–100 个视频。额度用完时会话会被直接切断——所以子代理每写完一个配置就自己同步到 Mac，下一次运行开头会把上次没渲染完的补上。

## 路径
- Mac（device_bash 里）：仓库 `$HOME/mnt/LC_Video`，引擎 `$HOME/mnt/LC_Video/engine`，Obsidian 库 `$HOME/mnt/Leetcode`
- Mac（device_stage_files / device_commit_files 用的路径）：`/Users/9s/Documents/LC_Video/...`
- 云端：引擎 `/home/claude/lc_video`，简报 `/home/claude/briefs`

如果 remote-devices 工具调用失败（电脑没开 / 没连上），直接结束，说明「电脑不在线，本次跳过」。

## 0. 加锁 + 读设置
```
cd $HOME/mnt/LC_Video/engine && python3 pipeline/lock.py acquire "$(date -u +%FT%TZ)" && cat pipeline/settings.json
```
输出 `LOCKED ...` → 另一次运行还在进行，直接结束。输出 `ACQUIRED` → 记下设置（agent_model、agents_per_round、keys_per_agent、max_rounds），继续。

## 1. Mac 上的 Python 3.12 + 补渲染上次留下的配置
渲染统一用 Python 3.12（`~/py312`，每次运行的 Linux 环境是新的，没有就装，约 10 秒）：
```
export PATH=$HOME/.local/bin:$PATH; [ -x ~/py312/bin/python ] || (python3 -m pip install -q uv && uv python install 3.12 && uv venv -q ~/py312 --python 3.12 && uv pip install -q --python ~/py312/bin/python pillow pygments av sortedcontainers); ~/py312/bin/python --version
cd $HOME/mnt/LC_Video/engine && ~/py312/bin/python allsets.py recheck-failed | tail -5 && ~/py312/bin/python allsets.py check unrendered --root .. --quarantine | tail -3 && ~/py312/bin/python allsets.py render .. --jobs 4 --budget 140
```
输出里 `remaining` > 0 就再跑一次 render（每次调用 ≤ 170 秒）。

## 2. 准备云端环境
1. Mac：`cd $HOME/mnt/LC_Video/engine && python3 pipeline/pack.py engine ../_work && ls -t ../_work/briefs_*.tgz | head -1`
2. device_stage_files 把这两个文件拉到云端（`/Users/9s/Documents/LC_Video/_work/<文件名>`），等 1–2 秒。
3. 云端 Bash：
```
rm -rf /home/claude/lc_video /home/claude/briefs && mkdir -p /home/claude/lc_video
tar xzf /mnt/user-data/uploads/LC_Video/_work/<engine_ts>.tgz -C /home/claude/lc_video
tar xzf /mnt/user-data/uploads/LC_Video/_work/<briefs_ts>.tgz -C /home/claude
pip install -q av pygments pillow uv --break-system-packages
fc-list | grep -c NotoSansCJK || (apt-get install -y -q fonts-noto-cjk)
# Python 3.12 环境（和 Mac 渲染一致），子代理和 allsets.py check 会自动用它
export PATH=$HOME/.local/bin:$PATH; uv venv -q /opt/py312 --python 3.12 && uv pip install -q --python /opt/py312/bin/python pillow pygments av sortedcontainers
/opt/py312/bin/python -c "import PIL, pygments; print('py312 ok')"
cd /home/claude/lc_video && python3 allsets.py status
```

## 3. 一轮（重复，最多 max_rounds 轮）
a. `cd /home/claude/lc_video && python3 allsets.py next <agents_per_round × keys_per_agent>` → 题号列表。输出为空 → 跳到第 5 步「收尾」。
b. 按顺序每 keys_per_agent 个一组，**在同一条消息里**并行发出 agents_per_round 个 Agent 调用（subagent_type: general-purpose，model: 设置里的 agent_model），prompt 一字不改地用：
   > 按 /home/claude/lc_video/pipeline/AGENT_TASK3.md 的说明工作（先完整读它）。你负责的题号 KEY：<这一组题号，空格分隔>。简报在 /home/claude/briefs/KEY.md。你的临时目录用 /tmp/claude-0/agent<组号>。最终回复按任务文件里的格式，要短。
c. 全部返回后，兜底同步（子代理漏同步的也能补上）：`python3 pipeline/pack.py configs /mnt/user-data/outputs` → device_commit_files 写到 `/Users/9s/Documents/LC_Video/_work/<同名文件>` → Mac：`cd $HOME/mnt/LC_Video/engine && tar xzf ../_work/<sync_ts>.tgz --overwrite`
d. Mac：检查 + 渲染（`remaining` > 0 就再跑 render）：
```
cd $HOME/mnt/LC_Video/engine && ~/py312/bin/python allsets.py check unrendered --root .. --quarantine | tail -3 && ~/py312/bin/python allsets.py render .. --jobs 4 --budget 140
```
e. Mac：刷新索引和锁心跳：
```
cd $HOME/mnt/LC_Video/engine && python3 pipeline/organize.py $HOME/mnt/Leetcode $HOME/mnt/LC_Video --steps solutions,paths,index,readme --budget 150 && python3 pipeline/lock.py touch
```
然后回到 a 开始下一轮。

## 4. 结束本次运行（做满 max_rounds 轮，或还有额度但想正常结束时）
1. Mac：`cd $HOME/mnt/LC_Video/engine && python3 allsets.py status .. && cat stats.json && python3 pipeline/lock.py release`
2. 用 Projects 工具 `project_write` 覆盖写 `claude/LC_Video 视频生成进度.md`：当前 stats、本次新增数量、跳过/失败数量、时间（保留文档里「计划」一节不变，先 project_read 再改）。
3. 最后回复一两句：本次生成了多少视频、总进度。

## 5. 收尾（`next` 已经没有题号时才做）
1. `python3 allsets.py failed` 有输出 → 修复：每个子代理分 4 个，prompt：
   > 按 /home/claude/lc_video/pipeline/AGENT_TASK3.md 的说明工作（先完整读它）。下面这些配置没通过检查，错误信息在同名 .err.txt 里：<文件列表>。逐个修好后写回 configs/ling_all/ 或 configs/yiduobo_all/ 原文件名，并新建空文件 configs/failed/<dir>/KEY.fixed 作为「已修复」标记，两个文件都同步到 Mac（不要删 failed 里的文件）；作者代码保持原始写法，只改配置里自己写的部分；实在修不好就写 skip 文件说明原因。最终回复按任务文件里的格式。
   然后照第 3 步 c–e 同步、检查、渲染（兜底打包会带上 configs/failed/ 里的 .fixed 标记）。
2. Mac 全量整理一次：`python3 pipeline/organize.py $HOME/mnt/Leetcode $HOME/mnt/LC_Video --budget 150`（输出 STOPPED 就再跑）。
3. 全部完成后：用 list_triggers 找到名为「LC_Video 视频自动生成」的定时任务，update_trigger 把它 enabled=false；更新项目进度文档写明「已全部完成」；释放锁。

## 注意
- 不要修改引擎代码（engine.py / views.py / make.py / tracer.py / common.py / allsets.py / repo.py / organize.py）和 settings.json。流水线出 bug 时：记录到项目进度文档，释放锁，结束。
- Mac 的连接文件夹不允许删除文件；需要覆盖用 `tar --overwrite`，不要 rm。
