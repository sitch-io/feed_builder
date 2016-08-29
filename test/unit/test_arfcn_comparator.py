import imp
import os
modulename = 'sitchlib'
modulepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
file, pathname, description = imp.find_module(modulename, [modulepath])
sitchlib = imp.load_module(modulename, file, pathname, description)


class TestArfcnComparator:
    def test_instantiate_comparator(self):
        comparator = sitchlib.ArfcnComparator()
        assert comparator

    def test_comparator_match(self):
        reference = {120.00000001: 999,
                     124.99999999991: 001,
                     788.000000000001: 002,
                     790: 998}
        start = 123.456
        end = 789.10
        result = sitchlib.ArfcnComparator.get_arfcn_list_by_range(reference,
                                                                  start,
                                                                  end)
        assert len(result) == 2

    def test_comparator_no_match(self):
        reference = {120.00000001: 999,
                     124.99999999991: 001,
                     788.000000000001: 002,
                     790: 998}
        start = 1
        end = 2
        result = sitchlib.ArfcnComparator.get_arfcn_list_by_range(reference,
                                                                  start,
                                                                  end)
        assert len(result) == 0
