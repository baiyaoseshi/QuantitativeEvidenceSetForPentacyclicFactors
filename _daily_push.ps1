# 每日公开数据推送 (任务计划程序 PublicDashboardDailyPush 每日 15:40 调用, 收盘+daemon 日检之后)
# 前置: 本目录已是独立 git 仓库且配置 origin (2026-08-11 已完成); 推送需 Clash TUN 在线
# 日志: 本目录 _daily_push.log (仅本地, 不进公开仓库 — 推送只 add data/equity_public.json)
$ErrorActionPreference = 'Stop'
$code = 'c:\Users\ASUS\Desktop\D\信息资源学\代码'
$pub = "$code\public_dashboard"
$log = "$pub\_daily_push.log"

function Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
    $line | Out-File $log -Append -Encoding utf8
    Write-Output $line
}

try {
    $exportOut = python -X utf8 "$code\quant\public_export.py" 2>&1
    Log "export: $exportOut"
    if ($LASTEXITCODE -ne 0) { Log 'ERROR: public_export 失败, 中止推送'; exit 1 }

    git -C $pub add data/equity_public.json
    git -C $pub diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        $today = Get-Date -Format 'yyyy-MM-dd'
        git -C $pub commit -m "data: $today 净值更新" | Out-Null
        $pushOut = git -C $pub push 2>&1
        if ($LASTEXITCODE -ne 0) { Log "ERROR: push 失败 (检查 Clash TUN): $pushOut"; exit 1 }
        Log "已推送 $today 净值更新"
    } else {
        Log '无新变化 (非交易日), 跳过'
    }
} catch {
    Log "ERROR: 未捕获异常 $_"
    exit 1
}
