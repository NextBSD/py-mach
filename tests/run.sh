#!/bin/sh
export ROOT=`pwd`
export PYTHON=${PYTHON:-python2.7}
export PYTHONPATH=${ROOT}/lib

mkdir -p /tmp/mach_test_logs/
export LOGPATH=/tmp/mach_test_logs/

total_tests=0
total_success=0
total_failed=0
total_skipped=0

for i in ${ROOT}/*/; do
    dir=`basename ${i}`
    if [ "$dir" = "lib" ]; then
        continue
    fi

    total_tests=$(( ${total_tests} + 1 ))

    if [ ! -f ${i}/${dir}.py ]; then
        total_skipped=$(( ${total_skipped} + 1 ))
        skipped_tests="${skipped_tests} ${dir}"
        continue
    fi

    echo "==> Running test ${dir}"
    cd ${dir}
    if ${PYTHON} ${i}/${dir}.py; then
        total_success=$(( ${total_success} + 1 ))
    else
        total_failed=$(( ${total_failed} + 1 ))
        failed_tests="${failed_tests} ${dir}"
    fi
    cd ${ROOT}
done

echo "==> SUMMARY:"
echo "==> ${total_tests} total tests"
echo "==> ${total_success} successes"
echo "==> ${total_failed} failures"
echo "==> ${total_skipped} skipped"

if [ "${total_skipped}" -gt 0 ]; then
    echo "==> Skipped tests:${skipped_tests}"
fi


if [ "${total_failed}" -gt 0 ]; then
    echo "==> Failed tests:${failed_tests}"
fi
