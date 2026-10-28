
# Windows IT Support Diagnostics Tool
# Step 2: System Information

Write-Host "=================================="
Write-Host "   IT SUPPORT DIAGNOSTICS TOOL"
Write-Host "=================================="
Write-Host ""

Write-Host "Starting system diagnostics..."
Write-Host ""

# Retrieve Windows system information
$computerName = $env:COMPUTERNAME
$operatingSystem = Get-CimInstance Win32_OperatingSystem
$processor = Get-CimInstance Win32_Processor
$computerSystem = Get-CimInstance Win32_ComputerSystem

# Calculate total installed RAM in GB
$totalRAM = [math]::Round($computerSystem.TotalPhysicalMemory / 1GB, 2)

# Calculate system uptime
$uptime = (Get-Date) - $operatingSystem.LastBootUpTime

# Display results
Write-Host "=================================="
Write-Host "       SYSTEM INFORMATION"
Write-Host "=================================="

Write-Host "Computer Name: $computerName"
Write-Host "Operating System: $($operatingSystem.Caption)"
Write-Host "CPU: $($processor.Name)"
Write-Host "Total RAM: $totalRAM GB"
Write-Host "System Uptime: $($uptime.Days) days, $($uptime.Hours) hours"

Write-Host ""
Write-Host "System information collected successfully!"


# ==================================
# Step 3: Network Diagnostics
# ==================================

Write-Host ""
Write-Host "=================================="
Write-Host "       NETWORK DIAGNOSTICS"
Write-Host "=================================="

# Retrieve network configuration
$network = Get-NetIPConfiguration |
    Where-Object { $_.IPv4Address -and $_.IPv4DefaultGateway } |
    Select-Object -First 1

if ($null -ne $network) {

    $ipAddress = $network.IPv4Address.IPAddress
    $gateway = $network.IPv4DefaultGateway.NextHop
    $dnsServers = @($network.DNSServer.ServerAddresses) -join ", "

    Write-Host "IPv4 Address: $ipAddress"
    Write-Host "Default Gateway: $gateway"
    Write-Host "DNS Servers: $dnsServers"

    # Test connectivity to the default gateway
    $gatewayReachable = Test-Connection -ComputerName $gateway -Count 2 -Quiet -ErrorAction SilentlyContinue

    if ($gatewayReachable) {
        Write-Host "[PASS] Default gateway is reachable" -ForegroundColor Green
    }
    else {
        Write-Host "[WARNING] Default gateway did not respond to ping" -ForegroundColor Yellow
    }
}
else {
    Write-Host "[WARNING] No active IPv4 network with a default gateway was found" -ForegroundColor Yellow
}

# Test DNS resolution
try {
    $dnsResult = Resolve-DnsName -Name "google.com" -Type A -ErrorAction Stop
    
    if ($dnsResult) {
        Write-Host "[PASS] DNS resolution successful" -ForegroundColor Green
    }
}
catch {
    Write-Host "[WARNING] DNS resolution failed" -ForegroundColor Yellow
}

# Test HTTPS connectivity
$internetTest = Test-NetConnection -ComputerName "google.com" -Port 443 -InformationLevel Quiet -WarningAction SilentlyContinue

if ($internetTest) {
    Write-Host "[PASS] HTTPS connectivity successful" -ForegroundColor Green
}
else {
    Write-Host "[WARNING] HTTPS connectivity test failed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Network diagnostics completed!"



# ==================================
# Step 4: System Health Monitoring
# ==================================

Write-Host ""
Write-Host "=================================="
Write-Host "       SYSTEM HEALTH"
Write-Host "=================================="

# Check local disk space
Write-Host ""
Write-Host "--- Disk Space ---"

$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType = 3"

foreach ($disk in $disks) {

    if ($disk.Size -le 0) {
        continue
    }

    $freePercent = [math]::Round(
        ($disk.FreeSpace / $disk.Size) * 100, 2
    )

    $freeGB = [math]::Round($disk.FreeSpace / 1GB, 2)

    Write-Host "$($disk.DeviceID) - $freeGB GB free ($freePercent%)"

    if ($freePercent -lt 20) {
        Write-Host "[WARNING] Low disk space on $($disk.DeviceID)" -ForegroundColor Yellow
    }
    else {
        Write-Host "[PASS] Disk space is healthy" -ForegroundColor Green
    }
}

# Check important Windows services
Write-Host ""
Write-Host "--- Windows Services ---"

$servicesToCheck = @(
    "Winmgmt",
    "EventLog",
    "Dhcp"
)

foreach ($serviceName in $servicesToCheck) {

    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

    if ($null -eq $service) {
        Write-Host "[WARNING] Service $serviceName not found" -ForegroundColor Yellow
    }
    elseif ($service.Status -eq "Running") {
        Write-Host "[PASS] $serviceName is running" -ForegroundColor Green
    }
    else {
        Write-Host "[WARNING] $serviceName is $($service.Status)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "System health diagnostics completed!"



# ==================================
# Step 5: Troubleshooting Recommendations
# ==================================

Write-Host ""
Write-Host "=================================="
Write-Host "   TROUBLESHOOTING RECOMMENDATIONS"
Write-Host "=================================="

$recommendations = @()

# Evaluate disk space
foreach ($disk in $disks) {

    if ($disk.Size -le 0) {
        continue
    }

    $freePercent = ($disk.FreeSpace / $disk.Size) * 100

    if ($freePercent -lt 20) {
        $recommendations += (
            "LOW DISK SPACE on $($disk.DeviceID) - " +
            "Review Storage settings, temporary files, " +
            "and unused applications. Avoid deleting " +
            "unknown system files."
        )
    }
}

# Evaluate gateway connectivity
if ($null -eq $network) {
    $recommendations += (
        "NETWORK CONFIGURATION: No active IPv4 " +
        "connection with a default gateway was detected. " +
        "Check the network adapter and IP configuration."
    )
}
elseif (-not $gatewayReachable) {
    $recommendations += (
        "GATEWAY CONNECTIVITY: Verify the local " +
        "network connection, adapter status, and " +
        "default gateway configuration."
    )
}

# Evaluate DNS resolution
if (-not $dnsResult) {
    $recommendations += (
        "DNS: Verify configured DNS servers and " +
        "test resolution of another known domain."
    )
}

# Evaluate HTTPS connectivity
if (-not $internetTest) {
    $recommendations += (
        "HTTPS CONNECTIVITY: Check firewall settings, " +
        "network connectivity, and whether the " +
        "destination is reachable."
    )
}

# Evaluate Windows services
foreach ($serviceName in $servicesToCheck) {

    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

    if ($null -eq $service -or $service.Status -ne "Running") {
        $recommendations += (
            "WINDOWS SERVICE: Investigate the status " +
            "and expected startup behavior of $serviceName."
        )
    }
}

# Display recommendations
if ($recommendations.Count -eq 0) {
    Write-Host "[PASS] No issues detected by the configured checks." -ForegroundColor Green
}
else {
    Write-Host "Issues requiring attention: $($recommendations.Count)" -ForegroundColor Yellow
    Write-Host ""

    foreach ($recommendation in $recommendations) {
        Write-Host "[RECOMMENDATION] $recommendation" -ForegroundColor Yellow
        Write-Host ""
    }
}

Write-Host "Troubleshooting analysis completed!"



# ==================================
# Step 6: Diagnostic Report Export
# ==================================

Write-Host ""
Write-Host "=================================="
Write-Host "       REPORT GENERATION"
Write-Host "=================================="

# Create a reports folder if it does not exist
$reportFolder = Join-Path $PSScriptRoot "reports"

if (-not (Test-Path $reportFolder)) {
    New-Item -ItemType Directory -Path $reportFolder | Out-Null
}

# Generate a unique filename
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportPath = Join-Path $reportFolder "diagnostics_$timestamp.txt"

# Build the report
$report = @()

$report += "IT SUPPORT DIAGNOSTIC REPORT"
$report += "============================"
$report += "Generated: $(Get-Date)"
$report += ""

$report += "SYSTEM INFORMATION"
$report += "------------------"
$report += "Computer Name: $computerName"
$report += "Operating System: $($operatingSystem.Caption)"
$report += "CPU: $($processor.Name)"
$report += "Total RAM: $totalRAM GB"
$report += "System Uptime: $($uptime.Days) days, $($uptime.Hours) hours"
$report += ""

$report += "NETWORK DIAGNOSTICS"
$report += "-------------------"

if ($null -ne $network) {
    $report += "IPv4 Address: $ipAddress"
    $report += "Default Gateway: $gateway"
    $report += "DNS Servers: $dnsServers"
    $report += "Gateway Reachable: $gatewayReachable"
}
else {
    $report += "No active IPv4 network with a default gateway detected."
}

$report += "DNS Resolution: $([bool]$dnsResult)"
$report += "HTTPS Connectivity: $internetTest"
$report += ""

$report += "DISK HEALTH"
$report += "-----------"

foreach ($disk in $disks) {

    if ($disk.Size -le 0) {
        continue
    }

    $freePercent = [math]::Round(
        ($disk.FreeSpace / $disk.Size) * 100, 2
    )

    $freeGB = [math]::Round($disk.FreeSpace / 1GB, 2)

    $report += "$($disk.DeviceID) - $freeGB GB free ($freePercent%)"
}

$report += ""
$report += "WINDOWS SERVICES"
$report += "----------------"

foreach ($serviceName in $servicesToCheck) {
    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

    if ($null -eq $service) {
        $report += "$serviceName : Not Found"
    }
    else {
        $report += "$serviceName : $($service.Status)"
    }
}

$report += ""
$report += "TROUBLESHOOTING RECOMMENDATIONS"
$report += "-------------------------------"

if ($recommendations.Count -eq 0) {
    $report += "No issues detected by the configured checks."
}
else {
    foreach ($recommendation in $recommendations) {
        $report += $recommendation
    }
}

# Save report
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "[PASS] Diagnostic report generated!" -ForegroundColor Green
Write-Host "Report saved to: $reportPath"
