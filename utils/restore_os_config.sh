#!/bin/bash

# Ensure that this script is being run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

# Reset realtime group scheduled if compiled into the kernel
rtGroupEnabled=$(zcat /proc/config.gz | grep CONFIG_RT_GROUP_SCHED | cut -c23-)
if [[ "$rtGroupEnabled" == "Y" ]] || [[  "$rtGroupEnabled" == "y" ]]; then
   echo 0 > /sys/fs/cgroup/cpu/gr-prowess/cpu.rt_runtime_us
   echo 950000 > /sys/fs/cgroup/cpu/cpu.rt_runtime_us
fi

# Allow Linux to interrupt realtime processes
echo 1000000 > /proc/sys/kernel/sched_rt_period_us
echo 950000 > /proc/sys/kernel/sched_rt_runtime_us

# Remove the GnuRadio CPU set and reset permissions
cset shield --reset
cset set -s gr-prowess --destroy
cset set -s system --destroy
chown -R root:root /sys/fs/cgroup/cpuset
chmod -R g-wx+r /sys/fs/cgroup/cpuset

# Restore the default IRQ affinities
if systemctl list-units --full --all | grep -Fq "irqbalance.service"; then
   systemctl stop irqbalance.service
fi
default_bitmask=$(cat /proc/irq/default_smp_affinity)
for irq in $(ls /proc/irq/*/smp_affinity); do
   echo $default_bitmask | tee $irq >/dev/null
done
if systemctl list-units --full --all | grep -Fq "irqbalance.service"; then
   systemctl start irqbalance.service
fi

# Reset the CPU governer
for (( i=0 ; i<$(getconf _NPROCESSORS_ONLN) ; i++ )); do
   cpufreq-set -c $i -d $(cat /sys/devices/system/cpu/cpu$i/cpufreq/cpuinfo_min_freq)
done
