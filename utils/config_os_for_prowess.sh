#!/bin/bash

# Ensure that this script is being run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi
arch=$(uname -m)

# Identify all hyperthreads for segmentation into system and user space
user_cores=""
system_cores=""
if [[ "$arch" == "aarch64" ]]; then
   for line in $(grep "processor" /proc/cpuinfo | grep -o ":.*" | grep -o "[^: \t].*"); do
      if [[ $line < 2 ]]; then system_cores=$system_cores","$line
      else user_cores=$user_cores","$line
      fi
   done
else
   found_core=false
   found_sys_core=false
   while read line; do
      if [[ "$line" == "core id"*"0" ]]; then found_sys_core=true
      elif [[ "$line" == "core id"* ]]; then found_core=true
      elif [ "$found_sys_core" = true ] && [[ "$line" == "apicid"* ]]; then
         found_sys_core=false
         system_cores=$system_cores","$(echo "$line" | grep -o ":.*" | grep -o "[^: \t].*")
      elif [ "$found_core" = true ] && [[ "$line" == "apicid"* ]]; then
         found_core=false
         user_cores=$user_cores","$(echo "$line" | grep -o ":.*" | grep -o "[^: \t].*")
      fi
   done < /proc/cpuinfo
fi
system_cores="${system_cores:1}"
user_cores="${user_cores:1}"

# Delete all existing CPU sets and create a new CPU set for GnuRadio
cset -m set | grep ";" | grep -v root | cut -d ";" -f1 | xargs -n1 cset set --destroy
for group in $(cset -m set | grep ";" | grep -v root | egrep -o "^[^;]*?"); do
   sudo cset set --cpu=$system_cores $group
done
cset shield --sysset=system --userset=gr-prowess --cpu="$user_cores" --kthread=on
chown -R root:$SUDO_USER /sys/fs/cgroup/cpuset
chmod -R g+rwx /sys/fs/cgroup/cpuset

# Determine the appropriate CPU mask for setting IRQ affinities
irq_mask=0
for i in ${system_cores//,/ }; do
   irq_mask=$(($irq_mask | 1 << $i))
done
irq_mask=$(printf "%x" $irq_mask)

# Update all IRQ affinities
if systemctl list-units --full --all | grep -Fq "irqbalance.service"; then
   systemctl stop irqbalance.service
fi
for irq in $(ls /proc/irq/*/smp_affinity); do
   echo $irq_mask | tee $irq >/dev/null
done

# Set the CPU governer to performance mode to disable CPU frequency scaling
for (( i=0 ; i<$(getconf _NPROCESSORS_ONLN) ; i++ )); do
   cpufreq-set -c $i -g performance
   cpufreq-set -c $i -d $(cat /sys/devices/system/cpu/cpu$i/cpufreq/cpuinfo_max_freq)
done

# Force Linux not to interrupt realtime processes
echo 1000000 > /proc/sys/kernel/sched_rt_period_us
echo -1 > /proc/sys/kernel/sched_rt_runtime_us

# Determine if realtime group scheduling was compiled into the kernel
rtGroupEnabled=$(zcat /proc/config.gz | grep CONFIG_RT_GROUP_SCHED | cut -c23-)
if [[ "$rtGroupEnabled" == "Y" ]] || [[  "$rtGroupEnabled" == "y" ]]; then

   # Allocate 0% realtime CPU time to any non gr-prowess group
   for group in $(find /sys/fs/cgroup/cpu/*/ -iname cpu.rt_runtime_us); do
      echo 0 > $group;
   done

   # Allocate unlimited realtime CPU time to gr-prowess
   mkdir -p /sys/fs/cgroup/cpu/gr-prowess
   echo -1 > /sys/fs/cgroup/cpu/cpu.rt_runtime_us
   echo -1 > /sys/fs/cgroup/cpu/gr-prowess/cpu.rt_runtime_us
fi
