# -*- coding: utf-8 -*-

from importlib import import_module
from sys import modules as sys_modules
from unittest import main

from plugpack.module.mixin._base import module_stash  # noqa
from plugpack.module.module import Module
from tester.unittest.module_test_case import ModuleIsolatedAsyncioTestCase


class ModuleTestCase(ModuleIsolatedAsyncioTestCase):
    def test_module_stash(self):
        module_name = self.plugpack_test_open
        import_module(module_name)
        self.assertIn(module_name, sys_modules)

        key = "key1"

        setattr(sys_modules[module_name], key, 100)
        self.assertEqual(100, getattr(sys_modules[module_name], key))

        with module_stash(module_name):
            self.assertNotIn(module_name, sys_modules)
            test_module = import_module(module_name)
            self.assertIn(module_name, sys_modules)

        self.assertTrue(hasattr(sys_modules[module_name], key))
        self.assertFalse(hasattr(test_module, key))

        setattr(test_module, key, 200)
        self.assertEqual(100, getattr(sys_modules[module_name], key))
        self.assertEqual(200, getattr(test_module, key))

    def test_isolated_modules(self):
        module0 = Module(self.plugpack_test_open, isolate=True)
        module1 = Module(self.plugpack_test_open, isolate=True)

        key = "key2"

        self.assertFalse(module0.has(key))
        self.assertFalse(module1.has(key))

        module0.set(key, 100)
        module1.set(key, 200)
        self.assertTrue(module0.has(key))
        self.assertTrue(module1.has(key))

        self.assertEqual(100, module0.get(key))
        self.assertEqual(200, module1.get(key))

    def test_attributes(self):
        module = Module(self.plugpack_test_open)
        self.assertEqual(self.plugpack_test_open, module.module_name)
        self.assertEqual("0.0.0", module.version)
        self.assertEqual("Documentation", module.doc)

    def test_open_close(self):
        module = Module(self.plugpack_test_open)
        self.assertFalse(module.opened)
        module.open()
        self.assertTrue(module.opened)
        module.close()
        self.assertFalse(module.opened)

    async def test_async_open_close(self):
        module = Module(self.plugpack_test_async_open)
        self.assertFalse(module.async_opened)
        await module.async_open()
        self.assertTrue(module.async_opened)
        await module.async_close()
        self.assertFalse(module.async_opened)


if __name__ == "__main__":
    main()
