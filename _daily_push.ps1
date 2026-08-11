# 每日公开数据推送 (本地工具, Task Scheduler 调用; 建议收盘后 15:40 运行, 在 daemon 日检之后)
# 前置: 代码/public_dashboard 已是独立 git 仓库且已配置公开 remote (部署方案见任务报告)
$ErrorActionPreference = 'Stop'
$code = 'c:\Users\ASUS\Desktop\D\信息资源学\代码'
python -X utf8 "$code\quant\public_export.py"
if ($LASTEXITCODE -ne 0) { Write-Error 'public_export 失败, 中止推送'; exit 1 }
$pub = "$code\public_dashboard"
git -C $pub add data/equity_public.json
git -C $pub diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $today = Get-Date -Format 'yyyy-MM-dd'
    git -C $pub commit -m "data: $today 净值更新"
    git -C $pub push
    Write-Output "已推送 $today 净值更新"
} else {
    Write-Output '无新变化 (非交易日或未导出), 跳过'
}
