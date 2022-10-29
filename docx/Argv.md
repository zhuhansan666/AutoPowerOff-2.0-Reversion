# Config.json 的参数

## 一级参数
`apo-time` -> str 开始提醒自动关机的时间 (%H:%M:%S) <br>
`apo-must-time` -> str 强制关机时间 (%H:%M:%S) <br>
`timeout` -> int/float 键鼠无操作最大时间, 超过此时间弹出关机提示 (秒) <br>
`after-fullscreen-timeout` -> int/float 在全屏应用关闭后键鼠无操作最大时间, 超过此时间弹出关机提示 (秒) <br>
`debug` -> dict debug参数, 详见下方 <br>

## Debug 参数
`out-log` -> bool 是否输出日志 <br>
`log-level` -> int/str 日志输出级别 (即python logging DEBUG/INFO/WARNING/ERROR, 分别对应10/20/30/40) <br>

