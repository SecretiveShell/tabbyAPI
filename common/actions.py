import json
from loguru import logger
from common.tabby_config import config
from endpoints.server import export_openapi
from common.config_models import generate_config_file


def branch_to_actions() -> bool:
    if config.actions.export_openapi:
        openapi_json = export_openapi()

        with open(config.actions.openapi_export_path, "w") as f:
            f.write(json.dumps(openapi_json))
            logger.info(
                "Successfully wrote OpenAPI spec to "
                + f"{config.actions.openapi_export_path}"
            )

    elif config.actions.export_config:
        generate_config_file(config.actions.config_export_path)

    else:
        # did not branch
        return False

    # branched and ran an action
    return True