import pytest

from careamics_restoration.config import Configuration
from careamics_restoration.engine import Engine
from careamics_restoration.models import create_model


def test_engine_init_errors():
    with pytest.raises(ValueError):
        Engine(config=None, config_path=None, model_path=None)

    with pytest.raises(TypeError):
        Engine(config="config", config_path=None, model_path=None)


def test_engine_predict_errors(minimum_config: dict):
    config = Configuration(**minimum_config)
    engine = Engine(config=config)

    with pytest.raises(ValueError):
        engine.predict(external_input=None, pred_path=None)

    config.data.mean = None
    config.data.std = None
    with pytest.raises(ValueError):
        engine.predict(external_input=None, pred_path="None")


@pytest.mark.parametrize(
    "epoch, losses", [(0, [1.0]), (1, [1.0, 0.5]), (2, [1.0, 0.5, 1.0])]
)
def test_engine_save_checkpoint(epoch, losses, minimum_config: dict):
    init_config = Configuration(**minimum_config)
    engine = Engine(config=init_config)
    path = engine.save_checkpoint(epoch=epoch, losses=losses, save_method="state_dict")
    assert path.exists()

    if epoch == 0:
        assert path.stem.split("_")[-1] == "best"

    assert (
        path.stem.split("_")[-1] == "best"
        if losses[-1] == min(losses)
        else path.stem.split("_")[-1] == "latest"
    )

    model, optimizer, scheduler, scaler, config = create_model(model_path=path)
    assert model is not None
    assert config is not None

    assert config == init_config
