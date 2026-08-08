# Open portable Mark knowledge pack (no ARMY service required).
$Kit = $PSScriptRoot
$Index = Join-Path $Kit "knowledge\00_INDEX.md"
$Soul = Join-Path $Kit "knowledge\soul\MARK_PERSONALITY.md"
$Pt5 = Join-Path $Kit "knowledge\doctrine\llm_basic_thinking\pack\pt5__basic_knowledge.txt"
$Kag = Join-Path $Kit "knowledge\kag\configs\fable5_mark_here_kag.json"
$Price = Join-Path $Kit "knowledge\00_PRICE_DATA.md"
if (-not (Test-Path $Price)) { $Price = Join-Path $Kit "PRICE_DATA.md" }
$Flea = Join-Path $Kit "FLEA_JAR_AND_PERFORMANCE.md"
if (-not (Test-Path $Flea)) { $Flea = Join-Path $Kit "knowledge\00_FLEA_JAR_AND_PERFORMANCE.md" }
$Lid = Join-Path $Kit "knowledge\doctrine\00_LID_OFF_THE_JAR.md"
$Cure = Join-Path $Kit "knowledge\doctrine\flea-jar\THE_FLEA_CURE.md"
$Perf1 = Join-Path $Kit "knowledge\performance\PERFORMANCE_IS_POSSIBLE.md"

Write-Host "MARK HERE offline pack - $Kit"
if (Test-Path $Index) { Start-Process $Index } else { Write-Host "Missing knowledge\00_INDEX.md - run .\sync_portable_pack.ps1 first" }
if (Test-Path $Soul) { Start-Process $Soul }
if (Test-Path $Pt5) { Start-Process $Pt5 }
if (Test-Path $Kag) { Start-Process $Kag }
if (Test-Path $Price) { Start-Process $Price }
if (Test-Path $Flea) { Start-Process $Flea }
if (Test-Path $Lid) { Start-Process $Lid }
if (Test-Path $Cure) { Start-Process $Cure }
if (Test-Path $Perf1) { Start-Process $Perf1 }
