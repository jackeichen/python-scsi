# coding: utf-8

# Copyright (C) 2024 by Brian Meagher<brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_synchronize_cache16 import SynchronizeCache16
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbSynchronizeCache16Test(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(sbc)) as s:
            s.blocksize = 512

            sc = s.synchronizecache16(1024, 25)
            cdb = sc.cdb
            self.assertEqual(cdb[0], s.device.opcodes.SYNCHRONIZE_CACHE_16.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(scsi_ba_to_int(cdb[2:10]), 1024)
            self.assertEqual(scsi_ba_to_int(cdb[10:14]), 25)
            self.assertEqual(cdb[14], 0)
            cdb = sc.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.SYNCHRONIZE_CACHE_16.value)
            self.assertEqual(cdb["immed"], 0)
            self.assertEqual(cdb["lba"], 1024)
            self.assertEqual(cdb["group"], 0)
            self.assertEqual(cdb["numblks"], 25)

            d = SynchronizeCache16.unmarshall_cdb(SynchronizeCache16.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            sc = s.synchronizecache16(65536, 27, immed=1, group=19)
            cdb = sc.cdb
            self.assertEqual(cdb[0], s.device.opcodes.SYNCHRONIZE_CACHE_16.value)
            self.assertEqual(cdb[1], 0x02)
            self.assertEqual(scsi_ba_to_int(cdb[2:10]), 65536)
            self.assertEqual(scsi_ba_to_int(cdb[10:14]), 27)
            self.assertEqual(cdb[14], 0x13)
            cdb = sc.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.SYNCHRONIZE_CACHE_16.value)
            self.assertEqual(cdb["immed"], 1)
            self.assertEqual(cdb["lba"], 65536)
            self.assertEqual(cdb["group"], 19)
            self.assertEqual(cdb["numblks"], 27)

            d = SynchronizeCache16.unmarshall_cdb(SynchronizeCache16.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
