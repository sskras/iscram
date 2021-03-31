from importlib.resources import read_text

from pytest import approx

from iscram.domain.model import SystemGraph, Trait

from iscram.adapters.repository import FakeRepository

from iscram.adapters.json import load_system_graph_json_str

from iscram.service_layer import services


def test_get_birnbaum_structural_importance(simple_and: SystemGraph):

    repo = FakeRepository()
    bst_imps = services.get_birnbaum_structural_importances(simple_and, repo)

    assert len(bst_imps) != 0


def test_get_birnbaum_importance(simple_and: SystemGraph):

    repo = FakeRepository()
    b_imps = services.get_birnbaum_importances(simple_and, repo)

    assert len(b_imps) != 0


def test_select_attribute_no_suppliers(full_example: SystemGraph):
    repo = FakeRepository()
    result = services.get_birnbaum_importances_select(full_example, Trait("domestic", False), repo)

    assert "birnbaum_importances_select_domestic_False" in result


def test_select_attribute_suppliers(simple_and_suppliers: SystemGraph):
    repo = FakeRepository()
    result = services.get_birnbaum_importances_select(simple_and_suppliers, Trait("domestic", False), repo)

    assert "birnbaum_importances_select_domestic_False" in result
    assert result["birnbaum_importances_select_domestic_False"] == 0


def test_get_cutsets(simple_and: SystemGraph):
    repo = FakeRepository()
    cutsets = services.get_cutsets(simple_and, repo)

    assert len(cutsets) == 2


def test_risk_cutsets_chained(simple_and: SystemGraph):
    repo = FakeRepository()

    risk = services.get_risk(simple_and, repo)

    cutsets = repo.get(simple_and, "cutsets")

    assert len(cutsets) == 2


def test_manually_inserted_cutsets(simple_or: SystemGraph):
    repo = FakeRepository()

    repo.put(simple_or, "cutsets", frozenset([frozenset(["three"])])) ## false info

    risk = services.get_risk(simple_or, repo)

    assert risk == 0.25 # make sure we are actually using the cached, false info

    repo.delete(simple_or, "cutsets")
    repo.delete(simple_or, "risk")

    risk = services.get_risk(simple_or, repo)

    assert risk == approx(1 - (.75 * .75 * .75)) ## make sure we can clear bad info from cache



# def test_scale_rand_tree_50():
#     json_str = read_text("iscram.tests.system_graph_test_data", "random_tree_50.json")
#
#     sg = load_system_graph_json_str(json_str)
#     repo = FakeRepository()
#     assert services.get_risk(sg, repo) >= 0.0


def test_scale_rand_tree_25():
    json_str = read_text("iscram.tests.system_graph_test_data", "random_tree_25.json")

    sg = load_system_graph_json_str(json_str)
    repo = FakeRepository()
    assert services.get_risk(sg, repo) >= 0.0

def test_scale_rand_tree_10():
    json_str = read_text("iscram.tests.system_graph_test_data", "random_tree_10.json")

    sg = load_system_graph_json_str(json_str)
    repo = FakeRepository()
    assert services.get_risk(sg, repo) >= 0.0