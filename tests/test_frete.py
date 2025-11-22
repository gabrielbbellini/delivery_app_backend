import pytest

from src.models import FreightTypeEnum
from src.utils import calculate_freight_price

class TestFrete:
    @pytest.mark.parametrize(
        "peso, distancia, tipo, valor_esperado",
        [
            (2.0, 500, FreightTypeEnum.normal, 1005.00),
            (2.0, 500, FreightTypeEnum.sedex, 1010.00),
            (3.4, 500, FreightTypeEnum.sedex10, 1715.00),
        ],
        ids=[FreightTypeEnum.normal, FreightTypeEnum.sedex, FreightTypeEnum.sedex10],
    )
    def test_gerar_frete_opcoes_validas(
        self, peso, distancia, tipo, valor_esperado
    ):
        resultado = calculate_freight_price(distancia, peso, tipo)
        assert resultado == valor_esperado

    def test_input_peso_invalido(self):
        peso = -3
        distancia = 500
        tipo = FreightTypeEnum.sedex10
        with pytest.raises(ValueError):
            resultado = calculate_freight_price(distancia, peso, tipo)

    def test_input_tipo_invalido(self):
        peso = 4
        distancia = 500
        tipo = "fedex"
        with pytest.raises(ValueError):
            resultado = calculate_freight_price(distancia, peso, tipo)

    def test_input_distancia_invalida(self):
        peso = 4.2
        distancia = 0
        tipo = FreightTypeEnum.sedex10
        with pytest.raises(ValueError):
            resultado = calculate_freight_price(distancia, peso, tipo)

    def test_gerar_frete_entrada_nao_numerica(self):
        peso = "abc"
        distancia = 500
        tipo = FreightTypeEnum.normal
        with pytest.raises(TypeError):
            calculate_freight_price(distancia, peso, tipo)

    def test_gerar_frete_entrada_nula(self):
        peso = None
        distancia = 500
        tipo = FreightTypeEnum.normal
        with pytest.raises(TypeError):
            calculate_freight_price(distancia, peso, tipo)
