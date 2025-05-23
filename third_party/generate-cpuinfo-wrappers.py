#!/usr/bin/env python3

from __future__ import print_function
import os


CPUINFO_SOURCES = {
    None: [
        "init.c",
        "api.c",
        "cache.c",
        "log.c",
    ],
    "defined(__linux__)": [
        "linux/multiline.c",
        "linux/cpulist.c",
        "linux/mockfile.c",
        "linux/smallfile.c",
        "linux/processors.c",
    ],
    "defined(__MACH__) && defined(__APPLE__)": [
        "mach/topology.c",
    ],
    "defined(__i386__) || defined(__i686__) || defined(__x86_64__) || defined(_WIN32)": [
        "x86/cache/init.c",
        "x86/cache/deterministic.c",
        "x86/cache/descriptor.c",
        "x86/info.c",
        "x86/mockcpuid.c",
        "x86/isa.c",
        "x86/topology.c",
        "x86/name.c",
        "x86/init.c",
        "x86/uarch.c",
        "x86/vendor.c",
    ],
    "(defined(__i386__) || defined(__i686__) || defined(__x86_64__)) && defined(__linux__)": [
        "x86/linux/init.c",
        "x86/linux/cpuinfo.c",
    ],
    "(defined(__i386__) || defined(__i686__) || defined(__x86_64__)) && defined(__MACH__) && defined(__APPLE__)": [
        "x86/mach/init.c",
    ],
    "defined(_WIN32)": [
        "x86/windows/init.c",
    ],
    "(defined(__arm__) || defined(__aarch64__)) && defined(__linux__)": [
        "arm/linux/cpuinfo.c",
        "arm/linux/hwcap.c",
        "arm/linux/init.c",
        "arm/linux/clusters.c",
        "arm/linux/midr.c",
        "arm/linux/chipset.c",
        "arm/tlb.c",
        "arm/uarch.c",
        "arm/cache.c",
    ],
    "defined(__arm__) && defined(__linux__)": [
        "arm/linux/aarch32-isa.c",
    ],
    "defined(__aarch64__) && defined(__linux__)": [
        "arm/linux/aarch64-isa.c",
    ],
    "(defined(__arm__) || defined(__aarch64__)) && defined(__ANDROID__)": [
        "arm/android/properties.c",
    ],
    "(defined(__arm__) || defined(__aarch64__)) && defined(TARGET_OS_IPHONE) && TARGET_OS_IPHONE": [
        "arm/mach/init.c",
    ],
}


if __name__ == "__main__":
    for condition, filenames in CPUINFO_SOURCES.items():
        for filename in filenames:
            filepath = os.path.join("cpuinfo/wrappers", filename)
            if not os.path.exists(os.path.dirname(filepath)):
                print(filepath)
                os.makedirs(os.path.dirname(filepath))
            with open(filepath, "w") as wrapper:
                print("/* Auto-generated by generate-wrappers.py script. Do not modify */", file=wrapper)
                print(file=wrapper)
                print("#ifdef __APPLE__", file=wrapper)
                print("\t#include <TargetConditionals.h>", file=wrapper)
                print("#endif /* __APPLE__ */", file=wrapper)
                print(file=wrapper)

                if not condition:
                    print(f"#include <{filename}>", file=wrapper)
                else:
                    # Include source file only if condition is satisfied
                    print(f"#if {condition}", file=wrapper)
                    print(f"#include <{filename}>", file=wrapper)
                    print(f"#endif /* {condition} */", file=wrapper)
