# Export the open SolidWorks assembly as triangles (tess.txt) for section.py / figure.py.
# Read-only: it only queries the model, it does not change or save anything.
# Usage (Windows PowerShell, with ASSEMBLY_main open in SolidWorks):
#   powershell -ExecutionPolicy Bypass -File export_tess.ps1 -OutFile tess.txt
# Output is about 30 MB, so it is not committed to Git (big files go to Google Drive).
param([string]$OutFile = "tess.txt")

$sw = [System.Runtime.InteropServices.Marshal]::GetActiveObject("SldWorks.Application")
$BF = [System.Reflection.BindingFlags]
function P($o, $n) { [System.__ComObject].InvokeMember($n, $BF::GetProperty, $null, $o, $null) }
function M($o, $n, $a) { [System.__ComObject].InvokeMember($n, $BF::InvokeMethod, $null, $o, $a) }

$doc = P $sw "ActiveDoc"
"Exporting: " + (M $doc "GetTitle" $null)
$comps = M $doc "GetComponents" @($false)
$sb = New-Object System.Text.StringBuilder
foreach ($c in $comps) {
    $n = P $c "Name2"
    if ($n -like "T NUT*") { continue }                      # skip small hardware
    $kids = M $c "GetChildren" $null
    if ($kids -and $kids.Count -gt 0) { continue }            # sub-assembly containers: children are listed separately
    $ad = P (P $c "Transform2") "ArrayData"                    # 3x3 rotation, translation, scale (metres)
    $bodies = M $c "GetBodies2" @(0)
    if (-not $bodies) { continue }
    [void]$sb.AppendLine("COMP|$n|" + (($ad | ForEach-Object { $_.ToString("R") }) -join ","))
    foreach ($b in $bodies) {
        foreach ($f in (M $b "GetFaces" $null)) {
            $t = M $f "GetTessTriangles" @($true)
            if ($t) { [void]$sb.AppendLine("T|" + (($t | ForEach-Object { ([double]$_).ToString("R") }) -join ",")) }
        }
    }
}
[System.IO.File]::WriteAllText((Join-Path (Get-Location) $OutFile), $sb.ToString())
"Written $OutFile"
