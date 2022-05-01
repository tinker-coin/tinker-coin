# from unittest import TestCase
#
# from datatypes.tinker import Tinker
# from exceptions.tinkervalueexception import TinkerValueException
#
#
# class TestTinker(TestCase):
#
#     def test_empty(self):
#         t = Tinker()
#         self.assertEqual(0, t.tink)
#         self.assertEqual(0, t.tinker)
#
#     def test_init_empty_tink(self):
#         t = Tinker(0)
#         self.assertEqual(0, t.tink)
#         self.assertEqual(0, t.tinker)
#
#     def test_init_all_zeros(self):
#         t = Tinker(0, 0)
#         self.assertEqual(0, t.tink)
#         self.assertEqual(0, t.tinker)
#
#     def test_init_valid_value(self):
#         t = Tinker(5, 1000)
#         self.assertEqual(1000, t.tink)
#         self.assertEqual(5, t.tinker)
#
#     def test_negative_tink(self):
#         self.assertRaises(TinkerValueException, lambda: Tinker(5, -1000))
#
#     def test_negative_tinker(self):
#         self.assertRaises(TinkerValueException, lambda: Tinker(-5, 1000))
#
#     def test_init_tink_upper_value(self):
#         t = Tinker(5, 999999999)
#         self.assertEqual(999999999, t.tink)
#         self.assertEqual(5, t.tinker)
#
#     def test_init_tink_upper_value_breached(self):
#         self.assertRaises(TinkerValueException, lambda: Tinker(5, 999999999 + 1))
#
#     def test_init_very_big_tink_value(self):
#         self.assertRaises(TinkerValueException, lambda: Tinker(5, 100000000000))
#
#     def test_to_string(self):
#         self.assertEqual("0.000000000", str(Tinker(0, 0)))
#         self.assertEqual("5.000000000", str(Tinker(5, 0)))
#         self.assertEqual("0.000000100", str(Tinker(0, 100)))
#         self.assertEqual("5.000000001", str(Tinker(5, 1)))
#         self.assertEqual("5.999999999", str(Tinker(5, 999999999)))
#         self.assertEqual("8348247477.123456789", str(Tinker(8348247477, 123456789)))
#         self.assertEqual("83482474778348247477.123456789", str(Tinker(83482474778348247477, 123456789)))
#
#     def test_simple_sum(self):
#         a = Tinker(1, 2)
#         b = Tinker(3, 4)
#         c = a + b
#         self.assertEqual(6, c.tink)
#         self.assertEqual(4, c.tinker)
#
#     def test_tink_carryover_on_sum(self):
#         a = Tinker(1, 999999990)
#         b = Tinker(3, 400)
#         c = a + b
#         self.assertEqual(390, c.tink)
#         self.assertEqual(5, c.tinker)
