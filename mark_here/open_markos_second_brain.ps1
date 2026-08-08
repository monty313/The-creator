# MARK HERE portable launcher.
# Works from ANY location of this mark_here folder.
# 1) Prefer live ARMY MarkOS chat when 01_SYSTEM is found
# 2) Ensure local knowledge pack exists (sync if empty + sources available)
# 3) If chat offline, open portable knowledge pack

$ErrorActionPreference = "Continue"
$Kit = $PSScriptRoot
$PortablePath = Join-Path $Kit "PORTABLE.json"
$KnowIndex = Join-Path $Kit "knowledge\00_INDEX.md"
$SoulFileLocal = Join-Path $Kit "knowledge\soul\MARK_PERSONALITY.md"
$SyncScript = Join-Path $Kit "sync_portable_pack.ps1"
$ChatUrl = "http://127.0.0.1:8000/chat"
$HealthUrl = "http://127.0.0.1:8000/api/health"

function Test-MarkOSApi {
  try {
    $r = Invoke-WebRequest -Uri $HealthUrl -UseBasicParsing -TimeoutSec 2
    return ($r.StatusCode -ge 200 -and $r.StatusCode -lt 300)
  } catch {
    return $false
  }
}

function Resolve-ArmyRoot {
  $candidates = New-Object System.Collections.Generic.List[string]
  if ($env:MARKOS_ARMY_ROOT) { [void]$candidates.Add($env:MARKOS_ARMY_ROOT) }
  if (Test-Path -LiteralPath $PortablePath) {
    try {
      $cfg = Get-Content -LiteralPath $PortablePath -Raw -Encoding UTF8 | ConvertFrom-Json
      if ($cfg.canonical_when_online.army_system_default) {
        [void]$candidates.Add([string]$cfg.canonical_when_online.army_system_default)
      }
    } catch {}
  }
  $parent = Split-Path -Parent $Kit
  [void]$candidates.Add((Join-Path $parent "ARMY\01_SYSTEM"))
  [void]$candidates.Add((Join-Path (Split-Path -Parent $parent) "ARMY\01_SYSTEM"))
  [void]$candidates.Add("C:\Users\user\OneDrive\Desktop\ARMY\01_SYSTEM")
  [void]$candidates.Add("C:\Users\user\Desktop\ARMY\01_SYSTEM")
  foreach ($c in $candidates) {
    $probe = Join-Path $c "config\agents\MARK_PERSONALITY.md"
    if ($c -and (Test-Path -LiteralPath $probe)) {
      return (Resolve-Path -LiteralPath $c).Path
    }
  }
  return $null
}

function Resolve-TruthRoot {
  $candidates = New-Object System.Collections.Generic.List[string]
  if ($env:MARKOS_THE_TRUTH_ROOT) { [void]$candidates.Add($env:MARKOS_THE_TRUTH_ROOT) }
  $parent = Split-Path -Parent $Kit
  if (Test-Path -LiteralPath (Join-Path $parent "GOAL.md")) {
    [void]$candidates.Add($parent)
  }
  [void]$candidates.Add("C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth")
  foreach ($c in $candidates) {
    if ($c -and (Test-Path -LiteralPath (Join-Path $c "GOAL.md"))) {
      return (Resolve-Path -LiteralPath $c).Path
    }
  }
  return $null
}

function Ensure-PortablePack {
  $hasSoul = Test-Path -LiteralPath $SoulFileLocal
  $hasIndex = Test-Path -LiteralPath $KnowIndex
  if ($hasSoul -and $hasIndex) { return $true }
  if (-not (Test-Path -LiteralPath $SyncScript)) { return $false }
  Write-Host "  Portable pack missing pieces - running sync..."
  try {
    & $SyncScript -Quiet
  } catch {
    Write-Host "  sync failed: $_"
  }
  return (Test-Path -LiteralPath $SoulFileLocal)
}

function Open-OfflinePack {
  Write-Host ""
  Write-Host "  OFFLINE MODE - using portable knowledge pack in this folder."
  Write-Host "  Soul / KAG / doctrine / lab live under mark_here\knowledge\"
  Write-Host ""
  if (Test-Path -LiteralPath $KnowIndex) {
    Start-Process $KnowIndex
  } elseif (Test-Path -LiteralPath $SoulFileLocal) {
    Start-Process $SoulFileLocal
  } else {
    Write-Host "  ERROR: knowledge pack empty. On a machine with ARMY + the-truth, run:"
    Write-Host "    .\sync_portable_pack.ps1"
  }
  $kagLaw = Join-Path $Kit "knowledge\kag\configs\fable5_mark_here_kag.json"
  $pt5 = Join-Path $Kit "knowledge\doctrine\llm_basic_thinking\pack\pt5__basic_knowledge.txt"
  if (Test-Path -LiteralPath $SoulFileLocal) { Start-Process $SoulFileLocal }
  if (Test-Path -LiteralPath $pt5) { Start-Process $pt5 }
  if (Test-Path -LiteralPath $kagLaw) { Start-Process $kagLaw }
}

Write-Host ""
Write-Host "  ========================================"
Write-Host "   MARK HERE!  --  portable Second Brain"
Write-Host "   Kit: $Kit"
Write-Host "  ========================================"
Write-Host ""

$ArmySystem = Resolve-ArmyRoot
$TruthRoot = Resolve-TruthRoot
$null = Ensure-PortablePack

if (Test-Path -LiteralPath $SoulFileLocal) {
  Write-Host "  Local soul pack:  YES"
} else {
  Write-Host "  Local soul pack:  NO"
}
if (Test-Path -LiteralPath $KnowIndex) {
  Write-Host "  Local knowledge:  YES - knowledge\00_INDEX.md"
} else {
  Write-Host "  Local knowledge:  NO"
}
if ($ArmySystem) {
  Write-Host "  ARMY 01_SYSTEM:   $ArmySystem"
} else {
  Write-Host "  ARMY 01_SYSTEM:   not found"
}
if ($TruthRoot) {
  Write-Host "  the-truth lab:    $TruthRoot"
} else {
  Write-Host "  the-truth lab:    not found (ok if pack already synced)"
}
Write-Host "  Chat:             $ChatUrl"
Write-Host ""

if ($ArmySystem) { $env:MARKOS_ARMY_ROOT = $ArmySystem }
if ($TruthRoot) { $env:MARKOS_THE_TRUTH_ROOT = $TruthRoot }

$live = $false
if ($ArmySystem) {
  $StartScript = Join-Path $ArmySystem "scripts\start_service.ps1"
  $SoulCanonical = Join-Path $ArmySystem "config\agents\MARK_PERSONALITY.md"
  Write-Host "  Canonical soul:   $SoulCanonical"

  if (-not (Test-MarkOSApi)) {
    Write-Host "  Second Brain offline -- starting Army service..."
    if (Test-Path -LiteralPath $StartScript) {
      try { & $StartScript } catch { Write-Host "  start failed: $_" }
    } else {
      Write-Host "  Missing start_service.ps1"
    }
    for ($i = 1; $i -le 25; $i++) {
      Start-Sleep -Seconds 1
      if (Test-MarkOSApi) { $live = $true; break }
      Write-Host "  waiting for chat... ($i/25)"
    }
  } else {
    $live = $true
  }

  if ($live) {
    Write-Host "  Opening MarkOS Second Brain (live chat)..."
    Start-Process $ChatUrl
    Write-Host "  Talk to Mark (same soul as ARMY)."
    if (Test-Path -LiteralPath $KnowIndex) {
      Write-Host "  Portable pack still available at knowledge\00_INDEX.md"
    }
    Start-Sleep -Seconds 2
    exit 0
  }

  Write-Host "  Live chat not ready."
} else {
  Write-Host "  ARMY not on this machine - cannot start live MarkOS API."
}

Open-OfflinePack
Write-Host "  Press any key to close..."
try {
  $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} catch {}
exit 0
