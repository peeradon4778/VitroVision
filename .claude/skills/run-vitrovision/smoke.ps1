#!/usr/bin/env pwsh
# VitroVision / VitroShelf smoke driver
# Usage: .\smoke.ps1 [start|stop|test|all]
# Default: all (start -> test -> stop)

$PYTHON   = "C:\Users\User\miniconda3\envs\ml\python.exe"
$APP_DIR  = Join-Path $PSScriptRoot "..\..\..\shelf_manager"
$PORT     = 5001
$BASE     = "http://localhost:$PORT"
$PID_FILE = Join-Path $PSScriptRoot "server.pid"

function Start-VitroServer {
    if (Test-Path $PID_FILE) {
        $old = Get-Content $PID_FILE
        if (Get-Process -Id $old -ErrorAction SilentlyContinue) {
            Write-Host "[skip] server already running PID $old"
            return
        }
    }
    $resolved = (Resolve-Path $APP_DIR).Path
    $proc = Start-Process -FilePath $PYTHON -ArgumentList "main.py" `
        -WorkingDirectory $resolved -PassThru -WindowStyle Hidden
    $proc.Id | Out-File $PID_FILE
    Write-Host "[start] PID $($proc.Id)"

    $deadline = (Get-Date).AddSeconds(30)
    while ((Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 500
        try {
            $r = Invoke-WebRequest -Uri "$BASE/api/ml_status" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            $j = $r.Content | ConvertFrom-Json
            if ($j.ready) {
                Write-Host "[ready] ML modules loaded"
                return
            }
        } catch {
            # not up yet
        }
    }
    Write-Host "[warn] server not ready after 30s - ML still loading, tests may still pass"
}

function Stop-VitroServer {
    if (Test-Path $PID_FILE) {
        $savedPid = Get-Content $PID_FILE
        $target = Get-Process -Id $savedPid -ErrorAction SilentlyContinue
        if ($target) {
            $target | Stop-Process -Force
            Write-Host "[stop] killed PID $savedPid"
        }
        Remove-Item $PID_FILE -Force
    } else {
        Write-Host "[skip] no pid file"
    }
}

function Run-SmokeTests {
    $pass = 0
    $fail = 0

    $checks = @(
        @{ label = "ml_status (all ready)"; url = "$BASE/api/ml_status" },
        @{ label = "dashboard /";           url = "$BASE/" },
        @{ label = "scan page";             url = "$BASE/scan" },
        @{ label = "glass page";            url = "$BASE/glass" },
        @{ label = "train page";            url = "$BASE/train" },
        @{ label = "analytics page";        url = "$BASE/analytics" },
        @{ label = "growth_data API";       url = "$BASE/api/growth_data" },
        @{ label = "glass_state API";       url = "$BASE/api/glass_state" },
        @{ label = "al_query API";          url = "$BASE/api/al_query" }
    )

    Write-Host "`n=== Smoke Tests ==="
    foreach ($c in $checks) {
        try {
            $r = Invoke-WebRequest -Uri $c.url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
            if ($r.StatusCode -eq 200) {
                Write-Host "  [OK]   $($c.label)"
                $pass++
            } else {
                Write-Host "  [FAIL] $($c.label) - HTTP $($r.StatusCode)"
                $fail++
            }
        } catch {
            Write-Host "  [FAIL] $($c.label) - $_"
            $fail++
        }
    }

    Write-Host "`nResult: $pass passed, $fail failed"
    if ($fail -gt 0) { exit 1 }
}

$cmd = if ($args.Count -gt 0) { $args[0] } else { "all" }
switch ($cmd) {
    "start" { Start-VitroServer }
    "stop"  { Stop-VitroServer }
    "test"  { Run-SmokeTests }
    default {
        Start-VitroServer
        Run-SmokeTests
        Stop-VitroServer
    }
}
