from src.interface_adapters.controllers import PuntoEquilibrioController


class _FakeUseCase:
    def __init__(self) -> None:
        self.received = None

    def execute(self, data):
        self.received = data
        return {"ok": True}


def test_controller_delega_en_use_case():
    use_case = _FakeUseCase()
    controller = PuntoEquilibrioController(use_case=use_case)

    result = controller.handle(
        cf=1,
        productos=["A"],
        pv=[10],
        cv=[5],
        m=[1.0],
    )

    assert result == {"ok": True}
    assert use_case.received.cf == 1
    assert use_case.received.productos == ["A"]
    assert use_case.received.pv == [10]
    assert use_case.received.cv == [5]
    assert use_case.received.m == [1.0]
