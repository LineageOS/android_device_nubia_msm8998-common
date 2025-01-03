#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools

extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_17_2'

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/lib-imsvideocodec.so': blob_fixup()
        .add_needed('libgui_shim.so')
        .replace_needed('libqdMetaData.so', 'libqdMetaData.system.so'),
    'vendor/bin/thermal-engine': blob_fixup()
        .binary_regex_replace(b'/system/etc/.tp/', b'/vendor/etc/.tp/'),
    'vendor/lib64/libril-qc-hal-qmi.so': blob_fixup()
        .replace_needed('android.hardware.radio.config@1.0.so', 'android.hardware.radio.c_shim@1.0.so')
        .replace_needed('android.hardware.radio.config@1.1.so', 'android.hardware.radio.c_shim@1.1.so')
        .replace_needed('android.hardware.radio.config@1.2.so', 'android.hardware.radio.c_shim@1.2.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'msm8998-common',
    'nubia',
    blob_fixups=blob_fixups,
    check_elf=False,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
